import numpy as np
from dataclasses import dataclass

@dataclass
class MarketConfig:
    start_price: float = 100.0
    drift: float = 0.0
    base_vol: float = np.random.normal(0.1,0.4)
    dt: float = 0.1
    total_time: int = 1000
        
    lambda_poisson: float = 15
    order_persistence: float = 0.7
    impact_score: float = 0.1
        
    tick: float = 0.01
    spread: float = 0.2
    quote_size: int = 1
    inventory_gamma: float = 0.01
        
    toxicity_alpha: float = 0.35
    kappa: float = 3
    k: float = 8