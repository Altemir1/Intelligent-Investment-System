from langchain.tools import tool
import yfinance as yf


@tool
def fetch_yahoo_analyst_forecast(ticker: str) -> dict:
    """
    Fetch Yahoo Finance analyst price targets for a ticker.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL", "TSLA").

    Returns:
        dict: Analyst price targets with keys like:
            - current (float | None)
            - high (float | None)
            - low (float | None)
            - mean (float | None)
            - median (float | None)
        If the API does not return data, the dict may be empty.
    """
    try:
        data = yf.Ticker(ticker)
        forecast = data.analyst_price_targets
        return forecast
    except Exception as e:
        print("No such ticker or company available in API")
        print(e)

