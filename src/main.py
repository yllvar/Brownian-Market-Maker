import math
import numpy as np
import ccxt
import matplotlib.pyplot as plt
from scipy.stats import norm

# KuCoin API keys
API_KEY = 'your_api_key'
SECRET_KEY = 'your_secret_key'
PASSPHRASE = 'your_passphrase'

class AvellanedaStoikovMarketMaker:
    def __init__(self, symbol='BTC/USDT'):
        self.symbol = symbol
        self.exchange = ccxt.kucoin({
            'apiKey': API_KEY,
            'secret': SECRET_KEY,
            'password': PASSPHRASE,
            'enableRateLimit': True
        })
        
    def simulate(self, n_sim=100):
        pnl_sim = np.empty((n_sim,))
        
        for i_sim in range(n_sim):
            # Parameters
            sigma = 2.0  # volatility
            T = 1.0  # total time
            N = 200  # number of steps
            dt = T / N  # time step
            
            # Initial conditions
            s = np.empty((N+1,))
            s[0] = 100.0  # initial stock price
            
            # Brownian motion simulation
            for n in range(N):
                s[n+1] = s[n] + 0.1 * n + sigma * np.sqrt(dt) * np.random.normal()
            
            # Initialize variables
            pnl = np.zeros((N+2,))
            x = np.zeros((N+2,))
            q = np.zeros((N+2,))
            q_max = 10
            gamma = 0.1
            k = 1.5
            
            r = np.zeros((N+1,))
            ra = np.zeros((N+1,))
            rb = np.zeros((N+1,))
            
            M = s[0] / 200.0
            A = 1.0 / dt / math.exp(k * M / 2.0)
            
            max_q_held = 0
            min_q_held = 0
            
            for n in range(N+1):
                s[n] += 0.1 * n  # stock price trend
                
                # Reserve price and spread
                r[n] = s[n] - q[n] * gamma * sigma**2 * (T - dt * n)
                r_spread = 2.0 / gamma * math.log(1 + gamma / k)
                ra[n] = r[n] + r_spread / 2.0
                rb[n] = r[n] - r_spread / 2.0
                
                # Calculate deltas and intensities
                delta_a = ra[n] - s[n]
                delta_b = s[n] - rb[n]
                lambda_a = A * math.exp(-k * delta_a)
                lambda_b = A * math.exp(-k * delta_b)
                
                # Order execution probability
                ya = np.random.random()
                yb = np.random.random()
                
                dNa = 1 if ya < (1 - np.exp(-lambda_a * dt)) else 0
                dNb = 1 if yb < (1 - np.exp(-lambda_b * dt)) else 0
                
                # Update inventory and cash
                q[n+1] = q[n] - dNa + dNb
                x[n+1] = x[n] + ra[n] * dNa - rb[n] * dNb
                pnl[n+1] = x[n+1] + q[n+1] * s[n]
                
                if q[n+1] > max_q_held:
                    max_q_held = q[n+1]
                if q[n+1] < min_q_held:
                    min_q_held = q[n+1]
            
            pnl_sim[i_sim] = pnl[-1]
        
        # Print and plot results
        print("Last simulation results:\n")
        print("Final inventory hold: ", q[-1])
        print("Last price: ", s[-1])
        print("Cash: ", x[-1])
        print("Final wealth: ", pnl[-1])
        print("Max q held: ", max_q_held)
        print("Min q held: ", min_q_held)
        
        f = plt.figure(figsize=(15, 4))
        f.add_subplot(1, 3, 1)
        t = np.linspace(0.0, T, N+1)
        plt.plot(t, s, color='black', label='Mid-market price')
        plt.plot(t, r[:-1], color='blue', linestyle='dashed', label='Reservation price')
        plt.plot(t, ra[:-1], color='red', linestyle='', marker='.', label='Price asked', markersize='4')
        plt.plot(t, rb[:-1], color='lime', linestyle='', marker='o', label='Price bid', markersize='2')
        plt.xlabel('Time', fontsize=16)
        plt.ylabel('Price [USD]', fontsize=16)
        plt.grid(True)
        plt.legend()
        
        f.add_subplot(1, 3, 2)
        plt.plot(t, pnl[:-1], color='black', label='P&L')
        plt.xlabel('Time', fontsize=16)
        plt.ylabel('PnL [USD]', fontsize=16)
        plt.grid(True)
        plt.legend()
        
        f.add_subplot(1, 3, 3)
        plt.plot(t, q[:-1], color='black', label='Stocks held')
        plt.xlabel('Time', fontsize=16)
        plt.ylabel('Inventory', fontsize=16)
        plt.grid(True)
        plt.legend()
        
        plt.show()
        
        print("\nParameters used in simulations:\n")
        print("gamma: %.3f" % gamma)
        print("k: %.3f" % k)
        print("sigma: %.3f" % sigma)
        print("T: %.2f" % T)
        print("n steps: %d" % N)
        
        print("\nResults over: %d simulations\n" % n_sim)
        print("Average PnL: %.2f" % np.mean(pnl_sim))
        print("Standard deviation PnL: %.2f" % np.std(pnl_sim))
        
        range_min = int(np.min(pnl_sim) - abs(np.min(pnl_sim)))
        range_max = int(np.max(pnl_sim) + abs(np.min(pnl_sim)))
        
        plt.hist(pnl_sim, bins=range_max - range_min, range=(range_min, range_max))
        plt.xlabel('PnL', fontsize=16)
        plt.ylabel('Frequency', fontsize=16)
        plt.show()

# Example usage
if __name__ == '__main__':
    mm_simulator = AvellanedaStoikovMarketMaker(symbol='BTC/USDT')
    mm_simulator.simulate(n_sim=100)
