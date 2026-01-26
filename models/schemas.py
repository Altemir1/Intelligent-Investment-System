from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import Self

# Enums
class SecurityType(str, Enum):
    STOCK = "Stock"
    BOND = "Bond"
    ETF = "ETF"
    CRYPTOCURRENCY = "Cryptocurrency"
    MUTUAL_FUND = "Mutual Fund"
    INDEX_FUND = "Index Fund"

class StatusType(str, Enum):
    LOADED = "Loaded"
    CHECKED = "Checked"
    SAVED = "Saved"
    ERROR = "Error"


# Data Models
class Holdings(BaseModel):
    """
    Flexible holdings model - supports multiple ways to describe investments.

    User can provide EITHER:
    - total_value alone (e.g., "$10,000 in SP500")
    - quantity + purchase_price (e.g., "50 shares at $150")
    - Any combination with available info
    """
    security_type: SecurityType = Field(..., description="Type: Stock, Bond, ETF, Cryptocurrency, Mutual Fund, or Index Fund")
    ticker: str = Field(..., description="Symbol (e.g., SPY, AAPL, BTC) or fund name if no ticker")

    # Optional detailed info - use when user provides specific numbers
    quantity: float | None = Field(default=None, gt=0.0, description="Number of shares/units if known")
    purchase_price: float | None = Field(default=None, gt=0.0, description="Price per share when bought if known")

    # Alternative - use when user only knows total value
    total_value: float | None = Field(default=None, gt=0.0, description="Total investment value in dollars (use if quantity/price unknown)")

    # Extra context
    notes: str | None = Field(default=None, description="Any extra details user mentioned (e.g., 'bought last year', 'in my 401k')")

    @model_validator(mode="after")
    def check_has_value_info(self) -> Self:
        """Ensure we have at least some value information."""
        has_detailed = self.quantity is not None and self.purchase_price is not None
        has_total = self.total_value is not None
        has_partial = self.quantity is not None or self.purchase_price is not None

        if not has_detailed and not has_total and not has_partial:
            raise ValueError("Provide at least one of: total_value, quantity, or purchase_price")
        return self

# Main model output (Final result)
class AnalysisResult(BaseModel):
    recommended_action: str = Field(..., description="The recommended action for the user based on the analysis. Each point as an action. Short and concise points")
    reasoning: str = Field(..., description="The reasoning behind the recommended action. No longer than 100 words")
    supporting_data: list[str] = Field(..., description="Supporting data or evidence for the recommended action. No longer that 100 words")

# User profile for preferences
class UserProfile(BaseModel):
    risk_tolerance: float = Field(..., gt=0, lt=30.0, description="User's risk tolerance level. How much percent user can afford to lose per year")
    time_horizon: float = Field(..., gt=0, lt=50.0, description="Investment time horizon in years")
    investment_goal: str = Field(..., description="What does the user want to achieve with their investments")
    profit_target: str = Field(default="Maximum profit a user can achieve", description="The profit target the user aims for with their investments")
    current_holdings: list[Holdings] | None = Field(default=None, description="List of current assets owned by user, or None if no holdings")

# Final output of the Fundamental Analyst Sub-Agent
class FundamentalAnalysis(BaseModel):
    score: int = Field(..., ge=0, le=10, description="Overall fundamental analysis score from 0 (poor) to 10 (excellent)")
    reasoning: str = Field(..., description="Detailed reasoning behind the assigned score. No more than 150 words.")
    horizon: str = Field(..., description="Recommended investment horizon based on fundamentals (e.g., in number of quarters)")
    key_strengths: list[str] = Field(..., description="2-4 key fundamental strengths identified from the analysis")
    key_risks: list[str] = Field(..., description="2-4 key fundamental risks or concerns identified from the analysis")

# Intermediary output of the User Manager Sub-Agent
class ProfileStatus(BaseModel):
    status: StatusType = Field(..., description="Status of the profile operation")
    changes_content: str | None = Field(default=None, description="Details about changes made or errors encountered")

