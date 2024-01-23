# ================== Solver list ================== #
# A3C-GCN and its Variants: [a3c_gcn, a3c_gcn_nrm_rank, a3c_gcn_nea_rank, a3c_gcn_multi_policies]
# ================== 1. Key Settings ================== #
solver_name="a3c_gcn_multi_policies"            # Solver name. Options: SOLVER_LIST
topology="wx100"                 # Topology name. Options: [geant, wx100]
num_train_epochs=50              # Number of training epochs. Options: [0, >0]. If 0, then inference only.
use_pretrained_model=0           # Whether to use pretrained model. Options: [0, 1]
infer_with_single_task_policy_id=0  # Whether to infer with single task policy id. Options: [0, 1, 2, ...]
identifier="-train_epochs_$num_train_epochs-batch_size_$batch_size"
# ================ 2. Other Settings ================ #
cuda_device=0                      # Cuda device id
batch_size=128                     # Batch size
# ===================================================== #

# set pretrained model path for testing
declare -A pretrained_model_path_dict_for_geant
declare -A pretrained_model_path_dict_for_wx100
pretrained_model_path_dict_for_wx100["a3c_gcn"]=""
pretrained_model_path_dict_for_wx100["a3c_gcn_nrm_rank"]=""
pretrained_model_path_dict_for_wx100["a3c_gcn_nea_rank"]=""
pretrained_model_path_dict_for_wx100["a3c_gcn_multi_policies"]=""
pretrained_model_path_dict_for_geant["a3c_gcn"]=""
pretrained_model_path_dict_for_geant["a3c_gcn_nrm_rank"]=""
pretrained_model_path_dict_for_geant["a3c_gcn_nea_rank"]=""
pretrained_model_path_dict_for_geant["a3c_gcn_multi_policies"]=""

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
        aver_arrival_rate_list=$(seq 0.001 0.001 0.006)
        identifier="-test"
        aver_arrival_rate_list=(0.006)
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
        identifier="-test"
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
        --eval_interval=10 \
        --save_interval=10 \
        --infer_with_single_task_policy_id=$infer_with_single_task_policy_id \
        --pretrained_model_path=$pretrained_model_path \
        --batch_size=$batch_size \
        --v_sim_setting_aver_arrival_rate=$aver_arrival_rate \
        --verbose=1 \
        --lr_actor=0.001 \
        --lr_critic=0.001 \
        --summary_dir="exp_data/flag_vne/preliminary_study" \
        --summary_file_name="$topology-$solver_name$identifier.csv"
done