#!/usr/bin/env python3
"""
Simple test to verify yfinance and enhanced data service
"""

def test_yfinance():
    print("Testing yfinance...")
    try:
        import yfinance as yf
        ticker = yf.Ticker('AAPL')
        info = ticker.info
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
        print(f"✅ yfinance working! AAPL current price: ${current_price}")
        return True
    except Exception as e:
        print(f"❌ yfinance error: {e}")
        return False

def test_enhanced_service():
    print("\nTesting enhanced data service...")
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        
        from backend.services.enhanced_financial_data_service import EnhancedFinancialDataService
        
        service = EnhancedFinancialDataService()
        result = service.get_comprehensive_stock_data('AAPL')
        
        if "error" in result:
            print(f"❌ Data service error: {result['error']}")
            return False
        
        price = result.get('price_data', {}).get('current_price', 'N/A')
        company = result.get('basic_info', {}).get('company_name', 'N/A')
        
        print(f"✅ Enhanced data service working!")
        print(f"   Company: {company}")
        print(f"   Current price: ${price}")
        print(f"   Data sections: {len(result)} categories")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced service error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Enhanced Financial Analysis Components")
    print("=" * 50)
    
    yf_ok = test_yfinance()
    service_ok = test_enhanced_service()
    
    print("\n" + "=" * 50)
    if yf_ok and service_ok:
        print("🎉 All tests passed! System ready for enhanced analysis.")
    else:
        print("⚠️ Some components need attention.")
