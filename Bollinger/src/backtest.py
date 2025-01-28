import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from bollinger import calculate_bollinger_bands
from strategy import bollinger_strategy_signals


def main():
    # Parameters
    ticker = "AAPL"
    start_date = "2022-01-01"
    end_date = "2022-12-31"

    # Get data from Yahoo Finance
    df = yf.download(ticker, start=start_date, end=end_date)

    # Alternatively, load data from local CSV:
    # df = pd.read_csv("data/sample_data.csv", parse_dates=True, index_col='Date')

    # Ensure df has the necessary columns
    if "Close" not in df.columns:
        print("Data does not have a 'Close' column. Check your data source.")
        return

    # Calculate Bollinger Bands
    df = calculate_bollinger_bands(df, window=20, num_std=2)

    # Generate signals
    df = bollinger_strategy_signals(df)

    # Compute returns
    df['Daily_Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Daily_Return'] * df['Signal'].shift(
        1)  # Shift signal by 1 day

    # Calculate cumulative returns
    df['Cumulative_Market_Return'] = (1 + df['Daily_Return']).cumprod()
    df['Cumulative_Strategy_Return'] = (1 + df['Strategy_Return']).cumprod()

    # Print basic performance metrics
    final_market_return = df['Cumulative_Market_Return'].iloc[-1] - 1
    final_strategy_return = df['Cumulative_Strategy_Return'].iloc[-1] - 1

    print(f"Market Return over period: {final_market_return:.2%}")
    print(f"Strategy Return over period: {final_strategy_return:.2%}")

    # Plot price and Bollinger Bands
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.plot(df.index, df['MA'], label='Moving Average', linestyle='--')
    plt.plot(df.index, df['UpperBand'], label='Upper Band', linestyle='--')
    plt.plot(df.index, df['LowerBand'], label='Lower Band', linestyle='--')
    plt.title(f"{ticker} Price with Bollinger Bands")
    plt.legend()
    plt.show()

    # Plot Cumulative Returns
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Cumulative_Market_Return'], label='Market Return')
    plt.plot(df.index,
             df['Cumulative_Strategy_Return'],
             label='Strategy Return')
    plt.title("Cumulative Returns")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
