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


@tool
def analyse_fundamentals(ticker:str) -> str:
    """
    Analyze the fundamental data of a given stock ticker.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL", "TSLA").

    Returns:
        str: A summary of the fundamental analysis.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        analysis = f"Fundamental Analysis for {ticker}:\n"
        analysis += f"Company Name: {info.get('longName', 'N/A')}\n"
        analysis += f"Sector: {info.get('sector', 'N/A')}\n"
        analysis += f"Industry: {info.get('industry', 'N/A')}\n"
        analysis += f"Market Cap: {info.get('marketCap', 'N/A')}\n"
        analysis += f"PE Ratio: {info.get('trailingPE', 'N/A')}\n"
        analysis += f"Dividend Yield: {info.get('dividendYield', 'N/A')}\n"
        analysis += f"52 Week High: {info.get('fiftyTwoWeekHigh', 'N/A')}\n"
        analysis += f"52 Week Low: {info.get('fiftyTwoWeekLow', 'N/A')}\n"

        return analysis
    except Exception as e:
        return f"Error fetching fundamental data for {ticker}: {str(e)}"