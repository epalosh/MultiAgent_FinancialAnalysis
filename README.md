# Multi-Agent Financial Analysis Platform

A financial analysis system that uses specialized AI agents to provide comprehensive stock analysis using real-time market data.

## Backend Architecture

The system is built on LangChain and employs three specialized agents that work together to analyze financial data:

### Research Agent
Gathers comprehensive financial information using "real-time" data sources:
- Yahoo Finance API integration via yfinance (15 min delay)
- Company fundamentals and business information
- News and public sentiment

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

## Usage

Users can analyze any publicly traded stock by entering the ticker symbol or company name. The system supports all major exchanges and provides comprehensive analysis with real-time data validation.

## Additional Information

This project was built heavily with AI. The primary goal is functionality over form. It's scrappy and effective! 

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
