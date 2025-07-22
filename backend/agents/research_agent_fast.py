from langchain.llms.base import BaseLLM
from langchain.schema import HumanMessage
from typing import Any, Dict
import json

class ResearchAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.name = "Research Agent"
    
    def _call_llm(self, prompt: str) -> str:
        """Helper method to call the LLM with proper format"""
        try:
            # Check if it's ChatOpenAI (has message-based interface)
            if hasattr(self.llm, 'predict_messages') or 'Chat' in str(type(self.llm)):
                response = self.llm.invoke([HumanMessage(content=prompt)])
                return response.content if hasattr(response, 'content') else str(response)
            else:
                # Fallback for other LLM types
                return self.llm.invoke(prompt)
        except Exception as e:
            return f"LLM call failed: {str(e)}"
    
    def research_company(self, company_info: str) -> str:
        """
        Research financial information about a company (optimized for speed)
        """
        try:
            prompt = f"""
            Research the following company/topic: {company_info}
            
            Provide a focused research summary (400-600 words) covering:

            ## Company Overview
            - Company name, ticker symbol, and sector
            - Primary business and revenue sources
            - Market capitalization and size

            ## Financial Highlights  
            - Revenue and profit trends (last 2 years)
            - Key financial ratios (P/E, debt-to-equity, profit margins)
            - Balance sheet strength

            ## Market Position
            - Stock performance vs market
            - Main competitors
            - Market share position

            ## Recent News
            - Latest quarterly earnings
            - Major announcements or changes
            - Analyst sentiment

            ## Key Risks
            - Primary business risks
            - Market/industry challenges
            - Competitive threats

            Be concise but include specific numbers, percentages, and financial data.
            """
            
            result = self._call_llm(prompt)
            
            return f"📊 FINANCIAL RESEARCH SUMMARY:\n\n{result}"
            
        except Exception as e:
            return f"Research Agent error: {str(e)}"
    
    def get_market_data(self, symbol: str) -> str:
        """
        Get basic market data for a stock symbol
        """
        try:
            # This would integrate with a real data source in production
            return f"Market data for {symbol} - This would contain real-time pricing and basic metrics"
        except Exception as e:
            return f"Error getting market data: {str(e)}"
