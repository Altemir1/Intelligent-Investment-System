from langchain.tools import tool
from models.schemas import UserProfile
import json

@tool
def check_profile_exists() -> bool:
    """
    Check if the user profile exists in the system.

    Returns:
        bool: True if the profile exists, False otherwise.
    """
    try:
        with open("data/user_profile.json", "r") as file:
                data = json.load(file)
                user_profile = UserProfile(**data)
                return user_profile is not None
    
    except Exception:
        return False

@tool
def save_profile(data: dict) -> bool:
    """
    Save the user profile to the system.

    Args:
        data (dict): The user profile data.

    Returns:
        bool: True if the profile was saved successfully, False otherwise.
    """
    try:
        user_profile = UserProfile(**data)
        with open("data/user_profile.json", "w") as file:
            json.dump(user_profile.dict(), file, indent=4)
        return True
    except Exception:
        return False

@tool
def load_profile() -> UserProfile | None:
     """
     Load the user profile from the system.
     """
     try:
          with open("data/user_profile.json", "r") as file:
               data = json.loads(file)
               return UserProfile(**data)
     except Exception:
          return None