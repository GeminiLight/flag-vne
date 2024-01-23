# Code for FlagVNE

Contents:

- [Installation](#installation)
- [File Structure](#file-structure)
- [Quick Start](#quick-start)
  - [Preliminary Study](#preliminary-study)
  - [Overall Performance](#overall-performance)
  - [Ablation Study](#ablation-study)
  - [Scalability Validation](#scalability-validation)
  - [Learning Curve](#learning-curve)
  - [Adaption to Unseen Size](#adaption-to-unseen-size)
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
├── dataset
│   └── p_net               # physical network dataset
│       ├── Geant-cpu_[50-100]-max_cpu_None-gpu_[50-100]-max_gpu_None-ram_[50-100]-max_ram_None-bw_[50-100]-max_bw_None
│       │   └── p_net.gml   # Topology: Geant
│       └── Waxman100-cpu_[50-100]-max_cpu_None-gpu_[50-100]-max_gpu_None-ram_[50-100]-max_ram_None-bw_[50-100]-max_bw_None
│           └── p_net.gml   # Topology: WX100
├── main.py
├── settings
│   ├── p_net_setting.yaml  # Setting of physical network 
│   ├── v_sim_setting.yaml  # Setting of virtual network request simulator 
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
    │   │   ├── ddpg_attention                           # Baseline-5: DDPG-Attention
    │   │   ├── mcts                                     # Baseline-6: MCTS
    │   │   └── pg_cnn                                   # Baseline-7: PG-CNN
    │   ├── meta_heuristic                               #
    │   │   └── particle_swarm_optimization_solver.py    # Baseline-8: PSO-VNE
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
    - Our algorithms: [flag_vne, flag_vne_meta_free_single_policy, flag_vne_meta_free_multi_policies, flag_vne_meta_policy, flag_vne_no_currimulum, flag_vne_unidirectional_action]
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

### Preliminary Study

Shell script: `run_preliminary_study.sh`

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

Run the experiments of the overall performance by the following procedure:

```
For topology in [geant, wx100]:
    For solver_name in [flag_vne, nrm_rank, nea_rank, pso_vne, mcts, a3c_gcn, pg_cnn, ddpg_attention]:
        1. Set the solver name to $solver_name in run_exp.sh
        2. Set the topology to $topology in run_exp.sh
        3. Run the code with the following command:
           bash run_exp.sh
```

### Learning Curve

Run the experiments of the learning curve by the following procedure:

```
For topology in [geant, wx100]:
    For solver_name in [flag_vne, flag_vne_meta_free_single_policy, flag_vne_meta_free_multi_policies]:
        1. Set the solver name to $solver_name in run_exp.sh
        2. Set the topology to $topology in run_exp.sh
        3. Run the code with the following command:
           bash run_exp.sh
```

### Adaption to Unseen Size

Run the experiments of the adaption to unseen size by the following procedure:

```
For topology in [geant, wx100]:
    For solver_name in [flag_vne, flag_vne_meta_free_single_policy, flag_vne_meta_free_multi_policies]:
        1. Set the solver name to $solver_name in run_exp_unseen_task.sh
        2. Set the topology to one of the following options: ['geant', 'wx100']
        3. Set the pre-trained model path to the path of the model trained on the training set with the same topology
        4. Set the unseen size to 12
        5. Run the code with the following command:
           bash run_exp_unseen_task.sh
```


### Ablation Study

Run the experiments of the ablation study by the following procedure:

```
For topology in [geant, wx100]:
    For solver_name in [flag_vne, flag_vne_meta_free_single_policy, flag_vne_meta_free_multi_policies]:
        1. Set the solver name to $solver_name in run_exp.sh
        2. Set the topology to one of the following options: ['geant', 'wx100']
        3. Run the code with the following command:
          bash run_exp.sh
```
