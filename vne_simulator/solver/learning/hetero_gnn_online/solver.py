import os
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical
from torch_geometric.data import Data, Batch, HeteroData

from vne_simulator.base import Solution
from .net import ActorCritic, Actor, Critic
from vne_simulator.solver.learning.rl_base import RLSolver, PPOSolver, A2CSolver, RolloutBuffer
from ..utils import get_pyg_data


class HeteroGNNOnlineSolver(PPOSolver):

    def __init__(self, controller, recorder, counter, **kwargs):
        super(HeteroGNNOnlineSolver, self).__init__('ppo_gat', controller, recorder, counter, **kwargs)
        num_p_net_nodes = kwargs['p_net_setting']['num_nodes']
        self.policy = ActorCritic(p_net_num_nodes=num_p_net_nodes, p_net_feature_dim=9, p_net_edge_dim=1, v_node_feature_dim=7, 
                                    embedding_dim=self.embedding_dim, dropout_prob=self.dropout_prob, batch_norm=self.batch_norm).to(self.device)
        self.optimizer = torch.optim.Adam([
                {'params': self.policy.actor.parameters(), 'lr': self.lr_actor},
                {'params': self.policy.critic.parameters(), 'lr': self.lr_critic},
            ],
            # weight_decay=self.weight_decay
        )
                
    def preprocess_obs(self, observation):
        """Preprocess the observation to adapt to batch mode."""
        hetero_data = HeteroData()
        p_x = torch.tensor(observation['p_net_x'])
        p_edge_index = torch.tensor(observation['p_net_edge_index']).long()
        p_edge_attr = torch.tensor(observation['p_net_edge_attr'])
        v_x = torch.tensor(observation['v_net_x'])
        v_edge_index = torch.tensor(observation['v_net_edge_index']).long()
        v_edge_attr = torch.tensor(observation['v_net_edge_attr'])
        # vp_edge_index = torch.tensor(observation['vp_edge_index']).long()
        # vp_edge_attr = torch.tensor(observation['vp_edge_attr'])
        pv_edge_index = torch.tensor(observation['pv_edge_index']).long()
        pv_edge_attr = torch.tensor(observation['pv_edge_attr'])
        hetero_data['p'].x = p_x
        hetero_data['v'].x = v_x
        hetero_data['p', 'connect', 'p'].edge_index = p_edge_index
        hetero_data['v', 'connect', 'v'].edge_index = v_edge_index
        hetero_data['p', 'connect', 'p'].edge_attr = p_edge_attr
        hetero_data['v', 'connect', 'v'].edge_attr = v_edge_attr
        # hetero_data['v', 'map', 'p'].edge_index = vp_edge_index
        # hetero_data['v', 'map', 'p'].edge_attr = vp_edge_attr
        # hetero_data = hetero_data.to(self.device)

        # p_net_data = get_pyg_data(observation['p_net_x'], observation['p_net_edge_index'], observation['p_net_edge_attr'])
        # v_net_data = get_pyg_data(observation['v_net_x'], observation['v_net_edge_index'], observation['v_net_edge_attr'])
        # hetero_data['p'].x = p_net_data.x
        # hetero_data['v'].x = v_net_data.x
        # hetero_data['p', 'connect', 'p'].edge_index = p_net_data.edge_index
        # hetero_data['v', 'connect', 'v'].edge_index = v_net_data.edge_index
        # hetero_data['p', 'connect', 'p'].edge_attr = p_net_data.edge_attr
        # hetero_data['v', 'connect', 'v'].edge_attr = v_net_data.edge_attr
        hetero_data['p', 'pair', 'v'].edge_index = pv_edge_index
        hetero_data['p', 'pair', 'v'].edge_attr = pv_edge_attr
        obs_hetero_data = Batch.from_data_list([hetero_data]).to(self.device)

        # obs_p_net = Batch.from_data_list([p_net_data]).to(self.device)
        # obs_v_net = Batch.from_data_list([v_net_data]).to(self.device)
        # obs_curr_v_node_id = torch.LongTensor(np.array([observation['curr_v_node_id']])).to(self.device)
        # return {'p_net': obs_p_net, 'v_net': obs_v_net, 'curr_v_node_id': obs_curr_v_node_id}
        return {'hetero_data': obs_hetero_data}

    def preprocess_batch_obs(self, obs_batch):
        # p_net_data_list, v_net_data_list, curr_v_node_id_list = [], [], []
        hetero_data_list = []
        for observation in obs_batch:
            p_net_data = get_pyg_data(observation['p_net_x'], observation['p_net_edge_index'], observation['p_net_edge_attr'])
            # p_net_data_list.append(p_net_data)
            v_net_data = get_pyg_data(observation['v_net_x'], observation['v_net_edge_index'], observation['v_net_edge_attr'])
            # v_net_data_list.append(v_net_data)
            # curr_v_node_id_list.append(observation['curr_v_node_id'])
            hetero_data = HeteroData()
            hetero_data['p'].x = p_net_data.x
            hetero_data['v'].x = v_net_data.x
            hetero_data['p', 'connect', 'p'].edge_index = p_net_data.edge_index
            hetero_data['v', 'connect', 'v'].edge_index = v_net_data.edge_index
            hetero_data['p', 'connect', 'p'].edge_attr = p_net_data.edge_attr
            hetero_data['v', 'connect', 'v'].edge_attr = v_net_data.edge_attr
            pv_edge_index = torch.tensor(observation['pv_edge_index']).long()
            pv_edge_attr = torch.tensor(observation['pv_edge_attr'])
            hetero_data['p', 'pair', 'v'].edge_index = pv_edge_index
            hetero_data['p', 'pair', 'v'].edge_attr = pv_edge_attr
            hetero_data_list.append(hetero_data)
        obs_hetero_data = Batch.from_data_list(hetero_data_list).to(self.device)
        # obs_p_net = Batch.from_data_list(p_net_data_list).to(self.device)
        # obs_v_net = Batch.from_data_list(v_net_data_list).to(self.device)
        # obs_curr_v_node_id = torch.LongTensor(np.array(curr_v_node_id_list)).to(self.device)
        # return {'p_net': obs_p_net, 'v_net': obs_v_net, 'curr_v_node_id': obs_curr_v_node_id}
        return {'hetero_data': obs_hetero_data}
