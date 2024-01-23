from turtle import forward
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, to_hetero
from torch_geometric.utils import to_dense_batch
from ..neural_network import GATConvNet, GraphAttentionPooling, ResNetBlock, MLPNet, NeuralTensorNetwork

# predictor

node_types = ['p', 'v']
metadata = [
    ['v', 'p'],
    [('v', 'connect', 'v'), ('p', 'connect', 'p'), ('p', 'pair', 'v')]
]


# 
# ('v', 'map', 'p')

class Encoder(nn.Module):

    def __init__(self, embedding_dim=128, edge_dim=1):
        super(Encoder, self).__init__()
        self.gnn1 = GATConv((-1, -1), embedding_dim, edge_dim=1)
        self.gnn2 = GATConv((-1, -1), embedding_dim, edge_dim=1)
        self.gnn3 = GATConv((-1, -1), 1, edge_dim=1)

    def forward(self, x, edge_index, edge_attr):
        x = self.gnn1(x, edge_index, edge_attr).relu()
        x = self.gnn2(x, edge_index, edge_attr).relu()
        x = self.gnn3(x, edge_index, edge_attr)
        return x


class ActorCritic(nn.Module):
    
    def __init__(self, p_net_num_nodes, p_net_feature_dim, p_net_edge_dim, v_net_feature_dim, v_net_edge_dim, embedding_dim=128, dropout_prob=0., batch_norm=False):
        super(ActorCritic, self).__init__()
        self.actor = Actor(embedding_dim)
        self.critic = Critic(embedding_dim)
        # self.predictor = Predictor(p_net_num_nodes, p_net_feature_dim, p_net_edge_dim, v_net_feature_dim, v_net_edge_dim, embedding_dim, dropout_prob=dropout_prob, batch_norm=batch_norm)

    def act(self, obs):
        return self.actor.act(obs)

    def evaluate(self, obs):
        return self.critic.evaluate(obs)

    def predict(self, obs):
        output = self.predictor.predict(obs['hetero_data'])
        return output


class Actor(nn.Module):

    def __init__(self, embedding_dim=128):
        super(Actor, self).__init__()
        self.encoder = Encoder(embedding_dim=embedding_dim)
        self.encoder = to_hetero(self.encoder, metadata, aggr='sum')

    def act(self, obs):
        hetero_data = obs['hetero_data']
        x, edge_index, edge_attr = hetero_data.x_dict, hetero_data.edge_index_dict, hetero_data.edge_attr_dict
        embeddings = self.encoder(x, edge_index, edge_attr)
        p_node_embeddings = embeddings['p']
        mask_logits, mask = to_dense_batch(p_node_embeddings, batch=hetero_data.batch_dict['p'])
        mask_logits = mask_logits.squeeze(-1)
        v_node_embeddings = embeddings['v']
        return mask_logits


class Critic(nn.Module):

    def __init__(self, embedding_dim=128):
        super(Critic, self).__init__()
        self.encoder = Encoder(embedding_dim=embedding_dim)
        self.encoder = to_hetero(self.encoder, metadata, aggr='sum')

    def evaluate(self, obs):
        hetero_data = obs['hetero_data']
        x, edge_index, edge_attr = hetero_data.x_dict, hetero_data.edge_index_dict, hetero_data.edge_attr_dict
        embeddings = self.encoder(x, edge_index, edge_attr)
        p_node_embeddings = embeddings['p']
        mask_logits, mask = to_dense_batch(p_node_embeddings, batch=hetero_data.batch_dict['p'])
        mask_logits = mask_logits.squeeze(-1)
        value = torch.mean(mask_logits, dim=-1)
        # v_node_embeddings = embeddings['v']
        return value