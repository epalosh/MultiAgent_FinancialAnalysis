#!/usr/bin/env python3
"""
Test script to verify the agents work properly with the new ChatOpenAI configuration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.agents.financial_orchestrator import FinancialOrchestrator

def test_agents():
    """Test the financial agents with a simple query"""
    
    print("🚀 Testing Multi-Agent Financial Analysis System")
    print("=" * 60)
    
    try:
        # Initialize the orchestrator
        print("📊 Initializing Financial Orchestrator...")
        orchestrator = FinancialOrchestrator()
        print("✅ Orchestrator initialized successfully")
        
        # Test query
        query = "Analyze Apple's financial performance and investment potential"
        
        print(f"\n📝 Testing query: {query}")
        print("-" * 60)
        
        # Test individual agents
        print("\n🔍 Testing Research Agent...")
        research_result = orchestrator.research_agent.research_company(query)
        print(f"✅ Research Agent Response Length: {len(research_result)} characters")
        print(f"📋 First 200 chars: {research_result[:200]}...")
        
        print("\n📊 Testing Analysis Agent...")
        analysis_result = orchestrator.analysis_agent.analyze_data(query)
        print(f"✅ Analysis Agent Response Length: {len(analysis_result)} characters")
        print(f"📋 First 200 chars: {analysis_result[:200]}...")
        
        print("\n💡 Testing Recommendation Agent...")
        recommendation_result = orchestrator.recommendation_agent.generate_recommendation(query)
        print(f"✅ Recommendation Agent Response Length: {len(recommendation_result)} characters")
        print(f"📋 First 200 chars: {recommendation_result[:200]}...")
        
        print("\n🎯 Testing Full Orchestrated Analysis...")
        full_result = orchestrator.orchestrate_analysis(query)
        
        if 'error' in full_result:
            print(f"❌ Error in orchestrated analysis: {full_result['error']}")
        else:
            analysis_length = len(full_result.get('analysis', ''))
            print(f"✅ Full Analysis Response Length: {analysis_length} characters")
            print(f"📋 Analysis preview: {full_result.get('analysis', '')[:300]}...")
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agents()
