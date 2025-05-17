# Code for FlagVNE

> [!IMPORTANT]
> :sparkles: The foundation model of FlagVNE has been integrated into our benchmark [Virne](https://github.com/GeminiLight/virne)
> 
> :sparkles: You can easily run it with a specific solver name `ppo_bigcn+` or `ppo_bigat+` in Virne!

Contents:

- [Installation](#installation)
- [File Structure](#file-structure)
- [Quick Start](#quick-start)
- [Experiments](#experiments)
  - [Preliminary Study](#preliminary-study)
  - [Overall Performance](#overall-performance)
  - [Ablation Study](#ablation-study)
  - [Learning Curve](#learning-curve)
  - [Adaption to Unseen Size](#adaption-to-unseen-size)
  - [Scalability Validation](#scalability-validation)
  - [Hyperparameter Sensitive Study](#hyperparameter-sensitive-study)

## Installation

We recommend using CUDA devices to accelerate the training process. If you do not have a CUDA device, you can also use the CPU to run the code.

With GPU:
```shell
# use cuda (optional version: 10.2, 11.3)
bash install.sh -c 12.1
```

With CPU:
```shell
bash install.sh -c 0
```

## File Structure

```shell
.
├── args.py
├── main.py
├── settings
│   ├── p_net_setting_multi_resource.yaml  # Simulation setting of physical network 
│   ├── v_sim_setting_multi_resource.yaml  # Simulation setting of virtual network request simulator 
└── vne_simulator
    ├── base                # Core components: environment, controller, recorder, scenario, solution
    ├── config.py           # Configuration class
    ├── data                # Data class: attribute, generator, network, physical_network, virtual_network, virtual_network_request_simulator
    ├── solver
    │   ├── heuristic                                    # 
    │   │   ├── node_rank.py                             # Baseline-1 & 2: NRM-VNE and NEA-VNE
    │   ├── learning                                     # 
    │   │   ├── flag_vne                                 # Our Algorithm and its variations: FlagVNE, FlagVNE-MetaFree-SinglePolicy, FlagVNE-MetaFree-MultiPolicies, FlagVNE-NoCurriculum, FlagVNE-NEARank
    │   │   ├── a3c_gcn                                  # Baseline-3 and its variations: A3C-GCN, A3C-GCN-NRM, A3C-GCN-NEA, A3C-GCN-MultiPolicies
    │   │   ├── ddpg_attention                           # Baseline-4: DDPG-Attention
    │   │   ├── mcts                                     # Baseline-5: MCTS
    │   │   └── pg_cnn                                   # Baseline-6: PG-CNN
    │   ├── meta_heuristic                               #
    │   │   └── particle_swarm_optimization_solver.py    # Baseline-7: PSO-VNE
    │   ├── registry.py
    │   └── solver.py
    └── utils
```

## Quick Start

We provide several shell scripts to run the experiment conveniently.

You can customize the settings in the shell scripts.

Key settings in the shell scripts are as follows:

- `topology`:
  - Description: Name of topology
  - Options: [geant, wx100, wx500]
- `solver_name`:
  - Description: Name of solver
  - Options: 
    - Our algorithms: [flag_vne, flag_vne_meta_free_single_policy, flag_vne_meta_free_multi_policy, flag_vne_meta_policy, flag_vne_no_curriculum, flag_vne_unidirectional_action]
    - Baselines: [nrm_rank, nea_rank, pso_vne, mcts, a3c_gcn, pg_cnn, ddpg_attention]
    - Preliminary Study: [a3c_gcn, a3c_gcn_nrm, a3c_gcn_nea, a3c_gcn_multi_policies]
- `num_train_epochs`:
  - Description: Number of training epochs. If 0, then inference only.
  - Options: [0, >0]
- `use_pretrained_model`:
  - Description: Whether to use pretrained model. If 1, then inference only.
  - Options: [1, 0]
- `pretrained_model_path`:
  - Description: Path to the pretrained model. If inference, then the path must be valid.
  - Options: ['null', $path]

## Experiments

### Preliminary Study

shell script: `run_preliminary_study.sh`

Run the experiments of the preliminary study by the following procedure:

```
For topology in [geant, wx100]:
    For solver_name in [a3c_gcn, a3c_gcn_nrm, a3c_gcn_nea, a3c_gcn_multi_policies]:
        1. Set the solver name to $solver_name in run_preliminary_study.sh
        2. Set the topology to $topology in run_preliminary_study.sh
        3. Run the code with the following command:
           bash run_preliminary_study.sh
```

### Overall Performance

shell script: `run_overall_performance.sh`

Run the experiments of the overall performance by the following procedure:

```
For topology in [geant, wx100]:
    For solver_name in [flag_vne, nrm_rank, nea_rank, pso_vne, mcts, a3c_gcn, pg_cnn, ddpg_attention]:
        1. Set the solver name to $solver_name in run_overall_performance.sh
        2. Set the topology to $topology in run_overall_performance.sh
        3. Run the code with the following command:
           bash run_overall_performance.sh
```

### Ablation Study

shell script: `run_ablation_study.sh`

Run the experiments of the ablation study by the following procedure:

```
For topology in [geant, wx100]:
    For solver_name in [flag_vne, flag_vne_meta_free_single_policy, flag_vne_meta_free_multi_policy, flag_vne_meta_policy, flag_vne_no_curriculum, flag_vne_unidirectional_action]:
        1. Set the solver name to $solver_name in run_exp.sh
        2. Set the topology to one of the following options: ['geant', 'wx100']
        3. Run the code with the following command:
          bash run_exp.sh
```

### Learning Curve

shell script: `run_ablation_study.sh`

Run the experiments of the learning curve by the following procedure:


```
For topology in [geant, wx100]:
    For solver_name in [flag_vne, flag_vne_meta_free_single_policy, flag_vne_meta_free_multi_policy, flag_vne_meta_policy, flag_vne_no_curriculum, flag_vne_unidirectional_action]:
        1. Set the solver name to $solver_name in run_ablation_study.sh
        2. Set the topology to $topology in run_ablation_study.sh
        3. Run the code with the following command:
           bash run_ablation_study.sh
```

### Adaption to Unseen Size

shell script: `run_adaptation.sh`

Run the experiments of the adaption to unseen size by the following procedure:

```
For topology in [geant, wx100]:
    For solver_name in [flag_vne, flag_vne_meta_free_single_policy, flag_vne_meta_free_multi_policy, flag_vne_meta_policy, flag_vne_no_curriculum, flag_vne_unidirectional_action]:
        1. Set the solver name to $solver_name in run_adaptation.sh
        2. Set the topology to one of the following options: ['geant', 'wx100']
        3. Set the pre-trained model path to the path of the model trained on the training set with the same topology
        4. Set the unseen size to 12
        5. Run the code with the following command:
           bash run_adaptation.sh
```

### Scalability Validation

shell script: `run_scalability_validation.sh`

Run the experiments of the scalability validation by the following procedure:

```
For topology in [geant, wx100]:
    For solver_name in [flag_vne, nrm_rank, nea_rank, pso_vne, mcts, a3c_gcn, pg_cnn, ddpg_attention]:
        1. Set the solver name to $solver_name in run_scalability_validation.sh
        2. Set the topology to one of the following options: ['wx500']
        3. Run the code with the following command:
          bash run_scalability_validation.sh
```

### Hyperparameter Sensitive Study

shell script: `run_hyperparameter_sensitive_study.sh`

Run the experiments of the hyperparameter sensitive study by the following procedure:

```
For topology in [geant, wx100]:
    For solver_name in [flag_vne]:
        1. Set the solver name to $solver_name in run_hyperparameter_sensitive_study.sh
        2. Set the topology to one of the following options: ['geant', 'wx100']
        2. Set the policy_entropy_threshold to one of the following options: [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
        3. Run the code with the following command:
          bash run_hyperparameter_sensitive_study.sh
```
