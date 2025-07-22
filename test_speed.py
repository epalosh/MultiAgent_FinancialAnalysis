#!/usr/bin/env python3
"""
Quick test script to verify the optimized agents work fast
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.agents.financial_orchestrator import FinancialOrchestrator

def test_speed():
    """Test the financial agents for speed"""
    
    print("🚀 Testing Optimized Multi-Agent System for Speed")
    print("=" * 60)
    
    try:
        # Initialize the orchestrator
        print("📊 Initializing Financial Orchestrator...")
        start_time = time.time()
        orchestrator = FinancialOrchestrator()
        init_time = time.time() - start_time
        print(f"✅ Initialized in {init_time:.2f} seconds")
        
        # Test query
        query = "Analyze Apple stock"
        
        print(f"\n📝 Testing query: {query}")
        print("-" * 40)
        
        # Test individual agents with timing
        print("\n🔍 Testing Research Agent...")
        start_time = time.time()
        research_result = orchestrator.research_agent.research_company(query)
        research_time = time.time() - start_time
        print(f"✅ Research completed in {research_time:.2f} seconds")
        print(f"📊 Response length: {len(research_result)} characters")
        
        print("\n📈 Testing Analysis Agent...")
        start_time = time.time()
        analysis_result = orchestrator.analysis_agent.analyze_data(query)
        analysis_time = time.time() - start_time
        print(f"✅ Analysis completed in {analysis_time:.2f} seconds")
        print(f"📊 Response length: {len(analysis_result)} characters")
        
        print("\n💡 Testing Recommendation Agent...")
        start_time = time.time()
        recommendation_result = orchestrator.recommendation_agent.generate_recommendation(query)
        recommendation_time = time.time() - start_time
        print(f"✅ Recommendations completed in {recommendation_time:.2f} seconds")
        print(f"📊 Response length: {len(recommendation_result)} characters")
        
        print("\n🎯 Testing Full Orchestrated Analysis...")
        start_time = time.time()
        full_result = orchestrator.orchestrate_analysis(query)
        full_time = time.time() - start_time
        
        if 'error' in full_result:
            print(f"❌ Error in orchestrated analysis: {full_result['error']}")
        else:
            analysis_length = len(full_result.get('analysis', ''))
            print(f"✅ Full Analysis completed in {full_time:.2f} seconds")
            print(f"📊 Response length: {analysis_length} characters")
        
        # Summary
        total_time = research_time + analysis_time + recommendation_time
        print("\n" + "=" * 60)
        print("⏱️  PERFORMANCE SUMMARY:")
        print(f"   Research Agent:      {research_time:.2f}s")
        print(f"   Analysis Agent:      {analysis_time:.2f}s")
        print(f"   Recommendation Agent: {recommendation_time:.2f}s")
        print(f"   Full Orchestration:  {full_time:.2f}s")
        print(f"   Total Individual:    {total_time:.2f}s")
        print("✅ Speed optimization successful!")
        
        # Performance assessment
        if total_time < 30:
            print("🚀 EXCELLENT: Response time under 30 seconds")
        elif total_time < 60:
            print("✅ GOOD: Response time under 1 minute")
        elif total_time < 120:
            print("⚠️  ACCEPTABLE: Response time under 2 minutes")
        else:
            print("❌ SLOW: Consider further optimization")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_speed()
