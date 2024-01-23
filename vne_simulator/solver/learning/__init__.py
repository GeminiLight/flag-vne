try:
    import torch_sparse, torch_scatter, torch_cluster
except ImportError:
    # raise ImportError('Please install PyTorch Geometric first.')
    print('PyTorch Geometric is not installed completely. Installing now...')
    import os
    import torch
    cuda_version = torch.version.cuda
    if cuda_version is None:
        cuda_suffix = 'cpu'
    elif cuda_version in [11.7, 11.8]:
        cuda_suffix = 'cu' + cuda_version.replace('.', '')
    else:
        cuda_suffix = 'cu117'
    os.system(f'pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.0.0+{cuda_suffix}.html')
    os.system('cls' if os.name == 'nt' else 'clear')


from .mcts import MctsSolver
from .pg_cnn import PgCnnSolver
from .a3c_gcn import A3CGcnSolver
from .ddpg_attention import DdpgAttentionSolver
from .a3c_gcn_seq2seq import A3CGcnSeq2SeqSolver
from .flag_vne import FlagVneSolver


__all__ = [
    'MctsSolver',
    'PgCnnSolver',
    'A3CGcnSolver',
    'DdpgAttentionSolver',
    'A3CGcnSeq2SeqSolver',
    'FlagVneSolver',
]