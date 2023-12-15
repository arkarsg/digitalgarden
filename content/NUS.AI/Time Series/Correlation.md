# Relationship between time series
- Linear relationship between variables
- Important for prediction and risk management

## Correlation
**Correlation coefficient** : how similar is the pairwise movement of two variables around their *averages*
- Varies between $[-1, 1]$

![correlation|500](Screenshot%202023-12-12%20at%2012.36.01%20PM.png)

---

```python
# Inspect data here
print(data.info())
# Calculate year-end prices here
annual_prices = data.resample('A').last()
# Calculate annual returns here
annual_returns = annual_prices.pct_change()
# Calculate and print the correlation matrix here
correlations = annual_returns.corr()
print(correlations)
# Visualize the correlations as heatmap here
sns.heatmap(correlations, annot=True)
plt.show()
```

![heatmap|400](Unknown%20(2).svg)