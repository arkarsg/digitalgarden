---
title: Time Series in Pandas
---

# Topics

1. [Time Series](Time%20Series.md)
2. [Growth Rates](Growth%20Rates.md)
3. [Resample](Resample.md)
4. [Windows](Windows.md)
5. [Correlation](Correlation.md)

---

# Case study:
- Measure *aggregate* stock performance

We want to build an *index* that will be composed of several stock prices.
1. Each component of the index will be weighted by its market capitalization
2. Companies with larger weight → price changes will have a larger impact on the index performance

>[!note]
>- **Market capitalization** : Value of all the stocks of a company
> $$
> n \times p_s
> $$
> 
> - **Value weighted index** : Each stock is weighted by the value of the company on the stock market 


## Building a cap-weighted index
1. Construct value-weighted index
	- Select the *largest* company from each sector as *index* components
	- Get number of shares and stock prices
	- Calculate component weights

Suppose I have a combined listing of NYSE, NASDAQ and AMEX, with a `Market Captialization` column.

The dataframe has the following columns:

```plain text
<class 'pandas.core.frame.DataFrame'> 
RangeIndex: 6674 entries, 0 to 6673 Data columns (total 8 columns):
#     Column     Non-Null Count     Dtype
---   ------     --------------     -----
0    Exchange    6674 non-null      object
1   Stock Symbol 6674 non-null      object
2   Company Name 6674 non-null      object
3    Last Sale   6590 non-null      float64
4  Market Capitalization 6674 non-null float64
5   IPO Year     2852 non-null     float64
6   Sector       5182 non-null     object 
7  Industry      5182 non-null     object
dtypes: float64(3), object(5)
memory usage: 417.2+ KB
None
```

### Cleaning the data

```python
# Inspect listings
print(listings.info())

# Move 'stock symbol' into the index
listings.set_index('Stock Symbol', inplace=True)
# Drop rows with missing 'sector' data
listings.dropna(subset=['Sector'], inplace=True)
# Select companies with IPO Year before 2019
listings = listings[listings['IPO Year'] < 2019]
# Inspect the new listings data
print(listings.info())
# Show the number of companies per sector
print(listings.groupby('Sector').size().sort_values(ascending=False))
```

### Selecting index components
```python
# Select largest company for each sector
components = listings.groupby(['Sector'])['Market Capitalization'].nlargest(1)

# Print components, sorted by market cap
print(components.sort_values( ascending=False))

# Select stock symbols and print the result
tickers = components.index.get_level_values('Stock Symbol')
print(tickers)

# Print company name, market cap, and last price for each component
info_cols = ['Company Name', 'Market Capitalization', 'Last Sale']
print(listings.loc[tickers, info_cols].sort_values(by='Market Capitalization', ascending=False))
```

### Importing index component price information
```python
# Print tickers
print(tickers)
# Import prices and inspect result
stock_prices = pd.read_csv('stock_prices.csv', parse_dates=['Date'], index_col='Date')
print(stock_prices.info())

# Calculate the returns
price_return = stock_prices.iloc[-1].div(stock_prices.iloc[0]).sub(1).mul(100)

# Plot horizontal bar chart of sorted price_return
price_return.sort_values().plot(kind='barh', title='Stock Price Returns')
plt.show()
```

### Finding companies with the most shares
```python
# Inspect listings and print tickers
print(listings.info())
print(tickers)

# Select components and relevant columns from listings
components = listings.loc[tickers, ['Market Capitalization', 'Last Sale']]

# Print the first rows of components
print(components.head(5))

# Calculate the number of shares here
no_shares = components['Market Capitalization'].div(components['Last Sale'])

# Print the sorted no_shares
print(no_shares.sort_values(ascending=False))
```

### Time series of market value
```python
# Select the number of shares
no_shares = components['Number of Shares'].sort_values()
print(no_shares)
# Create the series of market cap per ticker
market_cap = stock_prices.mul(no_shares)
# Select first and last market cap here
first_value = market_cap.iloc[0]
last_value = market_cap.iloc[-1]
# Concatenate and plot first and last market cap here
pd.concat([first_value, last_value], axis=1).plot(kind='barh')
plt.show()
```

### Calculating the composite index
```python
# Aggregate and print the market cap per trading day
raw_index = market_cap_series.sum(axis=1)
print(raw_index)
# Normalize the aggregate market cap here
index = raw_index.div(raw_index[0]).mul(100)
print(index)
# Plot the index here
index.plot(title='Market-Cap Weighted Index')
plt.show()
```

---

## Evaluation
1. Index return and contribution of each component to the result
2. Compare to benchmark that is also value weighted
	1. Total period return
	2. Rolling returns of a sub-period

---

## 
