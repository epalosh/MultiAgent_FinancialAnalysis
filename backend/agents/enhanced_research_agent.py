from langchain.llms.base import BaseLLM
from langchain.schema import HumanMessage
from typing import Any, Dict, List
import json
import sys
import os
import re
from datetime import datetime

# Add the services directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.enhanced_financial_data_service import EnhancedFinancialDataService

class EnhancedResearchAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.name = "Enhanced Research Agent"
        self.data_service = EnhancedFinancialDataService()
    
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
    
    def _extract_stock_symbol(self, company_info: str) -> str:
        """Extract stock symbol from company information"""
        # Look for stock symbols in parentheses or after ticker/symbol keywords
        patterns = [
            r'\(([A-Z]{1,5})\)',  # Symbol in parentheses
            r'ticker[:\s]+([A-Z]{1,5})',  # After "ticker:"
            r'symbol[:\s]+([A-Z]{1,5})',  # After "symbol:"
            r'\b([A-Z]{1,5})\b'  # 1-5 letter uppercase words
        ]
        
        for pattern in patterns:
            match = re.search(pattern, company_info.upper())
            if match:
                potential_symbol = match.group(1)
                # Validate if it's a real stock symbol by checking with yfinance
                if self._validate_stock_symbol(potential_symbol):
                    return potential_symbol
        
        # If no direct symbol found, try common company name mappings
        company_mappings = {
            'APPLE': 'AAPL',
            'MICROSOFT': 'MSFT', 
            'GOOGLE': 'GOOGL',
            'ALPHABET': 'GOOGL',
            'AMAZON': 'AMZN',
            'TESLA': 'TSLA',
            'META': 'META',
            'FACEBOOK': 'META',
            'NETFLIX': 'NFLX',
            'NVIDIA': 'NVDA',
            'INTEL': 'INTC',
            'WALMART': 'WMT',
            'JOHNSON': 'JNJ',
            'VISA': 'V',
            'MASTERCARD': 'MA',
            'COCA-COLA': 'KO',
            'PEPSI': 'PEP',
            'DISNEY': 'DIS',
            'BOEING': 'BA',
            'CATERPILLAR': 'CAT',
            'GENERAL ELECTRIC': 'GE',
            'IBM': 'IBM',
            'ORACLE': 'ORCL',
            'SALESFORCE': 'CRM',
            'PAYPAL': 'PYPL',
            'ADOBE': 'ADBE',
            'CISCO': 'CSCO',
            'QUALCOMM': 'QCOM',
            'BROADCOM': 'AVGO',
            'BERKSHIRE': 'BRK-B',
            'JPMORGAN': 'JPM',
            'BANK OF AMERICA': 'BAC',
            'PROCTER': 'PG',
            'HOME DEPOT': 'HD',
            'MCDONALDS': 'MCD'
        }
        
        company_upper = company_info.upper()
        for company_name, symbol in company_mappings.items():
            if company_name in company_upper:
                # Validate the mapped symbol
                if self._validate_stock_symbol(symbol):
                    return symbol
                
        return None

    def _validate_stock_symbol(self, symbol: str) -> bool:
        """Validate if a stock symbol exists and has data available"""
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            # Try to get basic info - if it fails, symbol doesn't exist
            info = ticker.info
            # Check if we got meaningful data (not just empty dict)
            return info and 'symbol' in info or 'shortName' in info or 'longName' in info
        except Exception:
            return False
    
    def research_company(self, company_info: str) -> str:
        """
        Research comprehensive financial information about a company using REAL data
        """
        try:
            # Extract stock symbol
            symbol = self._extract_stock_symbol(company_info)
            
            if not symbol:
                # Try to suggest potential symbols if company name is provided
                suggestions = self._suggest_symbols(company_info)
                suggestion_text = f"\n\nDid you mean one of these? {', '.join(suggestions)}" if suggestions else ""
                return f"""Unable to identify a valid stock symbol from: "{company_info}"

Please provide:
1. A valid stock ticker symbol (e.g., AAPL, MSFT, GOOGL, TSLA)
2. Company name with ticker in parentheses (e.g., "Apple Inc. (AAPL)")
3. Any publicly traded stock symbol on major exchanges{suggestion_text}

The system can analyze ANY publicly traded stock with real-time data from Yahoo Finance."""
            
            # Get comprehensive real data
            print(f"Fetching real financial data for {symbol}...")
            real_data = self.data_service.get_comprehensive_stock_data(symbol)
            
            if "error" in real_data:
                return f"""Error fetching data for {symbol}: {real_data['error']}

This might mean:
1. {symbol} is not a valid/active stock ticker
2. The stock is delisted or suspended
3. Temporary data service issue

Please verify the ticker symbol and try again. The system supports all major exchanges (NYSE, NASDAQ, etc.)."""
            
            # Generate comprehensive analysis using real data
            analysis = self._generate_comprehensive_analysis(symbol, real_data)
            
            return f"**REAL-TIME FINANCIAL RESEARCH REPORT** ({symbol})\nData Updated: {real_data.get('data_timestamp', 'N/A')}\n\n{analysis}"
            
        except Exception as e:
            return f"Enhanced Research Agent error: {str(e)}"

    def _suggest_symbols(self, company_info: str) -> List[str]:
        """Suggest potential stock symbols based on partial company names"""
        # Extended company mappings for suggestions
        suggestions = []
        company_upper = company_info.upper()
        
        # Common partial matches
        partial_mappings = {
            'APPLE': ['AAPL'],
            'MICROSOFT': ['MSFT'],
            'GOOGLE': ['GOOGL', 'GOOG'], 
            'AMAZON': ['AMZN'],
            'TESLA': ['TSLA'],
            'META': ['META'],
            'FACEBOOK': ['META'],
            'NETFLIX': ['NFLX'],
            'NVIDIA': ['NVDA'],
            'AMD': ['AMD'],
            'INTEL': ['INTC'],
            'WALMART': ['WMT'],
            'TARGET': ['TGT'],
            'JOHNSON': ['JNJ'],
            'PFIZER': ['PFE'],
            'VISA': ['V'],
            'MASTERCARD': ['MA'],
            'COCA': ['KO'],
            'PEPSI': ['PEP'],
            'DISNEY': ['DIS'],
            'BOEING': ['BA'],
            'FORD': ['F'],
            'GM': ['GM'],
            'GENERAL MOTORS': ['GM'],
            'EXXON': ['XOM'],
            'CHEVRON': ['CVX'],
            'BANK': ['JPM', 'BAC', 'WFC', 'C'],
            'JPMORGAN': ['JPM'],
            'WELLS FARGO': ['WFC'],
            'HOME DEPOT': ['HD'],
            'LOWES': ['LOW'],
            'MCDONALDS': ['MCD'],
            'STARBUCKS': ['SBUX'],
            'ORACLE': ['ORCL'],
            'SALESFORCE': ['CRM'],
            'ADOBE': ['ADBE']
        }
        
        for keyword, symbols in partial_mappings.items():
            if keyword in company_upper:
                suggestions.extend(symbols)
        
        return list(set(suggestions))[:3]  # Return up to 3 unique suggestions
    
    def _generate_comprehensive_analysis(self, symbol: str, data: Dict) -> str:
        """Generate comprehensive analysis using real data"""
        
        basic_info = data.get('basic_info', {})
        price_data = data.get('price_data', {})
        financial_statements = data.get('financial_statements', {})
        valuation_metrics = data.get('valuation_metrics', {})
        risk_metrics = data.get('risk_metrics', {})
        market_data = data.get('market_data', {})
        analyst_data = data.get('analyst_data', {})
        news_data = data.get('news_data', {})
        peer_data = data.get('peer_comparison', {})
        
        # Build formatted data for LLM
        formatted_real_data = self._format_real_data_for_llm(data)
        
        prompt = f"""
        You are a senior financial research analyst with 20+ years of experience. You have been provided with REAL, CURRENT financial data for {symbol} from live market sources (Yahoo Finance, SEC filings, etc.).
        
        **CRITICAL INSTRUCTIONS:**
        1. This is REAL DATA from live financial sources - use these EXACT numbers in your analysis
        2. Do NOT use any placeholder values or made-up numbers
        3. Base ALL conclusions on the actual data provided
        4. If specific data is missing, clearly state "Data not available" rather than estimating
        5. Use professional financial analysis language and provide actionable insights

        Do not use emojis in your response.
        
        **REAL FINANCIAL DATA FOR {symbol}:**
        {formatted_real_data}
        
        Generate a comprehensive professional financial research report using ONLY this real data:

        # FINANCIAL RESEARCH REPORT: {basic_info.get('company_name', symbol)}
        
        ## EXECUTIVE SUMMARY
        **Company Overview:**
        - Company: {basic_info.get('company_name', 'N/A')} (Ticker: {symbol})
        - Sector: {basic_info.get('sector', 'N/A')}
        - Industry: {basic_info.get('industry', 'N/A')}
        - Employees: {basic_info.get('employees', 0):,}
        - Market Cap: ${valuation_metrics.get('market_cap', 0):,.0f}
        
        **Current Market Position:**
        - Current Stock Price: ${price_data.get('current_price', 0):.2f}
        - 52-Week Range: ${price_data.get('52_week_low', 0):.2f} - ${price_data.get('52_week_high', 0):.2f}
        - Distance from 52W High: {price_data.get('price_from_52w_high', 0):.1f}%
        
        **Investment Thesis:** [Provide 2-3 sentence summary based on the real financial metrics]

        ## FINANCIAL PERFORMANCE ANALYSIS

        ### Stock Performance Analysis
        **Recent Price Performance:**
        {self._format_returns_analysis(price_data.get('returns', {}))}
        
        **Volatility & Risk Profile:**
        - Annual Volatility: {risk_metrics.get('volatility', 0):.1f}%
        - Beta (vs S&P 500): {risk_metrics.get('beta', 0):.2f}
        - Maximum Drawdown: {risk_metrics.get('max_drawdown', 0):.1f}%
        - Sharpe Ratio: {risk_metrics.get('sharpe_ratio', 0):.2f}

        ### Financial Statement Analysis
        {self._format_financial_statements_analysis(financial_statements)}

        ## VALUATION ANALYSIS

        ### Key Valuation Metrics (REAL DATA)
        - P/E Ratio (TTM): {valuation_metrics.get('pe_ratio', 0):.1f}
        - Forward P/E: {valuation_metrics.get('forward_pe', 0):.1f}
        - PEG Ratio: {valuation_metrics.get('peg_ratio', 0):.2f}
        - Price-to-Book: {valuation_metrics.get('price_to_book', 0):.2f}
        - Price-to-Sales: {valuation_metrics.get('price_to_sales', 0):.2f}
        - EV/EBITDA: {valuation_metrics.get('ev_to_ebitda', 0):.1f}
        - Enterprise Value: ${valuation_metrics.get('enterprise_value', 0):,.0f}

        {self._format_dividend_analysis(valuation_metrics)}

        ## MARKET CONTEXT & PERFORMANCE

        ### Broader Market Comparison
        - S&P 500 1-Year Return: {market_data.get('sp500_1y_return', 'N/A'):.1f}%
        - NASDAQ 1-Year Return: {market_data.get('nasdaq_1y_return', 'N/A'):.1f}%
        - Current VIX (Market Fear): {market_data.get('vix_current', 'N/A'):.1f}

        ### Competitive Landscape
        **Sector Peers:** {', '.join(peer_data.get('peers', []))}
        **Industry:** {basic_info.get('industry', 'N/A')}

        ## MARKET SENTIMENT & ANALYSIS

        ### Analyst Coverage
        {self._format_analyst_coverage(analyst_data)}

        ### Recent Market Activity
        {self._format_recent_news(news_data)}

        ## RISK ASSESSMENT

        ### Financial Risk Metrics (REAL DATA)
        - Current Ratio: {risk_metrics.get('current_ratio', 0):.2f}
        - Debt-to-Equity: {risk_metrics.get('debt_to_equity', 0):.2f}
        - Beta: {risk_metrics.get('beta', 0):.2f} ({'Low' if risk_metrics.get('beta', 1) < 0.8 else 'Moderate' if risk_metrics.get('beta', 1) < 1.2 else 'High'} volatility vs market)
        - 95% Value at Risk: {risk_metrics.get('var_95', 0):.2f}%

        ### Investment Risk Analysis
        Based on the real financial data, analyze:
        1. **Liquidity Risk:** [Based on current ratio and cash position]
        2. **Leverage Risk:** [Based on debt-to-equity and interest coverage]
        3. **Market Risk:** [Based on beta and volatility]
        4. **Business Risk:** [Based on sector, margins, and competitive position]

        ## INVESTMENT RECOMMENDATION

        ### Professional Assessment
        **Rating:** [Provide BUY/HOLD/SELL based on real data analysis]
        **Confidence Level:** [High/Medium/Low based on data completeness]
        **Investment Horizon:** [Short/Medium/Long term recommendation]

        **Key Investment Strengths:** (Based on actual financial metrics)
        1. [Specific strength based on real data]
        2. [Specific strength based on real data]
        3. [Specific strength based on real data]

        **Key Investment Risks:** (Based on actual risk analysis)
        1. [Specific risk based on real data]
        2. [Specific risk based on real data]
        3. [Specific risk based on real data]

        **Price Target Rationale:** [Use real valuation metrics to justify]

        ## DATA QUALITY & METHODOLOGY

        **Data Sources:** Live market data via Yahoo Finance APIs
        **Last Updated:** {data.get('data_timestamp', 'N/A')}
        **Coverage:** Financial statements, market data, risk metrics, analyst coverage
        **Reliability:** Real-time market data with institutional-grade accuracy

        **Important Disclaimers:**
        - Analysis based on most recent available financial data
        - Past performance does not guarantee future results
        - Consider consulting with a financial advisor for investment decisions
        - Market conditions can change rapidly affecting all assessments

        ---
        *This report uses real financial data and professional analysis methodologies. All numbers are actual market values, not estimates or projections.*
        """
        
        result = self._call_llm(prompt)
        return result
    
    def _format_real_data_for_llm(self, data: Dict) -> str:
        """Format real data comprehensively for LLM"""
        sections = []
        
        if 'basic_info' in data:
            sections.append(f"COMPANY INFO: {json.dumps(data['basic_info'], indent=2)}")
        
        if 'price_data' in data:
            sections.append(f"PRICE & PERFORMANCE DATA: {json.dumps(data['price_data'], indent=2)}")
        
        if 'financial_statements' in data:
            sections.append(f"FINANCIAL STATEMENTS: {json.dumps(data['financial_statements'], indent=2)}")
        
        if 'valuation_metrics' in data:
            sections.append(f"VALUATION METRICS: {json.dumps(data['valuation_metrics'], indent=2)}")
        
        if 'risk_metrics' in data:
            sections.append(f"RISK METRICS: {json.dumps(data['risk_metrics'], indent=2)}")
        
        if 'market_data' in data:
            sections.append(f"MARKET CONTEXT: {json.dumps(data['market_data'], indent=2)}")
        
        return "\n\n".join(sections)
    
    def _format_returns_analysis(self, returns: Dict) -> str:
        """Format returns data for analysis"""
        if not returns:
            return "Returns data not available"
        
        formatted = []
        period_names = {
            '1_day': '1 Day',
            '5_day': '5 Day', 
            '1_month': '1 Month',
            '3_month': '3 Month',
            '6_month': '6 Month',
            '1_year': '1 Year',
            '2_year': '2 Year'
        }
        
        for period, name in period_names.items():
            if period in returns:
                value = returns[period]
                formatted.append(f"- {name}: {value:+.2f}%")
        
        return "\n".join(formatted) if formatted else "Returns data not available"
    
    def _format_financial_statements_analysis(self, financial_statements: Dict) -> str:
        """Format financial statements for analysis"""
        if not financial_statements:
            return "**Financial statement data not available**"
        
        sections = []
        
        # Income Statement
        if 'income_statement' in financial_statements:
            income = financial_statements['income_statement']
            sections.append(f"""**Income Statement Analysis:**
- Total Revenue: ${income.get('total_revenue', 0):,.0f}
- Gross Profit: ${income.get('gross_profit', 0):,.0f}
- Operating Income: ${income.get('operating_income', 0):,.0f}
- Net Income: ${income.get('net_income', 0):,.0f}
- EBITDA: ${income.get('ebitda', 0):,.0f}""")
        
        # Margins
        if 'margins' in financial_statements:
            margins = financial_statements['margins']
            sections.append(f"""**Profitability Margins:**
- Gross Margin: {margins.get('gross_margin', 0):.1f}%
- Operating Margin: {margins.get('operating_margin', 0):.1f}%
- Net Margin: {margins.get('net_margin', 0):.1f}%""")
        
        # Balance Sheet
        if 'balance_sheet' in financial_statements:
            balance = financial_statements['balance_sheet']
            sections.append(f"""**Balance Sheet Strength:**
- Total Assets: ${balance.get('total_assets', 0):,.0f}
- Total Debt: ${balance.get('total_debt', 0):,.0f}
- Cash & Equivalents: ${balance.get('cash_and_equivalents', 0):,.0f}
- Total Equity: ${balance.get('total_equity', 0):,.0f}
- Working Capital: ${balance.get('working_capital', 0):,.0f}""")
        
        # Cash Flow
        if 'cash_flow' in financial_statements:
            cash_flow = financial_statements['cash_flow']
            sections.append(f"""**Cash Flow Analysis:**
- Operating Cash Flow: ${cash_flow.get('operating_cash_flow', 0):,.0f}
- Free Cash Flow: ${cash_flow.get('free_cash_flow', 0):,.0f}
- Capital Expenditure: ${cash_flow.get('capital_expenditure', 0):,.0f}""")
        
        return "\n\n".join(sections) if sections else "Financial data not available"
    
    def _format_dividend_analysis(self, valuation_metrics: Dict) -> str:
        """Format dividend analysis"""
        dividend_yield = valuation_metrics.get('dividend_yield', 0)
        
        if dividend_yield > 0:
            return f"""
        ### Dividend Analysis
        - Dividend Yield: {dividend_yield:.2f}%
        - Annual Dividend Rate: ${valuation_metrics.get('dividend_rate', 0):.2f}
        - Payout Ratio: {valuation_metrics.get('payout_ratio', 0):.1f}%"""
        else:
            return "\n        ### Dividend Analysis\n        - No dividend currently paid"
    
    def _format_analyst_coverage(self, analyst_data: Dict) -> str:
        """Format analyst coverage data"""
        if not analyst_data or not analyst_data.get('recommendations'):
            return "Analyst coverage data not available"
        
        recommendations = analyst_data.get('recommendations', {})
        latest = analyst_data.get('latest_recommendation', 'N/A')
        
        rec_summary = []
        for grade, count in recommendations.items():
            rec_summary.append(f"{grade}: {count}")
        
        return f"Recent Analyst Recommendations: {' | '.join(rec_summary)}\nLatest Rating: {latest}"
    
    def _format_recent_news(self, news_data: Dict) -> str:
        """Format recent news data"""
        if not news_data or not news_data.get('recent_news'):
            return "Recent news data not available"
        
        news_count = news_data.get('news_count', 0)
        recent_news = news_data.get('recent_news', [])
        
        if recent_news:
            latest = recent_news[0]
            return f"Recent News Coverage: {news_count} articles tracked\nLatest Headline: \"{latest.get('title', 'N/A')}\" - {latest.get('publisher', 'N/A')}"
        
        return f"Recent news tracked: {news_count} articles"
    
    def get_quick_analysis(self, symbol: str) -> str:
        """Get quick financial analysis for a stock"""
        try:
            # Get fundamental data
            fundamentals = self.data_service.get_stock_fundamentals(symbol)
            if "error" in fundamentals:
                return f"{fundamentals['error']}"
            
            # Get technical indicators
            technical = self.data_service.get_technical_indicators(symbol)
            if "error" in technical:
                technical = {}
            
            # Format quick analysis
            analysis = f"""
**QUICK ANALYSIS: {symbol}**

**Key Fundamentals:**
- P/E Ratio: {fundamentals.get('pe_ratio', 0):.1f}
- Price-to-Book: {fundamentals.get('price_to_book', 0):.2f}
- ROE: {fundamentals.get('roe', 0):.1f}%
- Debt/Equity: {fundamentals.get('debt_to_equity', 0):.2f}
- Current Ratio: {fundamentals.get('current_ratio', 0):.2f}
- Profit Margin: {fundamentals.get('profit_margin', 0):.1f}%

**📈 Technical Position:**
- Current Price: ${technical.get('current_price', 0):.2f}
- vs 20-day MA: {technical.get('price_vs_sma20', 0):+.1f}%
- vs 50-day MA: {technical.get('price_vs_sma50', 0):+.1f}%
- vs 200-day MA: {technical.get('price_vs_sma200', 0):+.1f}%
- RSI: {technical.get('rsi', 50):.1f}

**💡 Quick Assessment:**
{self._generate_quick_assessment(fundamentals, technical)}
            """
            
            return analysis
            
        except Exception as e:
            return f"Error in quick analysis: {str(e)}"
    
    def _generate_quick_assessment(self, fundamentals: Dict, technical: Dict) -> str:
        """Generate quick investment assessment"""
        assessments = []
        
        # Valuation assessment
        pe_ratio = fundamentals.get('pe_ratio', 0)
        if pe_ratio > 0:
            if pe_ratio < 15:
                assessments.append("Potentially undervalued (low P/E)")
            elif pe_ratio > 25:
                assessments.append("Potentially overvalued (high P/E)")
            else:
                assessments.append("Fairly valued (moderate P/E)")
        
        # Financial health
        current_ratio = fundamentals.get('current_ratio', 0)
        if current_ratio > 1.5:
            assessments.append("Strong liquidity position")
        elif current_ratio < 1:
            assessments.append("Potential liquidity concerns")
        
        # Profitability
        roe = fundamentals.get('roe', 0)
        if roe > 15:
            assessments.append("Strong profitability (ROE > 15%)")
        elif roe < 5:
            assessments.append("Low profitability concerns")
        
        # Technical position
        if technical:
            price_vs_sma200 = technical.get('price_vs_sma200', 0)
            if price_vs_sma200 > 10:
                assessments.append("Strong technical momentum")
            elif price_vs_sma200 < -10:
                assessments.append("Weak technical position")
        
        return " | ".join(assessments) if assessments else "Mixed signals - requires deeper analysis"
    
    def get_market_data(self, symbol: str) -> str:
        """
        Get real-time market data for a stock symbol
        """
        try:
            data = self.data_service.get_comprehensive_stock_data(symbol)
            
            if "error" in data:
                return f"Error getting market data for {symbol}: {data['error']}"
            
            price_data = data.get('price_data', {})
            basic_info = data.get('basic_info', {})
            
            return f"""
📊 **REAL-TIME MARKET DATA: {symbol}**

**Company:** {basic_info.get('company_name', 'N/A')}
**Sector:** {basic_info.get('sector', 'N/A')}

**Current Trading:**
- Price: ${price_data.get('current_price', 0):.2f}
- Day Range: ${price_data.get('day_range_low', 0):.2f} - ${price_data.get('day_range_high', 0):.2f}
- Previous Close: ${price_data.get('previous_close', 0):.2f}
- Volume (Avg): {price_data.get('trading_volume_avg', 0):,}

**52-Week Performance:**
- High: ${price_data.get('52_week_high', 0):.2f}
- Low: ${price_data.get('52_week_low', 0):.2f}
- From High: {price_data.get('price_from_52w_high', 0):.1f}%

**Returns:**
{self._format_returns_analysis(price_data.get('returns', {}))}

**Market Cap:** ${basic_info.get('market_cap', 0):,.0f}
**Volatility (1Y):** {price_data.get('volatility_1y', 0):.1f}%
            """
            
        except Exception as e:
            return f"Error getting market data: {str(e)}"
