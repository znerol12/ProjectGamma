import pandas as pd


def bollinger_strategy_signals(df: pd.DataFrame):
    """
    Generate trading signals based on Bollinger Bands.

    Buy signal when Close goes below the LowerBand.
    Sell signal when Close goes above the UpperBand.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'Close', 'UpperBand', 'LowerBand' columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with 'Signal' column where:
        1 = Buy signal,
        -1 = Sell signal,
        0 = Hold/No action.
    """
    # Initialize signals column with 0
    df['Signal'] = 0

    # Buy when price crosses below lower band
    buy_condition = df['Close'] < df['LowerBand']

    # Sell when price crosses above upper band
    sell_condition = df['Close'] > df['UpperBand']

    # Assign signals
    df.loc[buy_condition, 'Signal'] = 1
    df.loc[sell_condition, 'Signal'] = -1

    return df
