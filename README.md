# Brownian-Market-Maker
Adapting Avellaneda &amp; Stoikov market making using ccxt for KuCoin

Influced by this repo: https://github.com/fedecaccia/avellaneda-stoikov

# Avellaneda-Stoikov Market Making Simulation

This project implements a simulation of high-frequency trading using the Avellaneda-Stoikov market-making model. The simulation utilizes Brownian motion to model stock price dynamics and implements market-making strategies to manage inventory and optimize profit.

## Components

### 1. `main.py`

This is the main script that orchestrates the simulation. It initializes the market maker, simulates trading scenarios, and visualizes the results using Matplotlib.

### 2. `brownian.py`

Contains the implementation of the Brownian motion simulation, which is essential for modeling stock price movements over time.

### 3. `brownian_path.py`

Provides an example of generating a single realization of Brownian motion and plotting it using Matplotlib. This can be useful for understanding the stochastic process used in the simulation.

### 4. `requirements.txt`

Lists all the Python libraries and their versions required to run the project. Use `pip install -r requirements.txt` to install them.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/avellaneda-stoikov-market-making.git
   cd avellaneda-stoikov-market-making
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Simulation

To run the simulation with default settings (symbol: BTC/USDT, 100 simulations):

```bash
python main.py
```

### Customizing the Simulation

You can customize the simulation by modifying parameters in `main.py`:

- Adjust `n_sim` in `simulate()` method to change the number of simulations.
- Modify parameters such as `sigma`, `T`, `N`, `dt`, `gamma`, `k` in the `simulate()` method to explore different scenarios.

### Visualizing Brownian Motion

To visualize a single realization of Brownian motion:

```bash
python brownian_path.py
```

This will plot the path of Brownian motion over a specified time interval.

## Results

The simulation results include:

- Final inventory held
- Last price observed
- Cash balance
- Final wealth (cash + inventory value)
- Maximum and minimum inventory held during the simulation
- Average and standard deviation of Profit and Loss (PnL) across simulations

## Parameters

The parameters used in the simulations can be found and adjusted in `main.py`. These include:

- `sigma`: Volatility of the stock
- `T`: Total time period of simulation
- `N`: Number of steps in the simulation
- `dt`: Time step size
- `gamma`: Risk factor influencing bid/ask spread
- `k`: Market model parameter influencing intensity of order placement

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Federico Caccia https://github.com/fedecaccia/avellaneda-stoikov
- Marco Avellaneda & Sasha Stoikov for their pioneering work on market making models.
- Open-source libraries: CCXT, NumPy, Matplotlib, and SciPy and ChatGPT 
