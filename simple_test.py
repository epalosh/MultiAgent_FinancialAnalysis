#!/usr/bin/env python3
"""
Simple test to verify the financial analysis system is working
"""
import sys
import os
sys.path.append('backend')
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.recommendation_agent import RecommendationAgent
from agents.financial_orchestrator import FinancialOrchestrator
from langchain_openai import ChatOpenAI
import config

def test_basic_functionality():
    print("🚀 Testing Basic Financial Analysis System")
    print("=" * 50)
    
    try:
        # Initialize LLM
        llm = ChatOpenAI(
            model_name=config.OPENAI_MODEL,
            temperature=config.AGENT_TEMPERATURE,
            api_key=config.OPENAI_API_KEY,
            max_tokens=2000,  # Smaller for testing
            request_timeout=config.TIMEOUT_SECONDS
        )
        print("✅ LLM initialized")
        
        # Test research agent
        research_agent = ResearchAgent(llm)
        print("✅ Research Agent initialized")
        
        # Simple test query
        simple_query = "Provide basic financial information for Apple Inc."
        print(f"\n🔍 Testing with query: {simple_query}")
        
        # Test research
        research_result = research_agent.research_company(simple_query)
        print(f"✅ Research completed - {len(research_result)} characters")
        print(f"📋 Preview: {research_result[:100]}...")
        
        # Test if it contains realistic data (not placeholders)
        if "XX.X" in research_result or "placeholder" in research_result.lower():
            print("❌ Contains placeholders - needs improvement")
        else:
            print("✅ No placeholders found - good!")
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    if success:
        print("\n🎉 Basic test passed! System appears to be working.")
    else:
        print("\n💥 Basic test failed. Check configuration and API key.")
