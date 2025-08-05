import pandas as pd
import numpy as np
import pymc3 as pm
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('data/raw/brent_oil_prices.csv')  # Updated path
data['Date'] = pd.to_datetime(data['Date'], format='%d-%b-%y')
data = data.sort_values('Date')
prices = data['Price'].values
dates = data['Date'].values
n = len(prices)

# Bayesian change point model
with pm.Model() as model:
    # Prior for switch point
    tau = pm.DiscreteUniform('tau', lower=0, upper=n-1)
    
    # Parameters before and after change point
    mu_1 = pm.Normal('mu_1', mu=np.mean(prices), sd=10)
    mu_2 = pm.Normal('mu_2', mu=np.mean(prices), sd=10)
    sigma = pm.HalfNormal('sigma', sd=10)
    
    # Switch function to select mean
    mu = pm.math.switch(tau >= np.arange(n), mu_1, mu_2)
    
    # Likelihood
    likelihood = pm.Normal('likelihood', mu=mu, sd=sigma, observed=prices)
    
    # MCMC sampling
    trace = pm.sample(2000, tune=1000, return_inferencedata=False)

# Check convergence
print(pm.summary(trace))
pm.plot_trace(trace)
plt.savefig('outputs/trace_plot.png')  # Updated path

# Extract change point
tau_posterior = trace['tau']
tau_mode = int(np.median(tau_posterior))
change_date = dates[tau_mode]
print(f"Most likely change point: {change_date}")

# Quantify impact
mu_1_posterior = trace['mu_1']
mu_2_posterior = trace['mu_2']
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
plt.savefig('outputs/tau_posterior.png')  # Updated path