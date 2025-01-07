import yfinance as yf


def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in data.columns]
    return data