Comparing [Time Series](Time%20Series.md) and growth rates

- Stock performance — normalise price series to start at 100

1. Divide all the prices by first in series, multiply by 100
2. Standardises the starting point
3. All points are relative to the starting point
4. Difference to starting point in percentage points

---

# Normalizing
1. Select the column and `iloc` to get the first price
2. Divide the price series by the first price and multiply by 100

```python
# Import data here
prices = pd.read_csv('asset_classes.csv', parse_dates=['DATE'], index_col='DATE')

# Inspect prices here
print(prices.info())

# Select first prices
first_prices = prices.iloc[0]
print(first_prices)

# Create normalized
normalized = prices.div(first_prices).mul(100)

# Plot normalized
normalized.plot()
plt.show()
```

# Frequency
Changing the frequency of time series into a common frequency
- Frequency affects the data
	- **Upsampling** — need to handle missing data
	- **Downsampling** — aggregate existing data

## Interpolation
- `ffill` — forward fill, propagates value into the future if it contains NaN
- `bfill` — backward fill, propagates value into the past if it contains NaN
- `fill_value` — provide a fill value
- `reindex()`

```python
# Set start and end dates
start = '2016-1-1'
end = '2016-2-29'

# Create monthly_dates here
monthly_dates = pd.date_range(start=start, end=end, freq='M')

# Create and print monthly here
monthly = pd.Series(data=[1,2], index=monthly_dates)
print(monthly)

# Create weekly_dates here
weekly_dates = pd.date_range(start=start, end=end, freq='W')

# Print monthly, reindexed using weekly_dates
print(monthly.reindex(weekly_dates))
print(monthly.reindex(weekly_dates, method='bfill'))
print(monthly.reindex(weekly_dates, method='ffill'))
```

---

## Creating weekly and monthly data

Suppose we have a `csv` file of unemployment data.
1. Read the `csv` file and set `date` column as the index
2. Convert to weekly series and use `bfill` or `ffill` to interpolate the data
3. Use `loc` to slice the data

```python
# Import data here
data = pd.read_csv('unemployment.csv', parse_dates=['date'], index_col='date')

# Show first five rows of weekly series
print(data.asfreq('W').head())

# Show first five rows of weekly series with bfill option
print(data.asfreq(freq='W', method='bfill').head())

# Create weekly series with ffill option and show first five rows
weekly_ffill = data.asfreq(freq='W', method='ffill')
print(weekly_ffill.head())

# Plot weekly_fill starting 2015 here
weekly_ffill.loc['2015':].plot()
plt.show()
```