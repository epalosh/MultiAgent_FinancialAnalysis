from langchain.llms.base import BaseLLM
from typing import Any, Dict
import json

class RecommendationAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.name = "Recommendation Agent"
    
    def generate_recommendation(self, analysis_data: str) -> str:
        """
        Generate investment recommendations based on analysis results
        """
        try:
            prompt = f"""
            As an investment advisor, please provide recommendations based on the following analysis: {analysis_data}
            
            Please provide:
            1. Investment recommendation (Buy/Hold/Sell) with confidence level
            2. Target price range (if applicable)
            3. Key risks and opportunities
            4. Portfolio allocation suggestions
            5. Time horizon considerations
            6. Alternative investment options
            
            Provide clear, actionable recommendations with reasoning for each suggestion.
            Disclaimer: Include appropriate risk warnings and mention this is not financial advice.
            """
            
            result = self.llm(prompt)
            
            return f"Recommendation Agent findings:\n{result}"
            
        except Exception as e:
            return f"Recommendation Agent error: {str(e)}"
    
    def assess_risk_level(self, company_data: Dict[str, Any]) -> str:
        """
        Assess the risk level of an investment
        """
        # Simplified risk assessment logic
        risk_factors = []
        
        # This would be more sophisticated in a real implementation
        if company_data.get('debt_to_equity', 0) > 0.6:
            risk_factors.append("High leverage")
        
        if company_data.get('current_ratio', 0) < 1.2:
            risk_factors.append("Liquidity concerns")
        
        if len(risk_factors) == 0:
            return "Low Risk"
        elif len(risk_factors) <= 2:
            return "Medium Risk"
        else:
            return "High Risk"
