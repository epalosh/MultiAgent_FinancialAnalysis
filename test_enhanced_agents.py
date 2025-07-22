#!/usr/bin/env python3
"""
Test script for Enhanced Financial Analysis Agent with Real Data
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.agents.financial_orchestrator import FinancialOrchestrator

def test_enhanced_research():
    """Test enhanced research agent with real data"""
    print("🔍 Testing Enhanced Research Agent with Real Data")
    print("=" * 60)
    
    try:
        orchestrator = FinancialOrchestrator()
        
        # Test with Apple
        test_symbol = "AAPL"
        print(f"Testing with {test_symbol}...")
        
        result = orchestrator.enhanced_research_agent.research_company(test_symbol)
        
        print(f"✅ Research completed - {len(result)} characters")
        print("\n📊 Sample Output:")
        print(result[:500] + "..." if len(result) > 500 else result)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_enhanced_analysis():
    """Test enhanced analysis agent"""
    print("\n🔍 Testing Enhanced Analysis Agent")
    print("=" * 60)
    
    try:
        orchestrator = FinancialOrchestrator()
        
        # First get research data
        research_data = orchestrator.enhanced_research_agent.research_company("MSFT")
        
        # Then analyze it
        analysis_result = orchestrator.enhanced_analysis_agent.analyze_financial_data(research_data)
        
        print(f"✅ Analysis completed - {len(analysis_result)} characters")
        print("\n📊 Sample Output:")
        print(analysis_result[:500] + "..." if len(analysis_result) > 500 else analysis_result)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_quick_analysis():
    """Test quick analysis functionality"""
    print("\n🔍 Testing Quick Analysis")
    print("=" * 60)
    
    try:
        orchestrator = FinancialOrchestrator()
        
        result = orchestrator.enhanced_research_agent.get_quick_analysis("GOOGL")
        
        print(f"✅ Quick analysis completed - {len(result)} characters")
        print("\n📊 Quick Analysis Output:")
        print(result)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_stock_comparison():
    """Test stock comparison functionality"""
    print("\n🔍 Testing Stock Comparison")
    print("=" * 60)
    
    try:
        orchestrator = FinancialOrchestrator()
        
        stocks = ["AAPL", "MSFT", "GOOGL"]
        result = orchestrator.enhanced_analysis_agent.compare_stocks(stocks)
        
        print(f"✅ Stock comparison completed - {len(result)} characters")
        print("\n📊 Sample Comparison Output:")
        print(result[:500] + "..." if len(result) > 500 else result)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_enhanced_orchestration():
    """Test full enhanced orchestration"""
    print("\n🔍 Testing Enhanced Orchestration")
    print("=" * 60)
    
    try:
        orchestrator = FinancialOrchestrator()
        
        query = "Tesla (TSLA)"
        result = orchestrator.orchestrate_analysis(query)
        
        if result.get('success'):
            print(f"✅ Enhanced orchestration completed successfully")
            print(f"📊 Total length: {result.get('total_length')} characters")
            print(f"🔧 Agents used: {result.get('agents_used')}")
            print(f"📈 Data sources: {result.get('data_sources')}")
            print("\n📋 Sample Final Report:")
            analysis = result.get('analysis', '')
            print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
        else:
            print(f"❌ Enhanced orchestration failed: {result.get('error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_data_service():
    """Test the enhanced data service directly"""
    print("\n🔍 Testing Enhanced Data Service")
    print("=" * 60)
    
    try:
        from backend.services.enhanced_financial_data_service import EnhancedFinancialDataService
        
        data_service = EnhancedFinancialDataService()
        
        # Test comprehensive data fetch
        result = data_service.get_comprehensive_stock_data("NVDA")
        
        if "error" in result:
            print(f"❌ Data service error: {result['error']}")
            return False
        
        print(f"✅ Data service working - Retrieved data for NVDA")
        print(f"📊 Data sections: {list(result.keys())}")
        print(f"💰 Current price: ${result.get('price_data', {}).get('current_price', 'N/A')}")
        print(f"🏢 Company: {result.get('basic_info', {}).get('company_name', 'N/A')}")
        print(f"📈 Market cap: ${result.get('basic_info', {}).get('market_cap', 0):,.0f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Enhanced Financial Analysis System Tests")
    print("=" * 60)
    
    tests = [
        ("Data Service", test_data_service),
        ("Enhanced Research", test_enhanced_research),
        ("Enhanced Analysis", test_enhanced_analysis),
        ("Quick Analysis", test_quick_analysis),
        ("Stock Comparison", test_stock_comparison),
        ("Enhanced Orchestration", test_enhanced_orchestration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {str(e)}")
    
    print(f"\n🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced financial analysis system is ready.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
