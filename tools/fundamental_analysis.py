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
        return {"error": f"No data available for {ticker}: {str(e)}"}


@tool
def fetch_fundamental_data(ticker: str) -> dict:
    """
    Fetch all available fundamental data for a given stock ticker.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL", "TSLA").

    Returns:
        dict: Fundamental metrics including valuation, profitability, and growth data.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        fundamentals = {
            # Company info
            "ticker": ticker,
            "company_name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),

            # Valuation metrics
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "pb_ratio": info.get("priceToBook"),
            "peg_ratio": info.get("pegRatio"),
            "price_to_sales": info.get("priceToSalesTrailing12Months"),

            # Profitability metrics
            "profit_margin": info.get("profitMargins"),
            "operating_margin": info.get("operatingMargins"),
            "gross_margin": info.get("grossMargins"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),

            # Financial health
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),

            # Growth metrics
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),

            # Dividend info
            "dividend_yield": info.get("dividendYield"),
            "payout_ratio": info.get("payoutRatio"),

            # Price context
            "current_price": info.get("currentPrice"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
            "fifty_day_average": info.get("fiftyDayAverage"),
            "two_hundred_day_average": info.get("twoHundredDayAverage"),
        }

        return fundamentals
    except Exception as e:
        return {"error": f"Error fetching fundamental data for {ticker}: {str(e)}"}
    
    