import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from Config import MarketConfig

class Performance:
    def __init__(self, config: MarketConfig):
        self.config = config
        
    def Metrix(self, df):

        df['Tick_Returns'] = df['PnL'].diff().fillna(0)
        
        final_pnl = df['PnL'].iloc[-1]
        final_adverse = df['Adverse_PnL'].iloc[-1]
        
        rolling_peak = df['PnL'].cummax()
        drawdowns = rolling_peak - df['PnL']
        max_drawdown = drawdowns.max()
        
        mean_tick_return = df['Tick_Returns'].mean()
        std_tick_return = df['Tick_Returns'].std()
        
        downside_ticks = df['Tick_Returns'][df['Tick_Returns'] < 0]
        std_downside_tick = downside_ticks.std() if len(downside_ticks) > 0 else 0

        path_scaling = np.sqrt(len(df))
        
        if std_tick_return > 0:
            # Session-normalized Sharpe Ratio
            stable_sharpe = (mean_tick_return / std_tick_return) * path_scaling
            # Standard high-frequency information ratio format:
            hf_info_ratio = (mean_tick_return / std_tick_return) 
        else:
            stable_sharpe = 0.0
            hf_info_ratio = 0.0
            
        if std_downside_tick > 0:
            stable_sortino = (mean_tick_return / std_downside_tick) * path_scaling
        else:
            stable_sortino = 0.0
            
        calmar = (final_pnl / max_drawdown) if max_drawdown > 0 else 0
        inventory_turns = df['Inventory'].diff().abs().sum()

        # Print the normalized dashboard
        print(f"Final Gross PnL:         ${final_pnl:,.2f}")
        print(f"Max Drawdown:   ${max_drawdown:,.2f}")
        print("-" * 50)
        print(f"Stable Sharpe:    {stable_sharpe:.4f}")
        print(f"Stable Sortino:   {stable_sortino:.4f}")
        print(f"Information Ratio: {hf_info_ratio:.6f} (Per-tick edge)")
        print(f"Calmar Ratio:             {calmar:.4f}")
        print(f"Total Inventory Turns:    {inventory_turns:.0f}")
    
    def GraphPlot(self, df):
        plt.figure(figsize=(10, 8))
        
        plt.subplot(3,1,1)
        plt.plot(df['mid_price'], alpha=0.7, color='blue', label='Mid Price')
        plt.axhline(y=100, color='green', linestyle='--', alpha=0.5, label='Start Price')
        plt.title("Market Making Mid-Price Simulation (Arithmetic)")
        plt.xlabel("Time Steps")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.subplot(3,1,2)
        plt.plot(df['PnL'], color='green', linewidth=2, label='Mark-to-Market PnL')
        plt.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Breakeven Baseline')
        plt.title("Market Making Strategy Performance Equity Curve", fontsize=12, fontweight='bold')
        plt.xlabel("Simulation Ticks / Time Steps")
        plt.ylabel("Total Wealth Value ($)")
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(loc='upper left')
        
        plt.subplot(3,1,3)
        plt.plot(df['Inventory'], color='crimson', alpha=0.5)
        plt.title('Inventory Skew and Risk Management')
        plt.xlabel("Time Steps")
        plt.ylabel("Inventory")
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()

        plt.savefig("figures/perfor.png", dpi=300, bbox_inches="tight")
        plt.show()