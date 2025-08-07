import pandas as pd
import numpy as np
import pymc as pm
import matplotlib.pyplot as plt
import os

# Ensure output directory exists
os.makedirs('D:/KAIM/oil_price_change_point_analysis/outputs', exist_ok=True)

# Load data
data = pd.read_csv('../data/raw/BrentOilPrices.csv')
data['Date'] = pd.to_datetime(data['Date'], format='mixed', dayfirst=True, errors='coerce')
data = data.dropna(subset=['Date']).sort_values('Date')
prices = data['Price'].values
dates = data['Date'].values
n = len(prices)

# Bayesian change point model
def define_model():
    with pm.Model() as model:
        # Prior for switch point
        tau = pm.DiscreteUniform('tau', lower=0, upper=n-1)
        
        # Parameters before and after change point
        mu_1 = pm.Normal('mu_1', mu=np.mean(prices), sigma=10)
        mu_2 = pm.Normal('mu_2', mu=np.mean(prices), sigma=10)
        sigma = pm.HalfNormal('sigma', sigma=10)
        
        # Switch function to select mean
        mu = pm.math.switch(tau >= np.arange(n), mu_1, mu_2)
        
        # Likelihood
        likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=prices)
        
        return model

if __name__ == '__main__':
    # Define and sample model
    model = define_model()
    with model:
        trace = pm.sample(200, tune=200, return_inferencedata=True)

    # Check convergence
    print(pm.summary(trace))
    pm.plot_trace(trace)
    plt.savefig('../outputs/trace_plot.png')
    plt.close()

    # Extract change point
    tau_posterior = trace.posterior['tau'].values.flatten()
    tau_mode = int(np.median(tau_posterior))
    change_date = dates[tau_mode]
    print(f"Most likely change point: {change_date}")

    # Quantify impact
    mu_1_posterior = trace.posterior['mu_1'].values.flatten()
    mu_2_posterior = trace.posterior['mu_2'].values.flatten()
    mean_shift = np.mean(mu_2_posterior - mu_1_posterior)
    print(f"Mean price shift: ${mean_shift:.2f}")

    # Plot posterior of tau
    plt.figure(figsize=(12, 6))
    plt.hist(tau_posterior, bins=50, density=True)
    plt.axvline(tau_mode, color='red', linestyle='--', label=f'Change Point: {change_date}')
    plt.title('Posterior Distribution of Change Point')
    plt.xlabel('Time Index')
    plt.ylabel('Density')
    plt.legend()
    plt.savefig('../outputs/tau_posterior.png')
    plt.close()