# Algorithmic Strategy Backtester

A Python-based backtesting framework for evaluating equity trading strategies on historical market data. This project enables user to implement, test, and compare multiple strategies.

## Features

- **Multiple Strategies**:
  - Exponential Moving Average (EMA) Crossover
  - Bollinger Bands
  - Moving Average Volume
- **Dynamic Parameter Tuning**: Test strategies with customizable parameters for optimized performance.
- **Data Integration**: Retrieves historical market data using the [yfinance](https://github.com/ranaroussi/yfinance) library.
- **Performance Metrics**:
  - Total Return
  - Adjusted Return (relative to market performance)
  - Compound Annual Growth Rate (CAGR)
- **Visualizations**:
  - Stock price with buy/sell signals
  - Strategy performance over time

## Requirements

This project requires Python 3.9+ and the following libraries:
- `pandas`
- `numpy`
- `matplotlib`
- `yfinance`

Install the dependencies using:
```bash
pip install -r requirements.txt
```

## Usage

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Run the main script:
   ```bash
   python evaluate_strategies.py
   ```

3. Customize the `strategies` dictionary in `evaluate_strategies.py` to test your own parameter combinations.

## Example Output

The project evaluates strategies over a 5-year period and provides the following metrics:

```
Total Returns, Adjusted Returns, and Aggregated 5-Year CAGR:
EMA Crossover:
  Total Return: 79.67%
  5-Year CAGR: 10.54%
  Adjusted Return (Above Market): 2.03%
  Adjusted 5-Year CAGR: 2.03%
Bollinger Bands:
  Total Return: 42.30%
  5-Year CAGR: 6.50%
  Adjusted Return (Above Market): -3.70%
  Adjusted 5-Year CAGR: -1.20%
```

The framework also visualizes the results:
1. **Cumulative Strategy Performance**:
   - Line plots showing % gains for each strategy.
2. **Buy/Sell Signal Visualization**:
   - Stock price chart annotated with buy/sell signals for each strategy.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request for improvements.
## Acknowledgments

- Historical data provided by [yfinance](https://github.com/ranaroussi/yfinance).
- Strategy inspiration from various quantitative trading resources.

##  Future plans
-  Will add more strategies including the use of lag embedding, ML models like XGBoost, hybrid models, etc.

