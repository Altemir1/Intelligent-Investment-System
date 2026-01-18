# Investment Intelligence System

AI-powered investment analysis agent that provides personalized portfolio recommendations based on your goals, risk tolerance, and time horizon.

## How It Works

1. **Profile Setup** - Agent learns your investment preferences (once, with periodic updates)
2. **Autonomous Screening** - Agent selects candidate instruments based on your profile
3. **Multi-Method Analysis** - Each candidate scored on fundamentals, technicals, and sentiment
4. **Portfolio Optimization** - Allocations optimized for your risk/reward preferences
5. **Recommendation** - Actionable advice with reasoning and risk warnings

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INVESTMENT SYSTEM                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  LAYER 1: USER PROFILE                                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  user_profile.json                                                   │    │
│  │  - Investment goals (growth, income, preservation)                   │    │
│  │  - Risk tolerance (conservative, moderate, aggressive)               │    │
│  │  - Time horizon (short: <2yr, medium: 2-7yr, long: 7+yr)            │    │
│  │  - Asset preferences (stocks, ETFs, bonds, crypto, metals)          │    │
│  │  - Current holdings (optional, for rebalancing)                      │    │
│  │  - Exclusions (sectors/companies to avoid)                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│  Tools: load_profile(), update_profile(), check_profile_exists()            │
│  Behavior: Auto-detect profile, interactive onboarding if missing           │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  LAYER 2: AUTONOMOUS SCREENING                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Agent determines (from profile, not user input):                    │    │
│  │  1. Which asset classes to include                                   │    │
│  │  2. Target allocation % per class                                    │    │
│  │  3. Screening criteria per class                                     │    │
│  │                                                                      │    │
│  │  Curated universes:                                                  │    │
│  │  - Stocks: S&P 500 tickers                                          │    │
│  │  - ETFs: Popular ETFs by category (50-100)                          │    │
│  │  - Bonds: Bond ETF list                                             │    │
│  │  - Crypto: Top 50 by market cap                                     │    │
│  │  - Metals: GLD, SLV, precious metal ETFs                            │    │
│  │                                                                      │    │
│  │  Output: Candidate list (10-30 instruments) for deep analysis        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│  Tools: get_screening_criteria(), screen_by_asset_class()                   │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  LAYER 3: MULTI-METHOD ANALYSIS                                              │
│  ┌───────────────────┬───────────────────┬───────────────────┐              │
│  │   FUNDAMENTAL     │    TECHNICAL      │    SENTIMENT      │              │
│  │                   │                   │                   │              │
│  │ - P/E, P/B, PEG   │ - 50/200 day MA   │ - Recent news     │              │
│  │ - Debt/Equity     │ - RSI             │ - LLM interprets  │              │
│  │ - Revenue growth  │ - Price vs MA     │ - Confidence flag │              │
│  │ - Profit margins  │ - 52-week range   │                   │              │
│  │ - Dividend yield  │                   │                   │              │
│  │                   │                   │                   │              │
│  │ Score: 1-10       │ Score: 1-10       │ Score: 1-10       │              │
│  └───────────────────┴───────────────────┴───────────────────┘              │
│  Tools: analyze_fundamental(), analyze_technical(), analyze_sentiment()      │
│  Data: yfinance (fundamentals + price), free news API (sentiment)           │
│  Output: Combined score + reasoning for each instrument                      │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  LAYER 4: PORTFOLIO OPTIMIZATION (Simple Bucket Allocation)                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  1. Use target allocations from screening step                       │    │
│  │  2. Rank instruments within each bucket by combined score            │    │
│  │  3. Select top N from each bucket                                    │    │
│  │  4. Check against current holdings for overlap (if provided)         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│  Tools: optimize_portfolio()                                                 │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  LAYER 5: RECOMMENDATION OUTPUT                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  - Executive summary                                                 │    │
│  │  - Recommended portfolio with allocations                            │    │
│  │  - Per-instrument reasoning (why picked, key metrics)                │    │
│  │  - Risk warnings and uncertainties                                   │    │
│  │  - "What to watch" - events that would change recommendation         │    │
│  │  - Action items (buy/sell/hold)                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│  Tools: generate_recommendation()                                            │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR: Main Agent (agent.py)                                         │
│  - Gemini 2.5 Flash via LangChain                                           │
│  - Access to all tools above                                                │
│  - Conversation history for follow-up questions                              │
│  - Runs full pipeline or individual steps on request                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
investment-system/
├── agent.py                 # Main orchestrator agent
├── prompt.py                # System prompt for investment analyst
├── config.py                # API keys, constants, allocation defaults
├── tools/
│   ├── __init__.py
│   ├── profile.py           # User profile management (load/save/update)
│   ├── screener.py          # Autonomous instrument screening
│   ├── fundamental.py       # Fundamental analysis scoring
│   ├── technical.py         # Technical analysis scoring
│   ├── sentiment.py         # News sentiment analysis
│   └── optimizer.py         # Portfolio optimization
├── data/
│   ├── user_profile.json    # Persisted user preferences
│   ├── universes/           # Curated ticker lists
│   │   ├── sp500.json
│   │   ├── etfs.json
│   │   ├── bonds.json
│   │   ├── crypto.json
│   │   └── metals.json
│   └── recommendations/     # Historical recommendations (future)
└── models/
    └── schemas.py           # Pydantic models for data structures
```

## Development Tasks

Each task is designed to be completed in 1-2 hours.

### Task 1: Project Setup + User Profile System
**Goal**: Create folder structure, data models, and profile management tools.

**Deliverables**:
- `models/schemas.py` - Pydantic models for UserProfile, Holding, AnalysisResult
- `tools/profile.py` - Functions: `check_profile_exists()`, `load_profile()`, `save_profile()`, `create_profile_interactive()`
- `data/user_profile.json` - Template/example profile
- `config.py` - Constants and configuration

**Key concepts**: Persistent memory, Pydantic validation, tool design for LLMs

---

### Task 2: Fundamental Analysis Tool
**Goal**: Fetch and score stocks/ETFs on fundamental metrics.

**Deliverables**:
- `tools/fundamental.py` - Function: `analyze_fundamental(ticker: str) -> FundamentalScore`
- Metrics: P/E, P/B, PEG, debt/equity, revenue growth, profit margin, dividend yield
- Scoring logic: 1-10 scale with reasoning

**Key concepts**: Financial data APIs (yfinance), structured tool output

---

### Task 3: Technical Analysis Tool
**Goal**: Compute technical indicators and score instruments.

**Deliverables**:
- `tools/technical.py` - Function: `analyze_technical(ticker: str) -> TechnicalScore`
- Indicators: 50-day MA, 200-day MA, RSI, 52-week high/low position
- Scoring logic: 1-10 scale based on trend signals

**Key concepts**: Time series analysis, pandas for price data

---

### Task 4: Sentiment Analysis Tool
**Goal**: Fetch news and analyze sentiment using LLM.

**Deliverables**:
- `tools/sentiment.py` - Function: `analyze_sentiment(ticker: str) -> SentimentScore`
- News fetching via free API (NewsAPI free tier or Google News RSS)
- LLM interprets headlines/summaries, outputs sentiment score + confidence

**Key concepts**: LLM-as-judge pattern, unstructured data processing

---

### Task 5: Curated Universes + Autonomous Screener
**Goal**: Create ticker lists and screening logic driven by profile.

**Deliverables**:
- `data/universes/*.json` - Curated lists (S&P 500, ETFs by category, top crypto, bond ETFs, metal ETFs)
- `tools/screener.py` - Functions: `get_allocation_targets(profile)`, `screen_candidates(profile, universe)`
- Allocation mapping: profile → target % per asset class

**Key concepts**: Agent autonomy, rule-based filtering

---

### Task 6: Portfolio Optimizer
**Goal**: Rank and select instruments within allocation buckets.

**Deliverables**:
- `tools/optimizer.py` - Function: `optimize_portfolio(candidates, allocations, holdings)`
- Logic: Rank by combined score, select top N per bucket, flag overlaps with current holdings

**Key concepts**: Multi-signal aggregation, simple optimization

---

### Task 7: Agent Integration + System Prompt
**Goal**: Wire all tools into the main agent, craft effective prompt.

**Deliverables**:
- Updated `agent.py` - Import and register all tools
- Updated `prompt.py` - Detailed system prompt covering full workflow
- Profile check logic at startup (onboard or load)

**Key concepts**: Agentic workflows, prompt engineering for tool use

---

### Task 8: End-to-End Testing + Refinement
**Goal**: Run full pipeline, identify issues, refine.

**Deliverables**:
- Test with real profile and tickers
- Fix edge cases (missing data, API failures)
- Tune scoring weights and prompt instructions
- Document any manual steps needed

**Key concepts**: System integration, error handling in agents

---

## Future Enhancements (Post-MVP)

- [ ] SQLite for profile and history storage
- [ ] Correlation-aware portfolio optimization
- [ ] Backtesting recommendations against historical data
- [ ] Web UI or Telegram bot interface
- [ ] Scheduled quarterly reports
- [ ] Multiple user profiles

## Setup

```bash
# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Add your GOOGLE_API_KEY to .env

# Run the agent
python agent.py
```

## Tech Stack

- **LLM**: Google Gemini 2.5 Flash Lite via LangChain
- **Financial Data**: yfinance (free)
- **News**: Free news API (NewsAPI / Google News RSS)
- **Package Manager**: uv
- **Python**: 3.13+
