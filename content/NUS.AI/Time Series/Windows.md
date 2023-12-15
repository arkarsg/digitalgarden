# Rolling window
- Useful to operate in sub periods of time series
- Calculate metrics for sub periods inside the window
- Create a new time series of metrics

1. Rolling window
	1. Same size and sliding
2. Expanding window
	- Contain all prior data

```python
# window size = 30 calendar days (preceding)
data.rolling(window='30D').mean()
# aggregate method
data.price.rolling('90D').agg(['mean', 'std'])
```

---

## Examples

### Finding the rolling mean
- Find the rolling mean over different windows of a specified column

```python
# Import and inspect ozone data here
data = pd.read_csv('ozone.csv', parse_dates=['date'], index_col='date')
print(data.info())
# Calculate 90d and 360d rolling mean for the last price
data['90D'] = data['Ozone'].rolling(window='90D').mean()
data['360D'] = data['Ozone'].rolling(window='360D').mean()
# Plot data
data.loc['2010':].plot(title='New York City')
plt.show()
```

### Using `agg` method
```python
# Import and inspect ozone data here
data = pd.read_csv('ozone.csv', parse_dates=['date'], index_col='date').dropna()
print(data.info())
# Calculate the rolling mean and std here
rolling_stats = data.Ozone.rolling(window=360).agg(['mean', 'std'])
# Join rolling_stats with ozone data
stats = data.join(rolling_stats)
# Plot stats
stats.plot(subplots=True)
plt.show()
```

### Finding the quantiles
1. Resample the data into suitable time frequency
2. Create rolling window
3. Find the rolling quantiles

```python
# Import and inspect ozone data here
data = pd.read_csv('ozone.csv', parse_dates=['date'], index_col='date').dropna()
print(data.info())
# Calculate the rolling mean and std here
rolling_stats = data.Ozone.rolling(window=360).agg(['mean', 'std'])
# Join rolling_stats with ozone data
stats = data.join(rolling_stats)
# Plot stats
stats.plot(subplots=True)
plt.show()
```

---

# Expanding window
- Calculate metrics for periods up to current date
- New time series reflects all historical values up to that date
- Useful for running rate of return, running min/ max

>[!note] 
>Calling `expanding` followed by `sum` is essentially `cumsum`

## Running return
- **Single period return** : current price over last price minus 1
$$
r_t = \frac{P_t}{P_{t-1}} - 1
$$

>[!note]
>This is also the `pct_change`

- **Multi-period return** : product of $(1+ r_t)$ from $t = 1$ to $t = T$, minus 1
$$
R_t = (1+r_1)(1+r_2) ... (1+r_T) - 1
$$

```python
pr = data.SP500.pct_change() # period return
pr_plus_one = pr.add(1)
cumulative_return = pr_plus_one.cumprod().sub(1) # multi-period return
```

```python
def multi_period_return(period_returns):
	return np.prod(period_returns + 1) - 1
```

---

## Examples
```python
# Define your investment
investment = 1000

# Calculate the daily returns here
returns = data.pct_change()

# Calculate the cumulative returns here
returns_plus_one = returns.add(1)
cumulative_return = returns_plus_one.cumprod()

# Calculate and plot the investment return here
cumulative_return.mul(investment).plot()
plt.show()
```

```python
# Import numpy
import numpy as np

# Define a multi_period_return function
def multi_period_return(period_returns):
	return np.prod(period_returns + 1) - 1
# Calculate daily returns
daily_returns = data.pct_change()
# Calculate rolling_annual_returns
rolling_annual_returns = daily_returns.rolling('360D').apply(multi_period_return)
# Plot rolling_annual_returns
rolling_annual_returns.mul(100).plot()
plt.show()
```

---

# Case study
Models to predict daily stock are assumed to be random in nature
- `Numpy` generate random numbers
- From random returns to prices, use `cumprod()`

There are 2 methods
1. Generate random number normally
2. Randomly select SP500 price

```python
# Set seed here

seed(42)

# Create random_walk
random_walk = normal(loc=0.001, scale=0.01, size=2500)

# Convert random_walk to pd.series
random_walk = pd.Series(random_walk)
# Create random_prices
random_prices = random_walk.add(1).cumprod()
# Plot random_prices here
random_prices.mul(1000)[1000:].plot()
plt.show()
```

```python
# Set seed here
seed(42)
# Calculate daily_returns here
daily_returns = fb.pct_change().dropna()
# Get n_obs
n_obs = daily_returns.count()
# Create random_walk
random_walk = choice(daily_returns, size=n_obs)
# Convert random_walk to pd.series
random_walk = pd.Series(random_walk)
# Plot random_walk distribution
sns.distplot(random_walk)
plt.show()
```

```python
# Select fb start price here
start = fb.price.first('D')
# Add 1 to random walk and append to start
random_walk = random_walk.add(1)
random_price = start.append(random_walk)
# Calculate cumulative product here
random_price = random_price.cumprod()
# Insert into fb and plot
fb['random'] = random_price
fb.plot()
plt.show()
```

----

