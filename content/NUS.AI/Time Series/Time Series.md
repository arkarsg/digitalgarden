# Dates and time
- Data types for date & time information
- Represents *points in time* or *periods of time*
- As a `DataFrame` index → converts the entire `DataFrame` into a *time series*

## Basics
```python
import micropip
await micropip.install('numpy')
await micropip.install('pandas')
import numpy as np
import pandas as pd
from datetime import datetime
```

---

### `pd.Timestamp`
- Create a pandas Timestamp with `datetimte` object or a date `string`
- Day, year, months and weekdays are [attributes](Time%20Series.md#attributes)

```python
time_stamp = pd.Timestamp(datetime(2017, 1, 1))
print(time_stamp)
print(time_stamp.year)
print(time_stamp.day_name())
```

---

### `pd.Period`
- `Period` object has a [frequency](Time%20Series.md#frequencies)
- Defaults to month, can convert to daily

```python
period = pd.Period('2017-01') # Monthly by default

print(period)

# period.asfreq('D') # convert to daily

period = period + 2
print(period)
```

>[!note]
>`pd.Timestamp` can also perform date arithmetic

---


## Creating a sequence

### `pd.date_range`
- `start` : start datestamp
- `end` : end datestamp (optional)
- `periods` : Number of division
- `freq` : monthly or daily

```python
index = pd.date_range(start='2017-01-01', periods=12, freq='M')

print(index)
```

By retrieving an `index`, we obtain a `Timestamp`

```python
# Timestamp
print(index[0])
```

---

## Reference

### Frequencies
| **Period**    | **Alias** |
| ------------- | --------- |
| Hour          | H         |
| Day           | D         |
| Week          | W         |
| Month         | M         |
| Quarter       | Q         |
| Year          | A         |
| Business days | B          |

### Attributes
- `second`, `minute`, `hour`
- `day`, `month`, `quarter`, `year`
- `weekday`
- `dayofweek`
- `weekofyear`
- `dayofyear`

---

## Exercises

```python
# Create the range of dates here
seven_days = pd.date_range(start='2017-1-1', periods=7, freq='D')

# Iterate over the dates and print the number and name of the weekday
for day in seven_days:
	print(day.dayofweek, day.day_name())
```

---

# Indexing and Sampling

## Transformation
- Parsing `string` dates and convert to `datetime64` object
- Selecting and slicing for specific sub-periods
- Setting and changing `DateTimeIndex` frequency
	- **Upsampling** : Increasing the time frequency (need to generate new data)
	- **Downsampling** : Decreasing the time frequency (need to aggregate data)

Suppose we have a `date` column.
1. Parse the column with `pd.to_datetime()` to convert to `datetime64`
2. Turn `date` into index with `table.set_index(date, inplace=True)`

## Partial string indexing
Using string to represent *parts* of the date or a complete date, we can obtain relevant data. For example,
```python
table['2015'].info() # part of date

table['2015-3': '2016-2'].info() # slice includes last month

table.loc['2015-01-01', 'price'] # Use full date with .loc to obtain the price
```

## Setting frequency
- Set the frequency with `.asfreq()`

---
## Example
Given a `csv` file that has a column of `Object` dates,
1. Convert to `datetime64`
2. Convert to timeseries by setting the *date* column as index

```python
data = pd.read_csv('nyc.csv')

# Inspect data
print(data.info())

# Convert the date column to datetime64
data['date'] = pd.to_datetime(data['date'])

# Set date column as index
data.set_index('date', inplace=True)

# Inspect data
print(data.info())

# Plot data
data.plot(subplots=True)

plt.show()
```

---

Given a `DateTimeIndex` dataframe with a single column *price* and a list of *years* we are interested in,
1. Use `.loc` to slice the relevant years
2. Use `.reset_index()` to remove the DatetimeIndex
3. Rename the column *price* to appropriate *year*
4. `pd.concat` to combine yearly data with the data in *prices*
```python
# Create dataframe prices here
prices = pd.DataFrame()
# Select data for each year and concatenate with prices here
for year in ['2013', '2014', '2015']:
	price_per_year = yahoo.loc[year, ['price']].reset_index(drop=True)
	price_per_year.rename(columns={'price': year}, inplace=True)
	prices = pd.concat([prices, price_per_year], axis=1)

# Plot prices
prices.plot()
plt.show()
```

---

Given DataFrame of daily carbon monoxide concentration,
1. Resample the frequency

```python
# Inspect data
print(co.info())

# Set the frequency to calendar daily
co = co.asfreq('D')

# Plot the data
co.plot(subplots=True)
plt.show()

# Set frequency to monthly
co = co.asfreq('M')

# Plot the data
co.plot(subplots=True)
plt.show()
```

>[!note]
>There will be `NaN` values when `M` is used

---
# Calculations
Time series manipulations by
- shifting or lag values back or forward in time
- Get difference in value for a given time period
- Compute the percent change over any number of periods

---

## `shift()`
- Defaults to `periods=1`
- This shifts the column 1 period into the future

```python
# read google stock prices csv
# immediate parse `date` column and set as index column
google = pd.read_csv('google.csv', parse_dates=['date'], index_col='date')

# shifting operation
## This operation will result in a NaN at the first value
google['shifted'] = google.price.shift()

# lagging operation
## This operation will result in a NaN at the last value
google['lagged'] = google.price.shift(periods=-1)
```

### Rate of change
The *financial return*
$$
x_t / x_{t-1}
$$
is calculating the rate of change from period to period.

```python
google['change'] = google.price.div(google.shifted)
```
This is the relative change from the last price. In other words, a *factor* to multiply the previous price to obtain the current price.

---
## `diff()`
Difference in value for two adjacent periods
$$
x_t - x_{t-1}
$$

```python
google['diff'] = google.price.diff()

```
---
## `pct_change()`
Percentage change
- Call `mul(100)`

---
## Example
Given a `csv` file of `Date` and closing prices `Close`,
1. Plot `shifted` of 90 business days
2. Plot `lagged` of 90 business days

```python
# Import data here
google = pd.read_csv('google.csv', parse_dates=['Date'], index_col='Date')

# Set data frequency to business daily
google = google.asfreq("B")

# Create 'lagged' and 'shifted'
google['lagged'] = google.Close.shift(periods=-90)
google['shifted'] = google.Close.shift(periods=90)

# Plot the google price series
google.plot()
plt.show()
```

---

Given a `csv` file,

```python
# Created shifted_30 here
yahoo['shifted_30'] = yahoo.price.shift(30)

# Subtract shifted_30 from price
yahoo['change_30'] = yahoo.price.sub(yahoo.shifted_30)

# Get the 30-day price difference
yahoo['diff_30'] = yahoo.price.diff(30)

# Inspect the last five rows of price
print(yahoo.tail())

# Show the value_counts of the difference between change_30 and diff_30
print(yahoo.change_30.sub(yahoo.diff_30).value_counts())
```

---

- Percentage change between days, month and year
	- `mul(100)`
```python
# Create daily_return
google['daily_return'] = google.Close.pct_change(periods=1).mul(100)

# Create monthly_return
google['monthly_return'] = google.Close.pct_change(periods=30).mul(100)

# Create annual_return
google['annual_return'] = google.Close.pct_change(periods=360).mul(100)

# Plot the result
google.plot(subplots=True)
plt.show()
```