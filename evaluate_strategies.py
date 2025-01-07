import pandas as pd
import matplotlib.pyplot as plt
from strategies import ema_crossover_strategy, bollinger_bands_strategy, moving_average_volume_strategy
from data_loader import download_data


def backtest_strategy(data, strategy_function, **kwargs):
    signal_indices = strategy_function(data, **kwargs)

    trades = []
    bought_in = False
    buy_idx = None

    for idx in signal_indices:
        signal_value = data.loc[idx, 'signal']

        if signal_value == 1 and not bought_in:
            buy_idx = idx
            bought_in = True
        elif signal_value == -1 and bought_in:
            sell_idx = idx
            trades.append((buy_idx, sell_idx))
            bought_in = False

    results = []
    for buy_idx, sell_idx in trades:
        buy_price = data.loc[buy_idx, f'Close_{ticker}']
        sell_price = data.loc[sell_idx, f'Close_{ticker}']
        
        gain = ((sell_price - buy_price) / buy_price) * 100
        results.append(gain)

    return results, trades

def plot_results(results_dict, data, trades_dict, ticker):
    # Plot % gains for each strategy
    plt.figure(figsize=(10, 6))
    for strategy, gains in results_dict.items():
        plt.plot(gains, label=f"{strategy} (% Gains)")

    plt.xlabel("Trade Number")
    plt.ylabel("% Gain")
    plt.title("Strategy Performance")
    plt.legend()
    plt.show()

    # Plot stock price with buy/sell signals
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data[f'Close_{ticker}'], label=f'{ticker} Stock Price', color='black')

    colors = ['red', 'blue', 'green']
    for i, (strategy, trades) in enumerate(trades_dict.items()):
        buy_label = f'{strategy} Buy'
        sell_label = f'{strategy} Sell'
        for j, (buy_idx, sell_idx) in enumerate(trades):
            plt.scatter(buy_idx, data.loc[buy_idx, f'Close_{ticker}'], color=colors[i % len(colors)], marker='^', label=buy_label if j == 0 else "")
            plt.scatter(sell_idx, data.loc[sell_idx, f'Close_{ticker}'], color=colors[i % len(colors)], marker='v', label=sell_label if j == 0 else "")

    plt.xlabel("Date")
    plt.ylabel("Stock Price (US$)")
    plt.title(f"{ticker} Stock Price with Buy/Sell Signals")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    from datetime import datetime, timedelta

    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=5 * 365)).strftime('%Y-%m-%d')

    ticker = "XOM"
    data = download_data(ticker, start_date, end_date)

    strategies = {
        "EMA Crossover": (ema_crossover_strategy, {"short_window": 1, "long_window": 9}),
        "Bollinger Bands": (bollinger_bands_strategy, {"window": 25}),
        "MA Volume": (moving_average_volume_strategy, {"price_window": 10, "volume_window": 20}),
    }

    results_dict = {}
    trades_dict = {}
    total_returns = {}

    for name, (strategy_function, params) in strategies.items():
        data_copy = data.copy()

        # Run the strategy and backtest
        gains, trades = backtest_strategy(data_copy, lambda d, **p: strategy_function(d, ticker, **p), **params)

        results_dict[name] = gains
        trades_dict[name] = trades
        total_returns[name] = sum(gains)

    # Calculate overall market return
    start_price = data[f'Close_{ticker}'].iloc[0]
    end_price = data[f'Close_{ticker}'].iloc[-1]
    market_return = ((end_price - start_price) / start_price) * 100

    print("Total Returns, Adjusted Returns, and Aggregated 5-Year CAGR:")
    aggregated_returns = {}

    for strategy, total_return in total_returns.items():

        adjusted_return = total_return - market_return

        # Calculate CAGR
        years = 5 
        cagr = ((1 + total_return / 100) ** (1 / years) - 1) * 100

        # case where adjusted return is negative
        if 1 + adjusted_return / 100 > 0:
            adjusted_cagr = ((1 + adjusted_return / 100) ** (1 / years) - 1) * 100
        else:
            adjusted_cagr = "N/A"  # Invalid CAGR for negative base

        aggregated_returns[strategy] = (cagr, adjusted_cagr)

        print(f"{strategy}:")
        # print(f"  Total Return: {total_return:.2f}%")
        print(f"  5-Year CAGR: {cagr:.2f}%")
        # print(f"  Adjusted Return (Above Market): {adjusted_return:.2f}%")
        print(f"  Adjusted 5-Year CAGR: {adjusted_cagr}")

    plot_results(results_dict, data, trades_dict, ticker)

