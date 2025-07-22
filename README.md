# Multi-Agent Financial Analysis System

This project demonstrates a multi-agent orchestration system using LangChain, with a React frontend and Flask backend for financial analysis.

## 🏗️ Architecture

- **Frontend**: React application (without Tailwind) for user interface
- **Backend**: Flask API server with LangChain multi-agent orchestration
- **Agents**: Specialized agents for research, analysis, and recommendations

## 🚀 Quick Start

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

## 🤖 Agent System

### Financial Orchestrator
- Coordinates multiple specialized agents
- Uses LangChain's conversation agent with tools
- Maintains conversation memory

### Specialized Agents

1. **Research Agent**: Gathers company financial data and market information
2. **Analysis Agent**: Performs financial calculations and ratio analysis
3. **Recommendation Agent**: Generates investment recommendations and risk assessments

## 📁 Project Structure

```
MultiAgent_FinancialAnalysis/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── financial_orchestrator.py
│   │   ├── research_agent.py
│   │   ├── analysis_agent.py
│   │   └── recommendation_agent.py
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── QueryForm.js
│   │   │   ├── ResultDisplay.js
│   │   │   ├── AgentStatus.js
│   │   │   └── LoadingSpinner.js
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   └── package.json
└── README.md
```

## 🔧 Configuration

### Environment Variables (Set in Code)

Currently, configuration is set directly in `backend/config.py` for simplicity:

```python
OPENAI_API_KEY = "your-openai-api-key-here"
```

**Important**: Replace this with your actual OpenAI API key before running the application.

## 💡 Usage

1. Start both the backend (Flask) and frontend (React) servers
2. Open your browser to `http://localhost:3000`
3. Enter a financial analysis query (with optional company name)
4. Watch as the multi-agent system collaborates to provide comprehensive analysis

### Example Queries

- "Analyze the financial health and investment potential of Apple Inc."
- "What are the key financial risks for Tesla in 2024?"
- "Compare the profitability ratios of Microsoft vs Google"
- "Should I invest in renewable energy stocks right now?"

## 🔄 API Endpoints

- `POST /api/analyze` - Submit financial analysis query
- `GET /api/agents` - Get information about available agents
- `GET /api/health` - Health check endpoint

## ⚠️ Important Notes

1. **API Key Configuration**: Make sure to set your OpenAI API key in the code
2. **Rate Limits**: Be aware of OpenAI API rate limits
3. **Costs**: Monitor your OpenAI usage as API calls incur costs
4. **Mock Data**: Some agents use mock data for demonstration purposes

## 🔮 Future Enhancements

- Environment variable configuration
- Real financial data integration (APIs like Alpha Vantage, Yahoo Finance)
- Database storage for analysis history
- User authentication
- Advanced agent capabilities
- Docker containerization

## 📄 License

This project is for educational and demonstration purposes.
