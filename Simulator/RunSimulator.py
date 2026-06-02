import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from Config import MarketConfig
from Market import MarketPrice
from OrderFlow import OrderFlow
from MarketMaker import MarketMaker
from Performance import Performance

class Simulator:
    def __init__(self, config: MarketConfig):
        self.config = config
        self.price_engine = MarketPrice(config=config)
        self.flow_engine = OrderFlow(config=config)
        self.mm_engine = MarketMaker(config=config)
        self.perfor_engine = Performance(config=config)
        
        self.start_time = 0
        self.adverse_pnl = 0.0
        self.data_log = []
        
    def run(self):
        while self.start_time < self.config.total_time:
            old_mid = self.price_engine.mid_price
            mid_price = self.price_engine.StohasticsPrice()
            price_delta = mid_price - old_mid
            
            bid, ask = self.mm_engine.Quote(mid_price)
            side = 'NONE'
            event_tag = 'NONE'
            
            if self.flow_engine.PoissonGeneration():
                is_informed = self.flow_engine.TraderType()

                if is_informed:
                    side = 'buy' if price_delta > 0 else 'sell'
                    actual_impact = self.config.impact_score*3
                    event_tag = "TOXIC"
                else:
                    side = self.flow_engine.OrderSide()
                    actual_impact = self.config.impact_score*1
                    event_tag = "NOISE"
                    
                if side == 'buy':
                    delta = ask - mid_price
                else:
                    delta = mid_price - bid                    
                fill_prob = np.exp(-self.config.k * delta)
                
                if np.random.rand() < fill_prob:
                    self.mm_engine.ExecuteTrade(side, bid, ask)

                    impact_dir = 1 if side == 'buy' else -1
                    self.price_engine.mid_price += impact_dir * actual_impact

                    mid_price = self.price_engine.mid_price
                    
                    if is_informed:
                        if side == 'buy':
                            self.adverse_pnl -= price_delta
                        else:
                            self.adverse_pnl += price_delta
                else:
                    pass
            else:
                pass
            
            snapshot_dict = {
                'snapshot': self.start_time,
                'mid_price': mid_price,
                'bid': bid,
                'ask': ask,
                'PnL': self.mm_engine.update_pnl(mid_price),
                'Inventory': self.mm_engine.inventory,
                'Side': side.upper(),
                'Tag': event_tag,
                'Adverse_PnL': self.adverse_pnl
                  
            }
            
            self.data_log.append(snapshot_dict)
            self.start_time += self.config.dt

        data_log_df = pd.DataFrame(self.data_log)
        return data_log_df
    
if __name__ == '__main__':
    config = MarketConfig()
    sim = Simulator(config=config)
    result = Performance(config=config)
    
    data_log = sim.run()
    result.GraphPlot(data_log)
    result.Metrix(data_log)
    
# run_sim()