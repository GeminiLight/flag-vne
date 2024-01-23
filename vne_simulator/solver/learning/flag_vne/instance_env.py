import numpy as np
import networkx as nx
from gym import spaces
from vne_simulator.solver.learning.rl_base import JointPRStepInstanceRLEnv, NodePairStepInstanceRLEnv


class InstanceRLEnv(NodePairStepInstanceRLEnv):

    def __init__(self, p_net, v_net, controller, recorder, counter, **kwargs):
        kwargs['node_ranking_method'] = 'nrm'
        super(InstanceRLEnv, self).__init__(p_net, v_net, controller, recorder, counter, **kwargs)
        self.calcuate_graph_metrics(degree=True, closeness=False, eigenvector=False, betweenness=False)
    
    @property
    def next_unplaced_v_node_id(self):
        if self.num_placed_v_net_nodes == self.v_net.num_nodes:
            return 0
        return self.v_net.ranked_nodes[self.num_placed_v_net_nodes]

    def get_observation(self):
        p_net_obs = self._get_p_net_obs()
        v_net_obs = self._get_v_net_obs()
        action_mask = self.generate_action_mask().flatten()
        return {
            'p_net_x': p_net_obs['x'],
            'p_net_edge_index': p_net_obs['edge_index'],
            'p_net_edge_attr': p_net_obs['edge_attr'],
            'v_net_x': v_net_obs['x'],
            'v_net_edge_index': v_net_obs['edge_index'],
            'v_net_edge_attr': v_net_obs['edge_attr'],
            'curr_v_node_id': self.next_unplaced_v_node_id,
            'v_net_size': self.v_net.num_nodes,
            'action_mask': action_mask,
        }

    def _get_p_net_obs(self, ):
        attr_type_list = ['resource']
        v_node_min_link_demend = self.obs_handler.get_v_node_min_link_demend(self.v_net, self.curr_v_node_id)
        # p_subnet = self.obs_handler.get_subgraph_view(self.p_net, v_node_min_link_demend)
        # node data
        node_data = self.obs_handler.get_node_attrs_obs(self.p_net, node_attr_types=attr_type_list, node_attr_benchmarks=self.node_attr_benchmarks)
        p_node_link_max_resource = self.obs_handler.get_link_aggr_attrs_obs(self.p_net, link_attr_types=attr_type_list, aggr='max', link_attr_benchmarks=self.link_attr_benchmarks)
        p_node_link_sum_resource = self.obs_handler.get_link_aggr_attrs_obs(self.p_net, link_attr_types=attr_type_list, aggr='sum', link_sum_attr_benchmarks=self.link_sum_attr_benchmarks)
        p_node_link_mean_resource = self.obs_handler.get_link_aggr_attrs_obs(self.p_net, link_attr_types=attr_type_list, aggr='mean', link_sum_attr_benchmarks=self.link_attr_benchmarks)
        p_nodes_status = self.obs_handler.get_p_nodes_status(self.p_net, self.v_net, self.solution['node_slots'])
        v_node_sizes = np.ones((self.p_net.num_nodes, 1), dtype=np.float32) * self.v_net.num_nodes / 10
        v_num_placed_nodes = np.ones((self.p_net.num_nodes, 1), dtype=np.float32) * self.num_placed_v_net_nodes / 10
        avg_distance = self.obs_handler.get_average_distance(self.p_net, self.solution['node_slots'], normalization=True)
        node_data = np.concatenate((node_data, v_node_sizes, v_num_placed_nodes, p_nodes_status, p_node_link_sum_resource, p_node_link_max_resource, p_node_link_mean_resource, self.p_net_node_degrees, avg_distance), axis=-1)
        edge_index = self.obs_handler.get_link_index_obs(self.p_net)
        link_data = self.obs_handler.get_link_attrs_obs(self.p_net, link_attr_types=attr_type_list, link_attr_benchmarks=self.link_attr_benchmarks)
        # data
        p_net_obs = {
            'x': node_data,
            'edge_index': edge_index,
            'edge_attr': link_data,
        }
        return p_net_obs

    def _get_v_net_obs(self):
        # node data
        attr_type_list = ['resource']
        v_node_sizes = np.ones((self.v_net.num_nodes, 1), dtype=np.float32) * self.v_net.num_nodes / 10
        v_num_placed_nodes = np.ones((self.v_net.num_nodes, 1), dtype=np.float32) * self.num_placed_v_net_nodes / 10
        node_data = self.obs_handler.get_node_attrs_obs(self.v_net, node_attr_types=['resource'], node_attr_benchmarks=self.node_attr_benchmarks)
        v_node_status = self.obs_handler.get_v_nodes_status(self.v_net, self.solution['node_slots'], consist_decision=True)
        v_node_link_max_resource = self.obs_handler.get_link_aggr_attrs_obs(self.v_net, link_attr_types=['resource'], aggr='max', link_attr_benchmarks=self.link_attr_benchmarks)
        v_node_link_sum_resource = self.obs_handler.get_link_aggr_attrs_obs(self.v_net, link_attr_types=['resource'], aggr='sum', link_sum_attr_benchmarks=self.link_sum_attr_benchmarks)
        v_node_link_mean_resource = self.obs_handler.get_link_aggr_attrs_obs(self.v_net, link_attr_types=['resource'], aggr='mean', link_sum_attr_benchmarks=self.link_attr_benchmarks)
        node_data = np.concatenate((node_data, v_node_sizes, v_num_placed_nodes, v_node_status, v_node_link_max_resource, v_node_link_sum_resource, v_node_link_mean_resource), axis=-1)
        link_data = self.obs_handler.get_link_attrs_obs(self.v_net, link_attr_types=['resource'], link_attr_benchmarks=self.link_attr_benchmarks)
        # edge_index
        edge_index = self.obs_handler.get_link_index_obs(self.v_net)
        # edge_attr
        v_net_obs = {
            'x': node_data,
            'edge_index': edge_index,
            'edge_attr': link_data,
        }
        return v_net_obs
    
    def get_p_neighbor_status(self, v_node_id, node_slots, p_nodes_status):
        placed_v_nodes = list(node_slots.keys())
        placed_p_neighbors = []
        for v_neighbor in list(self.v_net.adj[v_node_id].keys()):
            if v_neighbor in placed_v_nodes:
                placed_p_neighbors.append(node_slots[v_neighbor])
        p_nodes_status[placed_p_neighbors, 1] = 1.

    def compute_reward(self, solution):
        """Calculate deserved reward according to the result of taking action."""
        weight = (1 / self.v_net.num_nodes)
        if solution['result']:
            reward = solution['v_net_r2c_ratio']
        elif solution['place_result'] and solution['route_result']:
            reward = weight
        else:
            reward = - weight
        self.solution['v_net_reward'] += reward
        return reward