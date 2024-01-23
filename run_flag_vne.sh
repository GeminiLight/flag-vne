# ================== All solver list ================== #
# Our Algorithms: [flag_vne, flag_vne_single_policy, flag_vne_multi_policies, flag_vne_meta_policy, flag_vne_no_currimulum]
# Heuristic Baselines: [nrm_rank, nea_rank, pso]
# RL-based Baselines: [mcts, a3c_gcn, pg_cnn, ddpg_attention]
# A3C-GCN Variants: [a3c_gcn_nrm, a3c_gcn_nea, a3c_gcn_multi_policies]
# ================== 1. Key Settings ================== #
solver_name="flag_vne_ppo_gcn"             # Solver name. Options: ALL_SOLVER_LIST
topology="geant"                   # Topology name. Options: [geant, wx100]
num_train_epochs=100               # Number of training epochs. Options: [0, >0]. If 0, then inference only.
use_bidirectional_action=1
use_meta_learning=1
num_meta_learning_epochs=50       # Number of meta learning epochs. Only work for FlagVNE and its variants.
use_curriculum_scheduling_strategy=0

v_sim_setting_num_v_nets=100
v_sim_setting_v_net_size_low=2
v_sim_setting_v_net_size_high=10


v_sim_setting_v_net_size_low=12
v_sim_setting_v_net_size_high=12

solver_pretrained_model_name="flag_vne_ppo_gcn_multi_policy"
use_pretrained_model=0

if [ $use_pretrained_model == 1 -a $num_train_epochs == 0 ]; then
    if [ $solver_pretrained_model_name == "flag_vne_ppo_gcn_multi_policy" ]; then
        num_meta_learning_epochs=0
        use_meta_learning=1
        use_curriculum_scheduling_strategy=0
    elif [ $solver_pretrained_model_name == "flag_vne_ppo_gcn_single_policy" ]; then
        num_meta_learning_epochs=0
        use_curriculum_scheduling_strategy=0
        use_meta_learning=0
    elif [ $solver_pretrained_model_name == "flag_vne_ppo_gcn_unidirectional_action" ]; then
        num_meta_learning_epochs=0
        use_meta_learning=0
        use_bidirectional_action=0
        use_curriculum_scheduling_strategy=0
    else
        echo "Error: solver_pretrained_model_name $solver_pretrained_model_name is not supported!"
        exit 1
    fi
fi


declare -A pretrained_model_path_dict_for_geant
declare -A pretrained_model_path_dict_for_wx100
# flag vne multi-policy with 0 meta-learning epochs (multi-policy)
pretrained_model_path_dict_for_wx100["flag_vne_ppo_gcn_multi_policy"]="save/flag_vne_ppo_gcn/nft2b-int-aigc-20240112T153325/model/model-49.pkl"
pretrained_model_path_dict_for_geant["flag_vne_ppo_gcn_multi_policy"]="save/flag_vne_ppo_gcn/nft2b-int-aigc-20240112T154315/model/model-49.pkl"
# flag vne multi-policy with single-policy without meta-learning
pretrained_model_path_dict_for_wx100["flag_vne_ppo_gcn_single_policy"]="save/flag_vne_ppo_gcn/nft2b-int-aigc-20240113T080445/model/model-49.pkl"
pretrained_model_path_dict_for_geant["flag_vne_ppo_gcn_single_policy"]="save/flag_vne_ppo_gcn/nft2b-int-aigc-20240113T080429/model/model-49.pkl"
# flag vne multi-policy with unidirectional action
pretrained_model_path_dict_for_wx100["flag_vne_ppo_gcn_unidirectional_action"]="save/flag_vne_ppo_gcn/nft2b-int-aigc-20240113T080038/model/model-49.pkl"
pretrained_model_path_dict_for_geant["flag_vne_ppo_gcn_unidirectional_action"]="save/flag_vne_ppo_gcn/nft2b-int-aigc-20240113T080101/model/model-59.pkl"
# flag vne multi-policy without curriculum scheduling strategy

if [ $topology == "geant" -a $use_pretrained_model == 1 ]; then
    pretrained_model_path=${pretrained_model_path_dict_for_geant[$solver_pretrained_model_name]}
elif [ $topology == "wx100" -a $use_pretrained_model == 1 ]; then
    pretrained_model_path=${pretrained_model_path_dict_for_wx100[$solver_pretrained_model_name]}
else
    pretrained_model_path="null"
fi
echo $pretrained_model_path
# wx100
# pretrained_model_path="save/pg_cnn/nft2b-int-aigc-20240110T145158/model/model.pkl"
# pretrained_model_path="save/a3c_gcn/nft2b-int-aigc-20240110T145214/model/model.pkl"
# pretrained_model_path="save/ddpg_attention/nft2b-int-aigc-20240110T145228/model/model.pkl"
# geant
# pretrained_model_path="save/pg_cnn/nft2b-int-aigc-20240111T111558/model/model.pkl"
# pretrained_model_path="save/a3c_gcn/nft2b-int-aigc-20240111T111537/model/model.pkl"
# pretrained_model_path="save/ddpg_attention/nft2b-int-aigc-20240111T111613/model/model.pkl"
# ================ 3. Other Settings ================ #
num_workers=1                      # Number of parallel workers for A3C
cuda_device=0                      # Cuda device id
batch_size=128                     # Batch size

# ===================================================== #

identifier="-train_epochs_$num_train_epochs-meta_learning_epochs_$num_meta_learning_epochs-batch_size_$batch_size-use_bidirectional_action_$use_bidirectional_action-use_meta_learning_$use_meta_learning-use_curriculum_scheduling_strategy_$use_curriculum_scheduling_strategy_entropy_0.01"

if [ $topology == "geant" ]; then
    # geant topology
    if [ $num_train_epochs == "0" ]; then
        # inference setting
        aver_arrival_rate_list=$(seq 0.001 0.001 0.012)
        identifier="-test-$solver_pretrained_model_name$identifier"
    else
        # pretrain setting
        aver_arrival_rate_list=(0.001)
        pretrained_model_path="null"
    fi
elif [ $topology == "wx100" ]; then
    # wx100 topology
    if [ $num_train_epochs == "0" ]; then
        # inference setting
        aver_arrival_rate_list=$(seq 0.08 0.02 0.18)
        identifier="-test-$solver_pretrained_model_name$identifier"
        echo $pretrained_model_path
    else
        # pretrain setting
        aver_arrival_rate_list=(0.08)
        pretrained_model_path="null"
    fi
elif [ $topology == "wx500" ]; then
    # geant topology
    if [ $num_train_epochs == "0" ]; then
        # inference setting
        aver_arrival_rate_list=$(seq 0.5 0.5 10.0)
        identifier="-test-$solver_pretrained_model_name$identifier"
    else
        # pretrain setting
        aver_arrival_rate_list=(0.001)
        pretrained_model_path="null"
        v_sim_setting_v_net_size_high=20
    fi
else
    echo "Error: topology $topology is not supported!"
    exit 1
fi

# Judge if the pretrained model exists. If inference, then the path must be valid.
if [ "$pretrained_model_path" == "null" ]; then
    echo "pretrained model path is null, skip the check"
else
    if [ ! -f $pretrained_model_path ]; then
        echo "Error: pretrained model $pretrained_model_path does not exist!"
        exit 1
    fi
fi

for aver_arrival_rate in $aver_arrival_rate_list
do 
    echo "aver_arrival_rate: $aver_arrival_rate"
    CUDA_VISIBLE_DEVICES=$cuda_device \
    python main.py \
        --p_net_topology=$topology \
        --solver_name=$solver_name \
        --num_train_epochs=$num_train_epochs \
        --num_meta_learning_epochs=$num_meta_learning_epochs \
        --use_bidirectional_action=$use_bidirectional_action \
        --use_meta_learning=$use_meta_learning \
        --use_curriculum_scheduling_strategy=$use_curriculum_scheduling_strategy \
        --eval_interval=10 \
        --save_interval=5 \
        --p_net_setting_path="settings/p_net_setting_multi_resource.yaml" \
        --v_sim_setting_path="settings/v_sim_setting_multi_resource.yaml" \
        --v_sim_setting_num_v_nets=$v_sim_setting_num_v_nets \
        --v_sim_setting_v_net_size_low=$v_sim_setting_v_net_size_low \
        --v_sim_setting_v_net_size_high=$v_sim_setting_v_net_size_high \
        --v_sim_setting_node_resource_attrs_high=20 \
        --num_workers=$num_workers \
        --pretrained_model_path=$pretrained_model_path \
        --batch_size=$batch_size \
        --v_sim_setting_aver_arrival_rate=$aver_arrival_rate \
        --verbose=1 \
        --lr_actor=0.001 \
        --lr_critic=0.001 \
        --summary_dir="exp_data/flag_vne" \
        --summary_file_name="$topology-$solver_name$identifier.csv"
done
