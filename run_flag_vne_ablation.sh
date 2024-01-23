# ================== All solver list ================== #
# Our Algorithms: [
#   flag_vne, 
#   flag_vne_single_policy, 
#   flag_vne_multi_policies, 
#   flag_vne_meta_policy, 
#   flag_vne_no_currimulum, 
#   flag_vne_unidirectional_action]
# ================== 1. Key Settings ================== #
solver_name="flag_vne"             # Solver name. Options: ALL_SOLVER_LIST
topology="geant"                   # Topology name. Options: [geant, wx100]
num_train_epochs=25               # Number of training epochs. Options: [0, >0]. If 0, then inference only.
num_meta_learning_epochs=20       # Number of meta learning epochs. Only work for FlagVNE and its variants.
use_pretrained_model=0
# ================ 3. Other Settings ================ #
cuda_device=0                      # Cuda device id
batch_size=128                     # Batch size
# ===================================================== #
identifier="-train_epochs_$num_train_epochs-meta_learning_epochs_$num_meta_learning_epochs-batch_size_$batch_size"

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
        identifier="-test-$identifier"
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
        identifier="-test-$identifier"
        echo $pretrained_model_path
    else
        # pretrain setting
        aver_arrival_rate_list=(0.08)
        pretrained_model_path="null"
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
        --pretrained_model_path=$pretrained_model_path \
        --batch_size=$batch_size \
        --v_sim_setting_aver_arrival_rate=$aver_arrival_rate \
        --verbose=1 \
        --lr_actor=0.001 \
        --lr_critic=0.001 \
        --summary_dir="exp_data/flag_vne/ablation" \
        --summary_file_name="$topology-$solver_name$identifier.csv"
done