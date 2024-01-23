import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv
from torch_geometric.utils import to_dense_batch

from ..neural_network import *


class ActorCritic(nn.Module):
    
    def __init__(self, p_net_num_nodes, p_net_feature_dim, v_node_feature_dim, embedding_dim=64, dropout_prob=0., batch_norm=False):
        super(ActorCritic, self).__init__()
        self.actor = Actor(p_net_num_nodes, p_net_feature_dim, v_node_feature_dim, embedding_dim, dropout_prob=dropout_prob, batch_norm=batch_norm)
        self.critic = Critic(p_net_num_nodes, p_net_feature_dim, v_node_feature_dim, embedding_dim, dropout_prob=dropout_prob, batch_norm=batch_norm)

    def act(self, obs):
        return self.actor(obs)

    def evaluate(self, obs):
        return self.critic(obs)


class Actor(nn.Module):

    def __init__(self, p_net_num_nodes, p_net_feature_dim, v_node_feature_dim, embedding_dim=64, dropout_prob=0., batch_norm=False):
        super(Actor, self).__init__()
        self.gnn = GCNConvNet(p_net_feature_dim, embedding_dim, embedding_dim=embedding_dim, dropout_prob=dropout_prob, batch_norm=batch_norm, return_batch=True)
        self.mlp = MLPNet(v_node_feature_dim, embedding_dim, num_layers=2, embedding_dims=None, batch_norm=batch_norm, dropout_prob=dropout_prob)
        self.lin_fusion = nn.Sequential(
            nn.Linear(embedding_dim, embedding_dim),
            nn.ReLU(),
            nn.Linear(embedding_dim, 1),
        )

    def forward(self, obs):
        """Return logits of actions"""
        p_node_embeddings = self.gnn(obs['p_net'])
        v_node_embedding = self.mlp(obs['v_net_x'])
        fusion_embeddings = p_node_embeddings + v_node_embedding.unsqueeze(1).repeat(1, p_node_embeddings.shape[1], 1)
        action_logits = self.lin_fusion(fusion_embeddings).squeeze(-1)
        return action_logits


class Critic(nn.Module):

    def __init__(self, p_net_num_nodes, p_net_feature_dim, v_node_feature_dim, embedding_dim=64, dropout_prob=0., batch_norm=False):
        super(Critic, self).__init__()
        self.gnn = GCNConvNet(p_net_feature_dim, embedding_dim, embedding_dim=embedding_dim, dropout_prob=dropout_prob, batch_norm=batch_norm, return_batch=True)
        self.mlp = MLPNet(v_node_feature_dim, embedding_dim, num_layers=2, embedding_dims=None, batch_norm=batch_norm, dropout_prob=dropout_prob)
        self.lin_fusion = nn.Sequential(
            nn.Linear(embedding_dim, embedding_dim),
            nn.ReLU(),
            nn.Linear(embedding_dim, 1),
        )

    def forward(self, obs):
        """Return logits of actions"""
        p_node_embeddings = self.gnn(obs['p_net'])
        v_node_embedding = self.mlp(obs['v_net_x'])
        fusion_embedding = p_node_embeddings + v_node_embedding.unsqueeze(1).repeat(1, p_node_embeddings.shape[1], 1)
        action_logits = self.lin_fusion(fusion_embedding).squeeze(-1)
        value = action_logits.mean(dim=1)
        return value

