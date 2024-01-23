# ================== Solver List ================== #
# Our Algorithms: [flag_vne]
# Heuristic Baselines: [nrm_rank, nea_rank, pso]
# RL-based Baselines: [mcts, a3c_gcn, pg_cnn, ddpg_attention]
# A3C-GCN Variants: [a3c_gcn_nrm, a3c_gcn_nea, a3c_gcn_multi_policies]
# ================== 1. Key Settings ================== #
solver_name="flag_vne"             # Solver name. Options: SOLVER_LIST
topology="wx100"                   # Topology name. Options: [geant, wx100]
num_train_epochs=100               # Number of training epochs. Options: [0, >0]. If 0, then inference only.
use_pretrained_model=0
num_meta_learning_epochs=0       # Number of meta learning epochs. Only work for FlagVNE and its variants.
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

if [ $topology == "geant" ]; then
    # geant topology
    if [ $num_train_epochs == "0" ]; then
        # inference setting
        aver_arrival_rate_list=$(seq 0.001 0.001 0.012)
        identifier=""
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
        identifier=""
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
        --eval_interval=10 \
        --save_interval=10 \
        --pretrained_model_path=$pretrained_model_path \
        --batch_size=$batch_size \
        --v_sim_setting_aver_arrival_rate=$aver_arrival_rate \
        --verbose=1 \
        --lr_actor=0.001 \
        --lr_critic=0.001 \
        --summary_dir="exp_data/flag_vne/comparison" \
        --summary_file_name="$topology-$solver_name$identifier.csv"
done