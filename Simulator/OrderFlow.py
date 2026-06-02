import numpy as np
import pandas as pd
import random
from Config import MarketConfig

class OrderFlow:
    def __init__(self, config: MarketConfig):
        self.config = config
        self.last_side = None
        
    def PoissonGeneration(self):
        prob_arrive = 1 - np.exp(-self.config.lambda_poisson*self.config.dt)
        return np.random.rand() < prob_arrive
    
    def TraderType(self):
        return np.random.rand() < self.config.toxicity_alpha
    
    def OrderSide(self):
        if self.last_side == None:
            side = np.random.choice(['buy', 'sell'])
        else:
            if np.random.rand() < self.config.order_persistence:
                side = self.last_side
            else:
                side = 'sell' if self.last_side == 'buy' else 'buy'
        
        self.last_side = side
        return side