import numpy as np
import pandas as pd
import random
from Config import MarketConfig

class MarketMaker:
    def __init__(self, config: MarketConfig):
        self.config = config
        self.cash = 0.0
        self.inventory = 0
        
        self.recent_trades = []
        self.inventory_history = [0]
        self.pnl_history = [0.0]
        
    def Toxicity(self):
        window = self.recent_trades[-10:]
        if len(window) < 5:
            return 0.0
        
        buys = sum(1 for side in window if side == 'buy')
        sells = sum(1 for side in window if side == 'sell')
        imbalance = abs(buys - sells) / len(window)
        
        return imbalance
        
    def Quote(self, mid_price):
        # Avellaneda-Stoikov
        skewed_mid = mid_price - (self.inventory * self.config.inventory_gamma)
        hat_alpha = self.Toxicity()
        dynamic_spread = self.config.spread * (1.0 + self.config.kappa * hat_alpha)
        
        half_spread = dynamic_spread / 2.0   
        bid = np.floor((skewed_mid - half_spread) / self.config.tick) * self.config.tick
        ask = np.ceil((skewed_mid + half_spread) / self.config.tick) * self.config.tick

        return bid, ask
    
    def ExecuteTrade(self, side, bid, ask):
        if side == 'buy':
            self.inventory -= self.config.quote_size
            self.cash += ask * self.config.quote_size
        elif side == 'sell':
            self.inventory += self.config.quote_size
            self.cash -= bid * self.config.quote_size
            
        self.recent_trades.append(side)
        self.inventory_history.append(self.inventory)
        
    def update_pnl(self, current_mid):
        total_wealth = self.cash + self.inventory * current_mid
        return total_wealth