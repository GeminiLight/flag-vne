import os
import time
import pprint
import socket
import argparse
import networkx as nx

from vne_simulator.utils import read_setting, write_setting


parser = argparse.ArgumentParser(description='configuration file')

def str2bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, int):
        return False if v == 0 else True
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

### Dataset ###
data_arg = parser.add_argument_group('data')
data_arg.add_argument('--p_net_setting_path', type=str, default='settings/p_net_setting_multi_resource.yaml', help='File path of physical network settings')
data_arg.add_argument('--v_sim_setting_path', type=str, default='settings/v_sim_setting_multi_resource.yaml', help='File path of virtual network settings')
data_arg.add_argument('--p_net_topology', type=str, default='wx100', help='Physical network topology')
data_arg.add_argument('--v_sim_setting_num_v_nets', type=int, default=1000, help='')
data_arg.add_argument('--v_sim_setting_v_net_size_low', type=int, default=2, help='')
data_arg.add_argument('--v_sim_setting_v_net_size_high', type=int, default=10, help='')
data_arg.add_argument('--v_sim_setting_node_resource_attrs_low', type=int, default=0, help='')
data_arg.add_argument('--v_sim_setting_node_resource_attrs_high', type=int, default=20, help='')
data_arg.add_argument('--v_sim_setting_link_resource_attrs_low', type=int, default=0, help='')
data_arg.add_argument('--v_sim_setting_link_resource_attrs_high', type=int, default=20, help='')
data_arg.add_argument('--v_sim_setting_aver_arrival_rate', type=float, default=0.08, help='')
data_arg.add_argument('--v_sim_setting_aver_lifetime', type=int, default=500, help='')

### FlagVNE ###
flag_vne_arg = parser.add_argument_group('nrm_rank')
flag_vne_arg.add_argument('--node_ranking_method', type=str, default='order', help='Node ranking method')

### System ###
sys_arg = parser.add_argument_group('system')
sys_arg.add_argument('--summary_dir', type=str, default='save/', help='File Directory to save summary and records')
sys_arg.add_argument('--summary_file_name', type=str, default='global_summary.csv', help='Summary file name')
sys_arg.add_argument('--if_save_records', type=str2bool, default=True, help='Whether to save records')
sys_arg.add_argument('--if_temp_save_records', type=str2bool, default=True, help='Whether to temporarily save records')
sys_arg.add_argument('--p_net_name', type=str2bool, default=True, help='Name of the physical network')
sys_arg.add_argument('--r2c_ratio_threshold', type=float, default=0.0, help='Threshold of revenue-to-cost ratio')
sys_arg.add_argument('--vn_size_threshold', type=float, default=0.0, help='Threshold of virtual network size')

### solver  ###
solver_arg = parser.add_argument_group('solver')
solver_arg.add_argument('--solver_name', type=str, default='flag_vne', help='Name of the solver selected to run')
solver_arg.add_argument('--verbose', type=str2bool, default=1, help='Level of showing information')
solver_arg.add_argument('--reusable', type=str2bool, default=False, help='Whether or not to allow to deploy several VN nodes on the same VNF')

### Reinforcement Learning ###
rl_arg = parser.add_argument_group('net')
# rl
rl_arg.add_argument('--rl_gamma', type=float, default=0.99, help='Cumulative reward discount rate')
# rl_arg.add_argument('--explore_rate', type=float, default=0.9, help='Epsilon-greedy explore rate')
rl_arg.add_argument('--lr', type=float, default=1e-3, help='General Learning rate')
rl_arg.add_argument('--lr_actor', type=float, default=1e-3, help='Actor learning rate')
rl_arg.add_argument('--lr_critic', type=float, default=1e-3, help='Critic learning rate')
rl_arg.add_argument('--lr_penalty_params', type=float, default=1e-1, help='Penalty learning rate')
rl_arg.add_argument('--compute_cost_method', type=str, default='reachability', help='Cost computing method')

### FlagVNE ###
flag_vne_arg = parser.add_argument_group('flag_vne')
flag_vne_arg.add_argument('--num_meta_learning_epochs', type=int, default=50, help='Number of meta learning epochs')
flag_vne_arg.add_argument('--infer_with_single_task_policy_id', type=int, default=0, help='Whether to use single task policy to infer')
flag_vne_arg.add_argument('--use_bidirectional_action', type=str2bool, default=True, help='Whether to use bidirectional action')
flag_vne_arg.add_argument('--use_meta_learning', type=str2bool, default=True, help='Whether to use meta learning')
flag_vne_arg.add_argument('--use_curriculum_scheduling_strategy', type=str2bool, default=False, help='Whether to use curriculum scheduling strategy')
flag_vne_arg.add_argument('--policy_entropy_threshold', type=float, default=2.0, help='policy entropy threshold for curriculum scheduling strategy')

### Training ###
train_arg = parser.add_argument_group('train')
train_arg.add_argument('--use_cuda', type=int, default=1, help='Whether to use GPU')
train_arg.add_argument('--num_train_epochs', type=int, default=100, help='Number of training epochs')
train_arg.add_argument('--distributed_training', type=str2bool, default=True, help='Number of training epochs')
train_arg.add_argument('--num_workers', type=int, default=1, help='Number of workers to distributedly train')
train_arg.add_argument('--batch_size', type=int, default=128, help='Batch size of training')
train_arg.add_argument('--target_steps', type=int, default=1024, help='Number of steps to collect before update')
train_arg.add_argument('--repeat_times', type=int, default=10, help='')
train_arg.add_argument('--gae_lambda', type=float, default=0.98, help='')
train_arg.add_argument('--eps_clip', type=float, default=0.2, help='')
train_arg.add_argument('--use_negative_sample', type=str2bool, default=True, help='Whether to allow use failed sample to train')

### Evaluation ###
train_arg.add_argument('--matching_mathod', type=str, default="greedy", help='') 
train_arg.add_argument('--shortest_method', type=str, default="bfs_shortest", help='') 
train_arg.add_argument('--k_shortest', type=int, default=10, help="k param for k_shortest") 
train_arg.add_argument('--k_searching', type=int, default=3, help='') 
train_arg.add_argument('--decode_strategy', type=str, default='greedy', help='') 

### Run ###
run_arg = parser.add_argument_group('run')
run_arg.add_argument('--renew_v_net_simulator', type=str2bool, default=False, help='')
run_arg.add_argument('--num_epochs', type=int, default=1, help='Number of epochs')
run_arg.add_argument('--seed', type=int, default=0, help='Random seed')
run_arg.add_argument('--pretrained_model_path', type=str, default='', help='')
run_arg.add_argument('--pretrained_subsolver_model_path', type=str, default='', help='')
run_arg.add_argument('--sub_solver_name', type=str, default='nrm_rank', help='')
run_arg.add_argument('--allow_revocable', type=str2bool, default=False, help='')
run_arg.add_argument('--allow_rejection', type=str2bool, default=False, help='')
run_arg.add_argument('--eval_interval', type=int, default=10, help='')
run_arg.add_argument('--save_interval', type=int, default=10, help='')

### Misc ###
misc_arg = parser.add_argument_group('misc')


def get_args(args=None):
    config = parser.parse_args(args)
    return config