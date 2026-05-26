# **Market Making & Adverse Selection Simulator**

A Python-based market making simulation framework designed to study inventory risk, adverse selection, toxic order flow, and dynamic spread management under stochastic market conditions.

This project explores how market makers balance spread capture against inventory exposure while interacting with informed and uninformed flow in a simplified electronic market environment.

# **Project Motivation**

Modern electronic market makers continuously provide bid and ask liquidity while managing several competing risks:

- Adverse selection from informed traders
- Inventory accumulation
- Volatility shocks
- Toxic order flow persistence
- Execution uncertainty

The goal of this project was to build a simplified simulation environment to study how these factors influence quoting behavior and profitability.

# **🟢Core Features**

## **Stochastic Mid-Price Dynamics**

- Simulated arithmetic price process using Brownian-style random movement
- Configurable volatility, drift, and time discretization

## **Order Flow Generation**

- Poisson arrival process for market orders
- Persistent order flow modeling
- Toxic vs noise trader classification

## **Market Making Engine**

- Dynamic bid/ask quoting
- Inventory-skewed reservation pricing
- Spread widening under elevated toxicity conditions
- Tick-size discretization

## **Adverse Selection Modeling**

- Toxic informed traders generate directional price impact
- Simulated post-trade markouts
- Spread capture vs adverse selection trade-off analysis

## **Risk & Performance Tracking**

- Mark-to-market PnL tracking
- Inventory exposure monitoring
- Equity curve visualization

# **🟡Model Structure**

## **Price Process**

The mid-price evolves according to:


### $dS_t = \mu dt + \sigma \sqrt{dt}\epsilon_t$


Where:

- $\mu = drift$
- $\sigma = volatility$
- $\epsilon_t \sim N(0,1)$

## **Inventory-Skewed Quoting**

The market maker adjusts reservation prices based on inventory exposure:


### $r_t = S_t - \gamma q_t$


Where:

- $S_t = current mid-price$
- $q_t = inventory position$
- $\gamma = inventory risk aversion coefficient$

This discourages excessive directional inventory accumulation.

## **Dynamic Spread Adjustment**

Quoted spread widens under elevated toxicity conditions:

### $Spread_t = BaseSpread \times (1 + \kappa \hat{\alpha})$


Where:

- $\hat{\alpha} = estimated recent order flow toxicity$
- $\kappa = toxicity sensitivity parameter$

## **Simulation Components**

| **Component** | **Description** |
| --- | --- |
| MarketPrice | Simulates stochastic mid-price dynamics |
| OrderFlow | Generates market order arrivals |
| MarketMaker | Handles quoting, inventory, and PnL |
| Simulator | Runs full market interaction loop |

## **Example Simulation Output**

The simulator tracks:

- Mid-price evolution
- Inventory accumulation
- Mark-to-market PnL
- Toxic flow events
- Spread adjustment behavior

Example observations:

- Elevated toxic flow widens quoted spreads
- Persistent order flow increases inventory imbalance risk
- Adverse selection can dominate spread capture under informed flow regimes

## **Technologies Used**

- Python
- NumPy
- Matplotlib
- Dataclasses

## **Future Improvements**

Potential extensions include:

- Multi-level order book simulation
- Hawkes-process order arrivals
- Queue position modeling
- Reinforcement learning inventory control
- Volatility regime switching
- Real exchange data calibration
