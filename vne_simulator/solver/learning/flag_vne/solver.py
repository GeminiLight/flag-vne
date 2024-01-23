from collections import Counter
import os
import copy
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical
from torch_geometric.data import Data, Batch

from vne_simulator.solver import registry
from vne_simulator.solver.learning.rl_base.buffer import RolloutBuffer
from .instance_env import InstanceRLEnv
from .net import ActorCritic
from vne_simulator.solver.learning.rl_base import RLSolver, PPOSolver, A2CSolver, InstanceAgent, A3CSolver
from ..utils import apply_mask_to_logit, get_pyg_data
from ..obs_handler import POSITIONAL_EMBEDDING_DIM


@registry.register(
    solver_name='flag_vne',
    solver_type='r_learning')
class FlagVneSolver(InstanceAgent, PPOSolver):
    def __init__(self, controller, recorder, counter, **kwargs):
        ### ------------ flag vne ------------ ###
        self.use_bidirectional_action = kwargs.get('use_bidirectional_action', True)
        self.use_meta_learning = kwargs.get('use_meta_learning', True)
        self.num_meta_learning_epochs = kwargs.get('num_meta_learning_epochs', 40)
        # self.num_meta_learning_epochs = 0
        self.use_curriculum_scheduling_strategy = kwargs.get('use_curriculum_scheduling_strategy', True)
        self.infer_with_meta_policy = kwargs.get('infer_with_meta_policy', False)
        ### ------------ flag vne ------------ ###
        InstanceAgent.__init__(self, InstanceRLEnv)
        PPOSolver.__init__(self, controller, recorder, counter, make_policy, obs_as_tensor, **kwargs)
        self.coef_entropy_loss = 0.00
        self.coef_mask_loss = 0.01
        self.clip_grad = True
        if self.use_meta_learning:
            self.meta_policy = copy.deepcopy(self.policy).to(self.device)
            self.meta_optimizer = torch.optim.AdamW(self.meta_policy.parameters(), lr=self.lr_actor, weight_decay=self.weight_decay)
            self.task_policies = {}
            self.task_optimizers = {}
            self.target_steps = 516
            self.outer_repeat_times = 1
            self.inner_repeat_times = self.repeat_times
            self.init_inner_kl_penalty = 1e-3
            self.repeat_times = self.repeat_times * 10
            if self.use_curriculum_scheduling_strategy:
                self.training_task_id_list = []
                self.policy_entropy_threshold = kwargs.get('policy_entropy_threshold', 2.0)
            self.instance_dict = {}

    def solve(self, instance):
        v_net_size = instance['v_net'].num_nodes
        if self.use_meta_learning:
            if self.infer_with_meta_policy or v_net_size not in self.task_policies:
                self.searcher.policy = self.meta_policy
            else:
                self.searcher.policy = self.task_policies[v_net_size]
        v_net, p_net = instance['v_net'], instance['p_net']
        instance_env = self.InstanceEnv(p_net, v_net, self.controller, self.recorder, self.counter, **self.basic_config)
        obs = instance_env.get_observation()
        done = False
        while not done:
            tensor_obs = self.preprocess_obs(obs, device=self.device)
            action, action_logprob = self.select_action(tensor_obs, sample=False)
            obs, reward, done, info = instance_env.step(action)
            if done:
                return instance_env.solution
        raise Exception('')

    def select_action(self, observation, sample=True):
        v_net_size = int(observation['v_net_size'].item())
        mask = observation['action_mask'].reshape(observation['curr_v_node_id'].shape[0], v_net_size, -1).permute(0, 2, 1)
        # high level action
        if self.use_bidirectional_action:
            high_level_mask = (mask.sum(1) != 0).float()
            with torch.no_grad():
                high_level_action_logits = self.policy.forward(observation, actor_high=True)
            high_level_candidate_action_logits = apply_mask_to_logit(high_level_action_logits, high_level_mask) 
            high_level_candidate_action_dist = Categorical(logits=high_level_candidate_action_logits / self.softmax_temp)
            if sample:
                high_level_action = high_level_candidate_action_dist.sample()
            else:
                high_level_action = high_level_candidate_action_logits.argmax(-1)
            high_level_action_logprob = high_level_candidate_action_dist.log_prob(high_level_action)
        else:
            high_level_action = observation['curr_v_node_id']
            high_level_action_logprob = 0
        # low level action
        low_level_mask = mask[torch.arange(mask.shape[0]), :, high_level_action]
        with torch.no_grad():
            low_level_action_logits = self.policy.forward(observation, actor_low=True, high_level_action=high_level_action)
        low_level_candidate_action_logits = apply_mask_to_logit(low_level_action_logits, low_level_mask) 
        low_level_candidate_action_dist = Categorical(logits=low_level_candidate_action_logits / self.softmax_temp)
        low_level_action_dist_for_log_prob = low_level_candidate_action_dist
        if sample:
            low_level_action = low_level_candidate_action_dist.sample()
        else:
            low_level_action = low_level_candidate_action_logits.argmax(-1)
        low_level_action_logprob = low_level_action_dist_for_log_prob.log_prob(low_level_action)
        # high level action logprob and entropy
        action_logprob = high_level_action_logprob + low_level_action_logprob
        # decompose actions
        v_net_size = observation['v_net_size']
        action = v_net_size * low_level_action + high_level_action
        if torch.numel(action) == 1:
            action = action.item()
        else:
            action = action.reshape(-1, ).cpu().detach().numpy()
        # action = action.squeeze(-1).cpu()
        return action, action_logprob.cpu().detach().numpy()

    def check_parameters(self):
        for name, param in self.policy.named_parameters():
            # if there is nan
            if torch.isnan(param).any():
                print(f'nan in {name}')
                import pdb; pdb.set_trace()

    def evaluate_actions(self, old_observations, old_actions, return_others=False):
        v_net_sizes = old_observations['v_net_size']
        # decompose actions
        high_level_old_actions = (old_actions % v_net_sizes).long()
        low_level_old_actions = (old_actions // v_net_sizes).long()
        # obtain masks
        max_v_net_size = int(v_net_sizes.max().item())
        mask = old_observations['action_mask'].reshape(v_net_sizes.shape[0], max_v_net_size, -1).permute(0, 2, 1)
        high_level_mask = (mask.sum(1) != 0).float()
        low_level_mask = mask[torch.arange(mask.shape[0]), :, high_level_old_actions]
        # high level action logprob and entropy
        if self.use_bidirectional_action:
            high_level_action_logits = self.policy.forward(old_observations, actor_high=True)
            high_level_candidate_action_logits = apply_mask_to_logit(high_level_action_logits, high_level_mask) 
            high_level_candidate_action_probs = F.softmax(high_level_candidate_action_logits, dim=-1)
            try:
                high_level_policy_dist = Categorical(high_level_candidate_action_probs)
            except Exception as e:
                self.save_model('debug.pkl')
                import pdb; pdb.set_trace()
            high_level_action_logprobs = high_level_policy_dist.log_prob(high_level_old_actions)
            high_level_dist_entropy = high_level_policy_dist.entropy()
        else:
            high_level_action_logprobs = 0
            high_level_dist_entropy = 0
        # low level action logprob and entropy
        low_level_actions_logits = self.policy.forward(old_observations, actor_low=True, high_level_action=high_level_old_actions)
        low_level_candidate_actions_logits = apply_mask_to_logit(low_level_actions_logits, low_level_mask)
        low_level_candidate_actions_probs = F.softmax(low_level_candidate_actions_logits, dim=-1)
        low_level_policy_dist = Categorical(low_level_candidate_actions_probs)
        low_level_action_logprobs = low_level_policy_dist.log_prob(low_level_old_actions)
        low_level_dist_entropy = low_level_policy_dist.entropy()
        # pairwise action logprob and entropy
        dist_entropy = high_level_dist_entropy + low_level_dist_entropy
        action_logprobs = high_level_action_logprobs + low_level_action_logprobs
        values = self.policy.forward(old_observations, critic=True).squeeze(-1) if hasattr(self.policy, 'evaluate') else None

        if return_others:
            other = {}
            return values, action_logprobs, dist_entropy, other

        return values, action_logprobs, dist_entropy

    def save_model(self, checkpoint_fname):
        if not self.use_meta_learning:
            return super().save_model(checkpoint_fname)
        checkpoint_fname = os.path.join(self.model_dir, checkpoint_fname)
        model_list = [(task_id, self.task_policies[task_id], self.task_optimizers[task_id]) for task_id in self.task_policies.keys()]
        task_model_dict = {}
        task_model_dict['meta_policy'] = {'policy': self.meta_policy.state_dict(), 'optimizer': self.meta_optimizer.state_dict()}
        task_model_dict['task_policies'] = {}
        for task_id, policy, optimizer in model_list:
            task_model_dict['task_policies'][task_id] = {'policy': policy.state_dict(), 'optimizer': optimizer.state_dict()}
        torch.save(task_model_dict, checkpoint_fname)
        print(f'Save model to {checkpoint_fname}\n') if self.verbose >= 0 else None

    def load_model(self, checkpoint_path):
        if not self.use_meta_learning:
            return super().load_model(checkpoint_path)
        print('Attempting to load the pretrained model')
        
        try:
            checkpoint = torch.load(checkpoint_path)
            self.meta_policy.load_state_dict(checkpoint['meta_policy']['policy'])
            self.meta_optimizer.load_state_dict(checkpoint['meta_policy']['optimizer'])
            print('Loaded pretrained meta policy') if self.verbose >= 0 else None
            for task_id in checkpoint['task_policies'].keys():
                if task_id not in self.task_policies:
                    self.task_policies[task_id] = copy.deepcopy(self.meta_policy)
                    self.task_optimizers[task_id] = torch.optim.AdamW(self.task_policies[task_id].parameters(), lr=self.lr_actor, weight_decay=self.weight_decay)
                    print('New task policy is created for task {}'.format(task_id))
                self.task_policies[task_id].load_state_dict(checkpoint['task_policies'][task_id]['policy'])
                self.task_optimizers[task_id].load_state_dict(checkpoint['task_policies'][task_id]['optimizer'])
            print(f'Loaded pretrained task policies') if self.verbose >= 0 else None
            print(f'Loaded pretrained model from {checkpoint_path}') if self.verbose >= 0 else None
        except Exception as e:
            print(f'Load failed from {checkpoint_path}\nInitilized with random parameters') if self.verbose >= 0 else None

    def learn_with_instance(self, instance):
        # sub env for sub agent
        v_net, p_net = instance['v_net'], instance['p_net']
        if not self.use_meta_learning:
            return super().learn_with_instance(instance)
        v_net_size = v_net.num_nodes
        task_id = v_net_size
        if task_id not in self.task_policies:
            self._init_task_policy_and_task_optimizer(task_id)
        self.policy = self.task_policies[v_net_size]
        self.optimizer = self.task_optimizers[v_net_size]
        # add instance
        if self.use_meta_learning and self.training_epoch_id < self.num_meta_learning_epochs:
            if v_net_size in self.instance_dict.keys():
                if len(self.instance_dict[v_net_size]) >= 100:
                    self.instance_dict[v_net_size].pop(0)
                self.instance_dict[v_net_size].append(copy.deepcopy(instance))
            else:
                self.instance_dict[v_net_size] = [instance]
        return super().learn_with_instance(instance)

    def collect_new_task_buffer(self, policy, instance_set, max_num_instances=float('inf'), max_num_experiences=float('inf')):
        self.policy = policy
        task_specific_buffer = RolloutBuffer()
        for i, instance in enumerate(instance_set):
            solution, instance_buffer, last_value = super().learn_with_instance(instance)
            self.merge_instance_experience(instance, solution, instance_buffer, last_value)
            instance_buffer.compute_returns_and_advantages(last_value, gamma=self.gamma, gae_lambda=self.gae_lambda, method=self.compute_advantage_method)
            task_specific_buffer.merge(instance_buffer)
            if task_specific_buffer.size() >= max_num_experiences or i >= max_num_instances:
                break
        return task_specific_buffer

    def update(self):
        if not self.use_meta_learning:
            return super().update()
        if self.training_epoch_id < self.num_meta_learning_epochs:
            # Meta Learning Process
            print('Meta Learning Process')
            self._meta_learning_update()
        else:
            # Fine Tuning Process
            print('Fine Tuning Process')
            self._fine_tuning_update()

    def _init_task_policy_and_task_optimizer(self, task_id):
        self.task_policies[task_id] = copy.deepcopy(self.meta_policy)
        self.task_optimizers[task_id] = torch.optim.AdamW(self.task_policies[task_id].parameters(), lr=self.lr_actor, weight_decay=self.weight_decay)
        print(f'New task policy is created for task {task_id}')

    def _stats_task_dist(self, buffer):
        v_net_size_list = np.array([obs['v_net_size'] for obs in buffer.observations])
        counter = Counter(v_net_size_list)
        task_dist = dict(sorted(counter.items(), key=lambda x: x[0], reverse=False))
        return task_dist

    def _stats_instance_dist(self, ):
        instance_dict = self.instance_dict
        instance_dist = {}
        for task_id in instance_dict.keys():
            instance_dist[task_id] = len(instance_dict[task_id])
        instance_dist = dict(sorted(instance_dist.items(), key=lambda x: x[0], reverse=False))
        return instance_dist

    def _split_buffer(self, buffer):
        # Split buffer
        task_buffers = {}
        v_net_size_list = np.array([obs['v_net_size'] for obs in buffer.observations])
        tasks_list = sorted(list(set(v_net_size_list)))
        for task_id in tasks_list:
            task_indices = np.where(v_net_size_list == task_id)[0]
            task_buffer = RolloutBuffer()
            task_buffer.observations = [buffer.observations[i] for i in task_indices]
            task_buffer.actions = np.array(buffer.actions)[task_indices].tolist()
            task_buffer.logprobs = np.array(buffer.logprobs)[task_indices].tolist()
            task_buffer.rewards = np.array(buffer.rewards)[task_indices].tolist()
            task_buffer.returns = np.array(buffer.returns)[task_indices].tolist()
            task_buffer.dones = np.array(buffer.dones)[task_indices].tolist()
            task_buffer.values = np.array(buffer.values)[task_indices].tolist()
            # task_buffer.action_masks = [buffer.action_masks[i] for i in task_indices]
            task_buffers[task_id] = task_buffer
        task_buffers = {k: task_buffers[k] for k in sorted(list(task_buffers.keys()))}
        return task_buffers

    def _meta_learning_update(self):
        import higher
        import torchopt
        self.policy = self.meta_policy
        meta_buffer = self.buffer
        task_buffers = self._split_buffer(meta_buffer)
        task_dist = self._stats_task_dist(meta_buffer)
        instance_dist = self._stats_instance_dist()
        print(f'Experience distribution: {task_dist}') if self.verbose >= 0 else None
        print(f'Instance distribution: {instance_dist}') if self.verbose >= 0 else None
        if self.use_curriculum_scheduling_strategy:
            if len(self.training_task_id_list) == 0:
                self.training_task_id_list.append(min(task_dist.keys()))
                print(f'Add task {min(task_dist.keys())} to training task list')
            print(f'Training task list: {self.training_task_id_list}') if self.verbose >= 0 else None
        num_tasks = len(task_buffers.keys())
        self.outer_repeat_times = 1
        torch.autograd.set_detect_anomaly(True)
        for i in range(self.outer_repeat_times):
            kls = []
            total_meta_loss = 0
            total_kl_loss = 0
            total_ppo_loss = 0
            aver_actor_loss = 0
            aver_critic_loss = 0
            aver_entropy_loss = 0
            training_tasks_list = sorted(list(task_buffers.keys()))
            if self.use_curriculum_scheduling_strategy:
                most_complex_task_id = self.training_task_id_list[-1]
                training_tasks_list = self.training_task_id_list
            task_policy_entropy_dict = {}
            inner_opt = torchopt.MetaSGD(self.meta_policy, lr=0.01, weight_decay=self.weight_decay)
            policy_state_dict = torchopt.extract_state_dict(self.meta_policy)
            optim_state_dict = torchopt.extract_state_dict(inner_opt)

            for task_id in training_tasks_list:
                inner_kls = []
                inner_repeat_times = int((num_tasks * self.repeat_times) / len(training_tasks_list)) if self.use_curriculum_scheduling_strategy else self.inner_repeat_times
                inner_repeat_times = 10
                for step in range(inner_repeat_times):
                    buffer = task_buffers[task_id]
                    buffer.split_with_instance()
                    observations, actions, old_action_logprobs, rewards, returns = self._preprocess_buffer(buffer)
                    # calculate loss
                    loss, (actor_loss, critic_loss, entropy_loss, values, action_logprobs, advantages, kl_div) = \
                        self._calculate_ppo_loss(observations, actions, old_action_logprobs, returns, clip_loss=True)
                    # update parameters
                    inner_loss = loss
                    inner_opt.step(inner_loss)
                    inner_kls.append(kl_div)
                    kls.append(kl_div.detach())
                print(f'{task_id}-{step}, actor_loss: {actor_loss.detach():.4f}, critic_loss: {critic_loss.detach():.4f}, values: {values.detach().mean():.4f}, entropy_loss: {entropy_loss.mean():.4f}, advantages: {advantages.mean():.4f}') if self.verbose >= 0 else None
                # meta update
                task_specific_buffer = self.collect_new_task_buffer(self.meta_policy, self.instance_dict[task_id], max_num_experiences=64)
                observations, actions, old_action_logprobs, rewards, returns = self._preprocess_buffer(task_specific_buffer)
                ppo_loss, (actor_loss, critic_loss, entropy_loss, values, action_logprobs, advantages, kl_div) = \
                    self._calculate_ppo_loss(observations, actions, old_action_logprobs, returns, clip_loss=True, use_ppo=False)
                kl_loss = torch.zeros(1).to(self.device).mean()
                meta_loss = (ppo_loss + kl_loss)
                print(f'Task {task_id}, meta_loss: {loss:.4f}, kl: {kl_div:.4f}, actor_loss: {actor_loss:.4f}, critic_loss: {critic_loss:.4f}, entropy_loss: {entropy_loss:.4f}') if self.verbose >= 0 else None
                meta_loss.backward()
                torchopt.recover_state_dict(self.meta_policy, policy_state_dict)
                torchopt.recover_state_dict(inner_opt, optim_state_dict)
                total_meta_loss += meta_loss.detach().cpu().numpy()
                total_kl_loss += kl_loss.detach().cpu().numpy()
                total_ppo_loss += ppo_loss.detach().cpu().numpy()
                aver_entropy_loss += entropy_loss.detach().cpu().numpy()
                aver_actor_loss += actor_loss.detach().cpu().numpy()
                aver_critic_loss += critic_loss.detach().cpu().numpy()
            task_policy_entropy_dict[task_id] = entropy_loss.detach().cpu().numpy()
            grad_clipped = torch.nn.utils.clip_grad_norm_(self.meta_policy.parameters(), self.max_grad_norm) if self.clip_grad else None
            self.meta_optimizer.step()
            self.meta_optimizer.zero_grad()
            for name, param in self.meta_policy.named_parameters():
                if torch.isnan(param).any():
                    import pdb; pdb.set_trace()

            list(self.meta_policy.named_parameters())[0]
            num_tasks = len(training_tasks_list)
            aver_actor_loss /= num_tasks
            aver_critic_loss /= num_tasks
            aver_entropy_loss /= num_tasks
            
            if self.use_curriculum_scheduling_strategy:
                most_complex_task_id = self.training_task_id_list[-1]
                if most_complex_task_id >= max(task_dist.keys()):
                    continue
                most_complex_task_policy_entropy = task_policy_entropy_dict[most_complex_task_id]
                if most_complex_task_policy_entropy < self.policy_entropy_threshold:
                    self.training_task_id_list.append(most_complex_task_id + 1)
                    print(f'Add task {most_complex_task_id+1} to training task list')

            print(f'Total_meta_loss: {total_meta_loss:.4f}, ppo loss: {total_ppo_loss:.4f}, actor loss: {aver_actor_loss:.4f}, critic loss: {aver_critic_loss:.4f}, entropy loss: {aver_entropy_loss:.4f}, kl loss: {total_kl_loss:.4f}') if self.verbose >= 0 else None
 
        for task_id in task_buffers.keys():
            self.task_policies[task_id].load_state_dict(self.meta_policy.state_dict())
            # self.task_optimizers[task_id].load_state_dict(self.meta_optimizer.state_dict())
        meta_buffer.clear()
        self.buffer = meta_buffer
        self.instance_dict = {}
        # print(f'meta_loss: {meta_loss.detach():+2.4f}, ppo_loss: {ppo_loss.detach():+2.4f}, inner_kl: {inner_kl.detach():+2.4f}, outer_kl: {outer_kl.detach():+2.4f}') if self.verbose >= 0 else None
        return None

    def _fine_tuning_update(self):
        meta_buffer = self.buffer
        # Initialize task policies
        task_dist = self._stats_task_dist(self.buffer)
        print(f'Task distribution: {task_dist}') if self.verbose >= 0 else None
        for task_id in task_dist.keys():
            if task_id not in self.task_policies:
                self.task_policies[task_id] = copy.deepcopy(self.meta_policy)
                self.task_optimizers[task_id] = torch.optim.AdamW(self.task_policies[task_id].parameters(), lr=self.lr)
        # Split buffer
        task_buffers = self._split_buffer(self.buffer)
        # Inner loop
        # sort by task_id
        task_ids = sorted(list(task_buffers.keys()))
        for task_id in task_ids:
            self.policy = self.task_policies[task_id]
            self.optimizer = self.task_optimizers[task_id]
            self.buffer = task_buffers[task_id]
            super().update()
        meta_buffer.clear()

    def _calculate_ppo_loss(self, observations, actions, old_action_logprobs, returns, clip_loss=False, use_ppo=True):
        # evaluate actions and observations
        values, action_logprobs, dist_entropy = self.evaluate_actions(observations, actions)
        # calculate advantage
        advantages = returns - values.detach()
        if self.norm_advantage and values.numel() != 0:
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-9)
        if use_ppo:
            ratio = torch.exp(action_logprobs - old_action_logprobs)
            surr1 = ratio * advantages
            surr2 = torch.clamp(ratio, 1. - self.eps_clip, 1. + self.eps_clip) * advantages
            actor_loss = - torch.min(surr1, surr2).mean() if clip_loss else -(surr1).mean()
            critic_loss = self.criterion_critic(returns, values)
            kl_div = ((torch.exp(ratio) - 1) - ratio).mean()
        else:
            actor_loss = - (action_logprobs * advantages).mean()
            kl_div = torch.zeros(1).to(self.device).mean()
        critic_loss = self.criterion_critic(returns, values)
        entropy_loss = dist_entropy.mean()
        loss = actor_loss + self.coef_critic_loss * critic_loss - self.coef_entropy_loss * entropy_loss
        # clip gradients
        assert actor_loss.requires_grad
        assert critic_loss.requires_grad
        return loss, (actor_loss, critic_loss, entropy_loss, values, action_logprobs, advantages, kl_div)

    def _preprocess_buffer(self, buffer):
        # Split buffer
        batch_observations = self.preprocess_obs(buffer.observations, self.device)
        batch_actions = torch.LongTensor(np.array(buffer.actions)).to(self.device)
        batch_old_action_logprobs = torch.FloatTensor(np.concatenate(buffer.logprobs, axis=0)).to(self.device)
        batch_rewards = torch.FloatTensor(buffer.rewards).to(self.device)
        batch_returns = torch.FloatTensor(buffer.returns).to(self.device)
        if self.norm_reward:
            batch_returns = (batch_returns - batch_returns.mean()) / (batch_returns.std() + 1e-9)
        return batch_observations, batch_actions, batch_old_action_logprobs, batch_rewards, batch_returns


@registry.register(
    solver_name='flag_vne_meta_free_multi_policy',
    solver_type='r_learning')
class FlagVneMetaFreeMultiPolicySolver(FlagVneSolver):
    def __init__(self, controller, recorder, counter, **kwargs):
        super(FlagVneMetaFreeMultiPolicySolver, self).__init__(controller, recorder, counter, **kwargs)
        ### ------------ flag vne ------------ ###
        self.use_bidirectional_action = True
        self.use_meta_learning = True
        self.num_meta_learning_epochs = 0
        self.use_curriculum_scheduling_strategy = False
        self.infer_with_meta_policy = False
        ### ------------ flag vne ------------ ###


@registry.register(
    solver_name='flag_vne_meta_free_single_policy',
    solver_type='r_learning')
class FlagVneMetaFreeSinglePolicySolver(FlagVneSolver):
    def __init__(self, controller, recorder, counter, **kwargs):
        super(FlagVneMetaFreeSinglePolicySolver, self).__init__(controller, recorder, counter, **kwargs)
        ### ------------ flag vne ------------ ###
        self.use_bidirectional_action = True
        self.use_meta_learning = False
        self.num_meta_learning_epochs = 0
        self.use_curriculum_scheduling_strategy = False
        self.infer_with_meta_policy = False
        ### ------------ flag vne ------------ ###


@registry.register(
    solver_name='flag_vne_meta_policy',
    solver_type='r_learning')
class FlagVneMetaPolicySolver(FlagVneSolver):
    def __init__(self, controller, recorder, counter, **kwargs):
        super(FlagVneMetaPolicySolver, self).__init__(controller, recorder, counter, **kwargs)
        ### ------------ flag vne ------------ ###
        self.use_bidirectional_action = True
        self.use_meta_learning = False
        self.num_meta_learning_epochs = 0
        self.use_curriculum_scheduling_strategy = False
        self.infer_with_meta_policy = True
        ### ------------ flag vne ------------ ###


@registry.register(
    solver_name='flag_vne_no_curriculum',
    solver_type='r_learning')
class FlagVneNoCurriculumSolver(FlagVneSolver):
    def __init__(self, controller, recorder, counter, **kwargs):
        super(FlagVneNoCurriculumSolver, self).__init__(controller, recorder, counter, **kwargs)
        ### ------------ flag vne ------------ ###
        self.use_bidirectional_action = True
        self.use_meta_learning = False
        self.num_meta_learning_epochs = 0
        self.use_curriculum_scheduling_strategy = True
        self.infer_with_meta_policy = False
        ### ------------ flag vne ------------ ###


@registry.register(
    solver_name='flag_vne_unidirectional_action',
    solver_type='r_learning')
class FlagVneUnidirectionalActionSolver(FlagVneSolver):
    def __init__(self, controller, recorder, counter, **kwargs):
        super(FlagVneUnidirectionalActionSolver, self).__init__(controller, recorder, counter, **kwargs)
        ### ------------ flag vne ------------ ###
        self.use_bidirectional_action = False
        self.use_meta_learning = False
        self.num_meta_learning_epochs = 0
        self.use_curriculum_scheduling_strategy = False
        self.infer_with_meta_policy = False
        ### ------------ flag vne ------------ ###


def make_policy(agent, **kwargs):
    num_vn_attrs = agent.v_sim_setting_num_node_resource_attrs
    num_vl_attrs = agent.v_sim_setting_num_link_resource_attrs
    policy = ActorCritic(p_net_num_nodes=agent.p_net_setting_num_nodes, 
                        p_net_feature_dim=num_vn_attrs + num_vl_attrs*3 + 3 + 1 + 1, 
                        p_net_edge_dim=num_vl_attrs,
                        v_net_feature_dim=num_vn_attrs + num_vl_attrs*3 + 2 + 1,
                        v_net_edge_dim=num_vl_attrs,
                        embedding_dim=agent.embedding_dim, 
                        dropout_prob=agent.dropout_prob, 
                        batch_norm=agent.batch_norm).to(agent.device)
    optimizer = torch.optim.AdamW(policy.parameters(), lr=agent.lr_actor, weight_decay=agent.weight_decay)
    return policy, optimizer


def obs_as_tensor(obs, device):
    # one
    if isinstance(obs, dict):
        """Preprocess the observation to adapt to batch mode."""
        observation = obs
        p_net_data = get_pyg_data(observation['p_net_x'], observation['p_net_edge_index'], observation['p_net_edge_attr'])
        v_net_data = get_pyg_data(observation['v_net_x'], observation['v_net_edge_index'], observation['v_net_edge_attr'])
        obs_p_net = Batch.from_data_list([p_net_data]).to(device)
        obs_v_net = Batch.from_data_list([v_net_data]).to(device)
        obs_curr_v_node_id = torch.LongTensor(np.array([observation['curr_v_node_id']])).to(device)
        obs_action_mask = torch.FloatTensor(np.array([observation['action_mask']])).to(device)
        obs_v_net_size = torch.LongTensor(np.array([observation['v_net_size']])).to(device)
        return {'p_net': obs_p_net, 'v_net': obs_v_net, 'curr_v_node_id': obs_curr_v_node_id, 'action_mask': obs_action_mask, 'v_net_size': obs_v_net_size}
    # batch
    elif isinstance(obs, list):
        p_net_data_list, v_net_data_list, curr_v_node_id_list, action_mask_list, v_net_size_list = [], [], [], [], []
        for observation in obs:
            p_net_data = get_pyg_data(observation['p_net_x'], observation['p_net_edge_index'], observation['p_net_edge_attr'])
            p_net_data_list.append(p_net_data)
            v_net_data = get_pyg_data(observation['v_net_x'], observation['v_net_edge_index'], observation['v_net_edge_attr'])
            v_net_data_list.append(v_net_data)            
            curr_v_node_id_list.append(observation['curr_v_node_id'])
            action_mask_list.append(observation['action_mask'])
            v_net_size_list.append(observation['v_net_size'])
        obs_p_net = Batch.from_data_list(p_net_data_list).to(device)
        obs_v_net = Batch.from_data_list(v_net_data_list).to(device)
        obs_curr_v_node_id = torch.LongTensor(np.array(curr_v_node_id_list)).to(device)
        obs_v_net_size = torch.FloatTensor(np.array(v_net_size_list)).to(device)
        # Get the length of the longest sequence
        max_len_action_mask = max(len(seq) for seq in action_mask_list)
        # Pad all sequences with zeros up to the max length
        padded_action_mask = np.zeros((len(action_mask_list), max_len_action_mask))
        for i, seq in enumerate(action_mask_list):
            padded_action_mask[i, :len(seq)] = seq
        obs_action_mask = torch.FloatTensor(np.array(padded_action_mask)).to(device)
        return {'p_net': obs_p_net, 'v_net': obs_v_net, 'curr_v_node_id': obs_curr_v_node_id, 'action_mask': obs_action_mask, 'v_net_size': obs_v_net_size}
    else:
        raise Exception(f"Unrecognized type of observation {type(obs)}")
    