from langchain.llms.base import BaseLLM
from typing import Any, Dict
import json

class AnalysisAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.name = "Analysis Agent"
    
    def analyze_data(self, data: str) -> str:
        """
        Analyze financial data and perform calculations
        """
        try:
            prompt = f"""
            As a financial analysis expert, please analyze the following data: {data}
            
            Please provide:
            1. Financial ratio analysis (liquidity, profitability, leverage, efficiency)
            2. Trend analysis (if historical data is available)
            3. Strengths and weaknesses identification
            4. Risk assessment
            5. Comparative analysis with industry standards
            
            Present your analysis in a clear, structured format with specific metrics and interpretations.
            """
            
            result = self.llm(prompt)
            
            return f"Analysis Agent findings:\n{result}"
            
        except Exception as e:
            return f"Analysis Agent error: {str(e)}"
    
    def calculate_ratios(self, financial_data: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate key financial ratios
        """
        ratios = {}
        
        # Example ratio calculations (would be more comprehensive in real implementation)
        if 'current_assets' in financial_data and 'current_liabilities' in financial_data:
            ratios['current_ratio'] = financial_data['current_assets'] / financial_data['current_liabilities']
        
        if 'net_income' in financial_data and 'revenue' in financial_data:
            ratios['profit_margin'] = financial_data['net_income'] / financial_data['revenue']
        
        return ratios
