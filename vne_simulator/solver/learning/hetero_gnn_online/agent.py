from turtle import forward
import gym
import torch
from torch import nn
from torch_geometric.data import Data, Batch
from stable_baselines3.common.logger import configure
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from stable_baselines3.common.vec_env import SubprocVecEnv
from sb3_contrib.ppo_mask import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableMultiInputActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker

from .env import HeteroGNNOnlineEnv
from ..neural_network import GATConvNet

"""
Current implementation uses PPO to improve training efficiency
"""


class ActorNet(nn.Module):
    
    def __init__(self) -> None:
        super(ActorNet, self).__init__()

    def forward(self, x):
        return x


class CriticNet(nn.Module):
    
    def __init__(self) -> None:
        super(CriticNet, self).__init__()

    def forward(self, x):
        return x.mean(-1, keepdim=True)


class CustomPolicyAndValue(nn.Module):

    def __init__(self, features_dim, p_net_num_nodes):
        super(CustomPolicyAndValue, self).__init__()
        p_net_input_dim = features_dim
        p_net_edge_dim = 1
        embedding_dim = 128
        self.policy_net = nn.Sequential(
            GATConvNet(p_net_input_dim, 1, embedding_dim=embedding_dim, edge_dim=p_net_edge_dim, dropout_prob=0.0, return_batch=True, pooling=None),
            nn.Flatten()
        )
        self.value_net = nn.Sequential(
            GATConvNet(p_net_input_dim, 1, embedding_dim=embedding_dim, edge_dim=p_net_edge_dim, dropout_prob=0.0, return_batch=True, pooling=None),
            nn.Flatten()
        )
        self.latent_dim_pi = p_net_num_nodes
        self.latent_dim_vf = p_net_num_nodes

    def forward(self, features):
        return self.policy_net(features), self.value_net(features)

    def forward_actor(self, features):
        return self.policy_net(features)

    def forward_critic(self, features):
        return self.value_net(features)

    # def forward(self, observations) -> torch.Tensor:
    #     # p_net
    #     observations['p_net_edge_index'] = observations['p_net_edge_index'].long()
    #     data_list = []
    #     for i in range(len(observations['p_net_x'])):
    #         data = Data(x=observations['p_net_x'][i], edge_index=observations['p_net_edge_index'][i], edge_attr=observations['p_net_edge_attr'][i])
    #         data_list.append(data)
    #     p_net_obs = Batch.from_data_list(data_list)
    #     return p_net_obs
        

class CustomCombinedExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space: gym.spaces.Dict):
        super(CustomCombinedExtractor, self).__init__(observation_space, features_dim=1)
        extractors = {}
        embedding_dim = 128
        # p_net
        p_net_input_dim = observation_space.spaces['p_net_x'].shape[1]
        p_net_num_nodes = observation_space.spaces['p_net_x'].shape[0]
        p_net_edge_dim = 1
        self.p_net_num_nodes = p_net_num_nodes
        p_net_output_dim = embedding_dim
        # extractors['p_net'] = nn.Sequential(
        #     GATConvNet(p_net_input_dim, 1, embedding_dim=embedding_dim, edge_dim=p_net_edge_dim, dropout_prob=0.0, return_batch=True, pooling=None),
        #     nn.Flatten()
        # )
        # v_node
        # v_node_input_dim = observation_space.spaces['v_node'].shape[0]
        # v_node_output_dim = embedding_dim
        # extractors['v_node'] = nn.Sequential(
        #     nn.Linear(v_node_input_dim, embedding_dim),
        #     nn.ReLU(),
        #     nn.Linear(embedding_dim, v_node_output_dim),
        #     nn.ReLU(),
        #     nn.Flatten()
        # )
        fusion_concat_dim = p_net_num_nodes
        # fusion_output_dim = embedding_dim * 4
        # self.extractors = nn.ModuleDict(extractors)
        self.extractors = nn.Identity()
        # self.lins_fusion = nn.Sequential(
        #     nn.Linear(fusion_concat_dim, p_net_num_nodes),
        #     nn.ReLU(),
        # )
        # self._features_dim = p_net_num_nodes
        self._features_dim = p_net_input_dim
        # self.policy_net = nn.Sequential(nn.Identity())
        # self.value_net = nn.Sequential(nn.Identity())

    def forward(self, observations) -> torch.Tensor:
        encoded_tensor_list = []
        # p_net
        observations['p_net_edge_index'] = observations['p_net_edge_index'].long()
        data_list = []
        for i in range(len(observations['p_net_x'])):
            data = Data(x=observations['p_net_x'][i], edge_index=observations['p_net_edge_index'][i], edge_attr=observations['p_net_edge_attr'][i])
            data_list.append(data)
        p_net_obs = Batch.from_data_list(data_list)
        # p_net_node_embeddings = self.extractors['p_net'](p_net_obs)
        # encoded_tensor_list.append(p_net_node_embeddings)
        # v_node
        # v_node_obs = observations['v_node']
        # v_node_embedding = self.extractors['v_node'](v_node_obs)
        # encoded_tensor_list.append(v_node_embedding)
        # fusion = torch.cat(encoded_tensor_list, dim=1)
        # self.lins_fusion(fusion)
        # return p_net_node_embeddings
        return p_net_obs
        

class CustomActorCriticPolicy(MaskableMultiInputActorCriticPolicy):
    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        *args,
        **kwargs,
    ):

        super(CustomActorCriticPolicy, self).__init__(
            observation_space,
            action_space,
            *args,
            **kwargs,
        )
        # Disable orthogonal initialization
        self.ortho_init = True
        self.action_net = ActorNet()
        self.value_net = CriticNet()

    def _build_mlp_extractor(self):
        self.mlp_extractor = CustomPolicyAndValue(self.features_dim, self.features_extractor.p_net_num_nodes)


# env
def mask_fn(env):
    return env.generate_action_mask()

def make_env(config, rank=0):
    def _init():
        env = PpoGatEnv.from_config(config)
        return env
    # env = ActionMasker(env, mask_fn)
    return _init

class PpoGat:

    @staticmethod
    def from_config(config):
        log_dir = config.log_dir
        num_workers = config.num_workers
        # env
        if num_workers > 1:
            envs = [make_env(config, i) for i in range(num_workers)]
            env = SubprocVecEnv(envs)
        else:
            env = make_env(config, 0)()
        # agent
        policy_kwargs = dict(
            features_extractor_class=CustomCombinedExtractor,
        )
        agent = MaskablePPO(MaskableMultiInputActorCriticPolicy, env, verbose=1, gamma=0.99, 
                    policy_kwargs=policy_kwargs, batch_size=256)
        # logger
        logger = configure(log_dir, ["stdout", "csv", "tensorboard"])
        agent.set_logger(logger)
        return env, agent
