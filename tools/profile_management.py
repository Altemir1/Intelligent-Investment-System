from langchain.tools import tool
from models.schemas import UserProfile
from pathlib import Path
import json

# Get absolute path to data directory relative to this file
DATA_DIR = Path(__file__).parent.parent / "data"
PROFILE_PATH = DATA_DIR / "user_profile.json"


@tool
def check_profile_exists() -> str:
    """
    Check if the user profile exists in the system.

    Returns:
        str: Message indicating whether profile exists and is valid.
    """
    if not PROFILE_PATH.exists():
        return "No profile found. User needs to create a profile."

    try:
        with open(PROFILE_PATH, "r") as file:
            data = json.load(file)
            if not data:
                return "Profile file is empty. User needs to create a profile."
            UserProfile(**data)
            return "Profile exists and is valid."
    except json.JSONDecodeError:
        return "Profile file is corrupted. User needs to create a new profile."
    except Exception as e:
        return f"Profile validation failed: {str(e)}"


@tool
def save_profile(data: dict) -> str:
    """
    Save the user profile to the system. Extract values from user's natural language.

    Args:
        data (dict): The user profile data with these keys:
            - risk_tolerance (float): 1-29, derived from user's comfort with loss
            - time_horizon (float): 1-49, years until they need the money
            - investment_goal (str): Their objective (e.g., "retirement", "growth")
            - profit_target (str): Expected returns (e.g., "8-12% annually")
            - current_holdings (list | None): Optional list of holdings

    Holdings format - FLEXIBLE, use what info is available:
        - security_type (required): "Stock", "Bond", "ETF", "Cryptocurrency", "Mutual Fund", "Index Fund"
        - ticker (required): Symbol like "SPY", "AAPL", "BTC", or fund name
        - quantity (optional): Number of shares if known
        - purchase_price (optional): Price per share if known
        - total_value (optional): Total dollar amount if quantity/price unknown
        - notes (optional): Extra context like "in 401k", "bought 2 years ago"

    EXAMPLES:

    1. Full details - "50 Apple shares at $150":
       {"security_type": "Stock", "ticker": "AAPL", "quantity": 50, "purchase_price": 150.0}

    2. Only total value - "$10,000 in SP500":
       {"security_type": "Index Fund", "ticker": "SPY", "total_value": 10000.0}

    3. Partial info - "About 100 shares of Tesla":
       {"security_type": "Stock", "ticker": "TSLA", "quantity": 100}

    4. With context - "$5000 in Bitcoin, bought last year":
       {"security_type": "Cryptocurrency", "ticker": "BTC", "total_value": 5000.0, "notes": "bought last year"}

    If user has no holdings, set current_holdings to null.

    Returns:
        str: Message indicating success or failure with details.
    """
    try:
        # Validate data against schema
        user_profile = UserProfile(**data)

        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Save to file
        with open(PROFILE_PATH, "w") as file:
            json.dump(user_profile.model_dump(), file, indent=4)

        return "Profile saved successfully."
    except Exception as e:
        return f"Failed to save profile: {str(e)}"


@tool
def load_profile() -> str:
    """
    Load the user profile from the system.

    Returns:
        str: JSON string of user profile data, or error message if not found.
    """
    if not PROFILE_PATH.exists():
        return "No profile found. Please create a profile first."

    try:
        with open(PROFILE_PATH, "r") as file:
            data = json.load(file)
            user_profile = UserProfile(**data)
            return json.dumps(user_profile.model_dump(), indent=2)
    except json.JSONDecodeError:
        return "Profile file is corrupted. Please create a new profile."
    except Exception as e:
        return f"Failed to load profile: {str(e)}"
