import numpy as np
import pandas as pd
from Config import MarketConfig

class MarketPrice:
    def __init__(self, config: MarketConfig):
        self.config = config
        self.mid_price = config.start_price
        self.price_history = [self.mid_price]
        
    def StohasticsPrice(self):
        noise = np.random.normal()
        change = (self.config.drift*self.config.dt) + (self.config.base_vol*np.sqrt(self.config.dt)*noise)
        self.mid_price += change
        return self.mid_price
    
# if __name__ == '__main__':
#     config = MarketConfig()
#     MP = MarketPrice(config=config)
#     for _ in range(50):
#         print(MP.StohasticsPrice())