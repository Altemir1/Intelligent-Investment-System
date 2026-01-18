from pydantic import BaseModel, Field
from enum import Enum

# Enums
class SecurityType(str, Enum):
    STOCK = "Stock"
    BOND = "Bond"
    ETF = "ETF"
    CRYPTOCURRENCY = "Cryptocurrency"


# Data Models
class Holdings(BaseModel):
    security_type: SecurityType = Field(..., description="Type of the security user bought")
    ticker: str = Field(..., description="The stock ticker symbol")
    quantity: float = Field(..., gt=0.0, description="The number of shares user bought")
    purchase_price: float = Field(..., gt=0.0, description="The price at which the user bought the asset")

class AnalysisResult(BaseModel):
    recommended_action: str = Field(..., description="The recommended action for the user based on the analysis. Each point as an action")
    reasoning: str = Field(..., description="The reasoning behind the recommended action")
    supporting_data: list[str] = Field(..., description="Supporting data or evidence for the recommended action")

class UserProfile(BaseModel):
    risk_tolerance: float = Field(..., gt=0, lt=30.0, description="User's risk tolerance level. How much percent user can afford to lose per year")
    time_horizon: float = Field(..., gt=0, lt=50.0, description="Investment time horizon in years")
    investment_goal: str = Field(..., description="What does the user want to achieve with their investments")
    profit_target: str = Field(default="Maximum profit a user can achieve", description="The profit target the user aims for with their investments")
    current_holdings : Holdings = Field(..., description='Current assets of owned by user')
    

