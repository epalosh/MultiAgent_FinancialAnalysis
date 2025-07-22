from langchain.llms.base import BaseLLM
from langchain.schema import HumanMessage
from typing import Any, Dict
import json

class AnalysisAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.name = "Analysis Agent"
    
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
    
    def analyze_data(self, data: str) -> str:
        """
        Perform financial analysis (optimized for speed)
        """
        try:
            prompt = f"""
            Analyze the following financial information: {data}
            
            Provide a focused financial analysis (400-600 words) covering:

            ## Financial Ratio Analysis
            - Liquidity ratios (current ratio, quick ratio)
            - Profitability ratios (ROE, ROA, profit margins)
            - Leverage ratios (debt-to-equity, interest coverage)
            - Efficiency ratios (asset turnover, inventory turnover)

            ## Performance Assessment
            - Revenue and earnings trends
            - Margin analysis and sustainability
            - Cash flow strength
            - Balance sheet quality

            ## Valuation Analysis
            - Current valuation metrics (P/E, P/B, EV/EBITDA)
            - Historical valuation comparison
            - Peer valuation comparison
            - Fair value assessment

            ## Risk Analysis
            - Financial risk factors
            - Operational leverage
            - Credit risk assessment
            - Market sensitivity

            ## Key Findings
            - Strengths and opportunities
            - Weaknesses and threats
            - Overall financial health score (1-10)
            - Key metrics to monitor

            Include specific numbers, ratios, and percentages in your analysis.
            """
            
            result = self._call_llm(prompt)
            
            return f"📈 FINANCIAL ANALYSIS RESULTS:\n\n{result}"
            
        except Exception as e:
            return f"Analysis Agent error: {str(e)}"
    
    def calculate_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate key financial ratios
        """
        try:
            ratios = {}
            
            # Basic ratio calculations (these would use real data in production)
            if 'current_assets' in financial_data and 'current_liabilities' in financial_data:
                ratios['current_ratio'] = financial_data['current_assets'] / financial_data['current_liabilities']
            
            if 'total_debt' in financial_data and 'total_equity' in financial_data:
                ratios['debt_to_equity'] = financial_data['total_debt'] / financial_data['total_equity']
            
            return ratios
            
        except Exception as e:
            return {"error": str(e)}
