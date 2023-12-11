---
title: Resampling
---

# Resampling
- Groups data within resampling period and applies one or several methods to each group
- Takes the value from the method and assigns a new date within the resampling period
- New date determined by *offset*
---
# Upsampling

Suppose we have a monthly data and wish to convert to weekly.
Here, we are *upsampling*.

```python
# Inspect data here
print(monthly.info())

# Create weekly dates
weekly_dates = pd.date_range(start=monthly.index.min(), end=monthly.index.max(), freq='W')

# Reindex monthly to weekly data
weekly = monthly.reindex(weekly_dates)

# Create ffill and interpolated columns
weekly['ffill'] = weekly.UNRATE.ffill()
weekly['interpolated'] = weekly.UNRATE.interpolate()

# Plot weekly
weekly.plot()
plt.show()
```

![resample|300](Unknown.svg)

---

## Interpolation
Suppose we have a `csv` file with *Debt/GDP* and *Unemployment* columns with `DateTime` index.
1. *Debt/GDP* has lower number of entires as it is reported quarterly
2. Therefore, we need to interpolate some data

```python
# Import & inspect data here
data = pd.read_csv('debt_unemployment.csv', parse_dates=['date'], index_col='date')
print(data.info())
## 89 entries of unemployment, 29 entries of debt/gdp

# Interpolate and inspect here
interpolated = data.interpolate()
print(interpolated.info())

# Plot interpolated data here
interpolated.plot(secondary_y='Unemployment')
plt.show()
```
![unemployment|300](Unknown%20(1).svg)

---

# Downsampling
- Also known as *aggregation*
- From decreasing the frequency of the time series
	- Converting *hour* to *day*
	- Converting *day* to *month*
- Choice of representing the new value
	- Mean, median, last value

```python
# Import and inspect data here
ozone = pd.read_csv('ozone.csv', parse_dates=['date'], index_col='date')
print(ozone.info())

# Calculate and plot the weekly average ozone trend
weekly = ozone.resample('W').mean()
weekly.plot()
plt.show()

# Calculate and plot the monthly average ozone trend
monthly = ozone.resample('M').mean()
monthly.plot()
plt.show()

# Calculate and plot the annual average ozone trend
annual = ozone.resample('A').mean()
annual.plot()

plt.show()
```

---

The following `csv` has 504 stock entries from 2015 to 2016.
We are interested in *monthly* trends.
1. Downsampling aggregates data with `mean`
```python
# Import and inspect data here
stocks = pd.read_csv('stocks.csv', parse_dates=['date'], index_col='date')
print(stocks.info())

# Calculate and plot the monthly averages
monthly_average = stocks.resample('M').mean()
monthly_average.plot(subplots=True)
plt.show()
```

---

Suppose we have `gdp_growth` reported quarterly and stock prices
1. Resample `djia` to `QS` (quarter start)
2. Aggregate with `first`

```python
# Import and inspect gdp_growth here
gdp_growth = pd.read_csv('gdp_growth.csv', parse_dates=['date'], index_col='date')
gdp_growth.info()

# Import and inspect djia here
djia = pd.read_csv('djia.csv', parse_dates=['date'], index_col='date')
djia.info()

# Calculate djia quarterly returns here
djia_quarterly = djia.resample('QS').first()
djia_quarterly_return = djia_quarterly.pct_change().mul(100)

# Concatenate, rename and plot djia_quarterly_return and gdp_growth here
data = pd.concat([gdp_growth, djia_quarterly_return], axis=1)

data.columns = ['gdp', 'djia']
data.plot()
plt.show()
```

---
Suppose we wish to use different aggregation methods
```python
# Import data here
sp500 = pd.read_csv('sp500.csv', parse_dates=['date'], index_col='date')
sp500.info()

# Calculate daily returns here
daily_returns = sp500.squeeze().pct_change()

# Resample and calculate statistics
stats = daily_returns.resample('M').agg(['mean', 'median', 'std'])

# Plot stats here
stats.plot()
plt.show()
```