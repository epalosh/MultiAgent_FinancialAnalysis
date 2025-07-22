from langchain.llms.base import BaseLLM
from langchain.schema import HumanMessage
from typing import Any, Dict
import json

class RecommendationAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.name = "Recommendation Agent"
    
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
    
    def generate_recommendation(self, analysis_data: str) -> str:
        """
        Generate comprehensive investment recommendations based on analysis results
        """
        try:
            prompt = f"""
            As a financial advisor, provide investment recommendations based on: {analysis_data}
            
            Provide a concise analysis (500-800 words) covering:

            ## Investment Recommendation
            - Clear Buy/Hold/Sell with confidence level (1-10)
            - Target price range (12-month) and rationale
            - Position sizing recommendation

            ## Key Investment Drivers
            - Top 3-4 reasons supporting the recommendation
            - Expected return scenarios (bull/base/bear)
            - Key catalysts and timing

            ## Risk Analysis
            - Primary risk factors
            - Risk mitigation strategies
            - Maximum drawdown expectations

            ## Portfolio Context
            - Allocation recommendation for different risk profiles
            - Alternative investment options

            ## Monitoring Framework
            - Key metrics to track quarterly
            - Rebalancing triggers

            Be concise but quantitative. Include specific percentages and ratios.
            Disclaimer: This is analytical research, not personalized financial advice.
            """
            
            result = self._call_llm(prompt)
            
            return f"💡 COMPREHENSIVE INVESTMENT RECOMMENDATIONS & DETAILED ANALYSIS:\n\n{result}"
            
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
