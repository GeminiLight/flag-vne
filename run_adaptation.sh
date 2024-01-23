# ================== Solver list ================== #
# Our Algorithms: [flag_vne, flag_vne_meta_free_single_policy, flag_vne_meta_free_multi_policies, flag_vne_meta_policy, flag_vne_no_currimulum]
# ================== 1. Key Settings ================== #
solver_name="flag_vne"             # Solver name. Options: SOLVER_LIST
topology="geant"                   # Topology name. Options: [geant, wx100]
num_train_epochs=5000              # Number of training epochs. Options: [0, >0]. If 0, then inference only.
num_meta_learning_epochs=0       # Number of meta learning epochs. Only work for FlagVNE and its variants.
# ================== 2. Simulation Settings ================== #
v_sim_setting_num_v_nets=1
unseen_v_net_size=12
v_sim_setting_v_net_size_low=$unseen_v_net_size
v_sim_setting_v_net_size_high=$unseen_v_net_size
# ================ 3. Other Settings ================ #
cuda_device=0                      # Cuda device id
batch_size=128                     # Batch size
# ===================================================== #
identifier="-train_epochs_$num_train_epochs-v_sim_setting_num_v_nets_$v_sim_setting_num_v_nets-meta_learning_epochs_$num_meta_learning_epochs-$solver_pretrained_model_name-$use_pretrained_model"

# set pretrained model path for testing
declare -A pretrained_model_path_dict_for_geant
declare -A pretrained_model_path_dict_for_wx100
pretrained_model_path_dict_for_geant["SOLVE_NAME"]="PERTRAINED_MODEL_PATH"
pretrained_model_path_dict_for_wx100["SOLVE_NAME"]="PERTRAINED_MODEL_PATH"

if [ $topology == "geant" -a $use_pretrained_model == 1 ]; then
    pretrained_model_path=${pretrained_model_path_dict_for_geant[$solver_name]}
elif [ $topology == "wx100" -a $use_pretrained_model == 1 ]; then
    pretrained_model_path=${pretrained_model_path_dict_for_wx100[$solver_name]}
else
    pretrained_model_path="null"
fi
echo $pretrained_model_path


if [ $topology == "geant" ]; then
    # geant topology
    if [ $num_train_epochs == "0" ]; then
        # inference setting
        aver_arrival_rate_list=$(seq 0.001 0.001 0.012)
        identifier="-test-$solver_pretrained_model_name-$use_pretrained_model$identifier"
    else
        # pretrain setting
        aver_arrival_rate_list=(0.001)
        # pretrained_model_path="null"
    fi
elif [ $topology == "wx100" ]; then
    # wx100 topology
    if [ $num_train_epochs == "0" ]; then
        # inference setting
        aver_arrival_rate_list=$(seq 0.08 0.02 0.18)
        identifier="-test-$solver_pretrained_model_name-$use_pretrained_model$identifier"
        echo $pretrained_model_path
    else
        # pretrain setting
        aver_arrival_rate_list=(0.08)
        # pretrained_model_path="null"
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
        --eval_interval=$num_train_epochs \
        --save_interval=$num_train_epochs \
        --v_sim_setting_num_v_nets=$v_sim_setting_num_v_nets \
        --v_sim_setting_v_net_size_low=$v_sim_setting_v_net_size_low \
        --v_sim_setting_v_net_size_high=$v_sim_setting_v_net_size_high \
        --pretrained_model_path=$pretrained_model_path \
        --batch_size=$batch_size \
        --v_sim_setting_aver_arrival_rate=$aver_arrival_rate \
        --verbose=1 \
        --lr_actor=0.001 \
        --lr_critic=0.001 \
        --summary_dir="exp_data/flag_vne/adaptation_12" \
        --summary_file_name="$topology-$solver_name$identifier.csv"
done