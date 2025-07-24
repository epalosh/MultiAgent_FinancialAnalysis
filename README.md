# Multi-Agent Financial Analysis Platform

A financial analysis system that uses specialized AI agents to provide comprehensive stock analysis using real-time market data.

## Backend Architecture

The system is built on LangChain and employs three specialized agents that work together to analyze financial data:

### Research Agent
Gathers comprehensive financial information using real-time data sources:
- Yahoo Finance API integration via yfinance
- Real-time stock price and market data
- Company fundamentals and business information
- Financial statements and metrics
- News and analyst data

### Analysis Agent
Performs detailed financial analysis and calculations:
- Advanced financial ratio calculations
- Risk assessment and volatility analysis
- Valuation metrics (P/E, PEG, DCF modeling)
- Performance comparisons against market benchmarks
- Quantitative scoring and investment metrics

### Recommendation Agent
Generates investment recommendations and strategic guidance:
- Buy/sell/hold recommendations with price targets
- Risk-adjusted portfolio allocation suggestions
- Scenario analysis (bull/bear/base cases)
- Investment horizon recommendations
- Risk management strategies

### Financial Orchestrator
Coordinates the agents and manages the analysis workflow. Provides tools for:
- Stock symbol validation and extraction
- Multi-stock comparison analysis
- Quick analysis for rapid insights
- Real-time market data retrieval

## Data Sources

The system integrates multiple data sources for comprehensive analysis:

### Primary Data Sources
- **Yahoo Finance API** - Real-time stock data, financials, and basic news
- **yfinance Library** - Historical data and market metrics

### Web Scraping Sources
- **Finviz.com** - Advanced financial metrics, analyst recommendations, and ownership data
- **MarketWatch** - Real-time financial news and market analysis
- **Yahoo Finance (Extended)** - Additional news coverage and market insights
- **SEC EDGAR** - Regulatory filings and corporate governance documents
- **Insider Trading Data** - Corporate insider buy/sell activity tracking

### Economic Data
- **FRED (Federal Reserve Economic Data)** - Economic indicators and market context

The web scraping infrastructure provides:
- Enhanced financial metrics not available through APIs
- Real-time news sentiment analysis
- Regulatory filing monitoring
- Insider trading activity tracking
- Multi-source data validation

## Frontend

A React-based frontend built with AI assistance that provides an intuitive interface for submitting analysis requests and viewing results.

## Usage

Users can analyze any publicly traded stock by entering the ticker symbol or company name. The system supports all major exchanges and provides comprehensive analysis with real-time data validation.

##  Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. **Configure API Key**: Edit `backend/config.py` and replace `"your-openai-api-key-here"` with your actual OpenAI API key:
```python
OPENAI_API_KEY = "sk-your-actual-openai-api-key"
```

6. Run the Flask server:
```bash
python app.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`
