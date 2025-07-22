#!/usr/bin/env python3
"""
Simple test script to verify the multi-agent system setup
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_configuration():
    """Test if configuration is loaded correctly"""
    try:
        import config
        print("✅ Configuration loaded successfully")
        print(f"   API Key configured: {'Yes' if config.OPENAI_API_KEY != 'your-openai-api-key-here' else 'No - Please configure!'}")
        print(f"   Model: {config.OPENAI_MODEL}")
        print(f"   Flask Port: {config.FLASK_PORT}")
        return config.OPENAI_API_KEY != 'your-openai-api-key-here'
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_agent_imports():
    """Test if agents can be imported"""
    try:
        from agents.financial_orchestrator import FinancialOrchestrator
        from agents.enhanced_research_agent import EnhancedResearchAgent
        from agents.enhanced_analysis_agent import EnhancedAnalysisAgent
        from agents.recommendation_agent import RecommendationAgent
        print("✅ All enhanced agent classes imported successfully")
        return True
    except Exception as e:
        print(f"❌ Agent import error: {e}")
        return False

def test_flask_app():
    """Test if Flask app can be imported"""
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        import app
        print("✅ Flask app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def main():
    print("🧪 Testing Multi-Agent Financial Analysis System")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Agent Imports", test_agent_imports),
        ("Flask App", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready to use.")
        print("\n📝 Next steps:")
        print("1. Make sure you've configured your OpenAI API key in backend/config.py")
        print("2. Run the backend: cd backend && python app.py")
        print("3. Run the frontend: cd frontend && npm start")
    else:
        print("⚠️  Some tests failed. Please check the setup.")
        
    if not test_configuration():
        print("\n🔧 To configure your API key:")
        print("   Edit backend/config.py and replace 'your-openai-api-key-here' with your actual OpenAI API key")

if __name__ == "__main__":
    main()
