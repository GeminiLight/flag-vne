import torch
import torch.nn as nn
import torch.nn.functional as F
from vne_simulator.solver.learning.neural_network import *


class ActorCriticBase(nn.Module):

    def __init__(self, ):
        super(ActorCriticBase, self).__init__()
    
    def act(self, x):
        return self.actor(x)
    
    def evaluate(self, x):
        if not hasattr(self, 'critic'):
            return None
        return self.critic(x)


class ActorCriticWithSharedEncoderBase(nn.Module):

    def __init__(self, ):
        super(ActorCriticWithSharedEncoderBase, self).__init__()
    
    def act(self, x):
        x = self.encoder(x)
        return self.actor(x)
    
    def evaluate(self, x):
        x = self.encoder(x)
        if not hasattr(self, 'critic'):
            return None
        return self.critic(x)