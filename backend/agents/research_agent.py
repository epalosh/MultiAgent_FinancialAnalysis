from langchain.llms.base import BaseLLM
from langchain.schema import HumanMessage
from typing import Any, Dict
import json
import sys
import os
import re

# Add the services directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.financial_data_service import FinancialDataService

class ResearchAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.name = "Research Agent"
        self.data_service = FinancialDataService()
    
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
            r'\b([A-Z]{3,5})\b'  # 3-5 letter uppercase words
        ]
        
        for pattern in patterns:
            match = re.search(pattern, company_info.upper())
            if match:
                return match.group(1)
        
        # If no symbol found, try common company name mappings
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
            'BROADCOM': 'AVGO'
        }
        
        company_upper = company_info.upper()
        for company_name, symbol in company_mappings.items():
            if company_name in company_upper:
                return symbol
                
        return None
    
    def research_company(self, company_info: str) -> str:
        """
        Research comprehensive financial information about a company using real data
        """
        try:
            # Extract stock symbol
            symbol = self._extract_stock_symbol(company_info)
            
            if not symbol:
                return f"🔍 Unable to identify stock symbol from: {company_info}. Please provide a valid stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
            
            # Get comprehensive real data
            print(f"🔄 Fetching real financial data for {symbol}...")
            real_data = self.data_service.get_comprehensive_stock_data(symbol)
            
            if "error" in real_data:
                return f"❌ Error fetching data for {symbol}: {real_data['error']}"
            
            # Format the real data for analysis
            formatted_data = self._format_real_data_for_analysis(real_data)
            
            prompt = f"""
            You are a senior financial research analyst. You have been provided with REAL, CURRENT financial data for {symbol}.
            
            CRITICAL: This is REAL DATA from live financial sources. Use these EXACT numbers in your analysis.
            
            REAL FINANCIAL DATA:
            {formatted_data}
            
            Generate a comprehensive professional financial research report using this REAL DATA:

            # FINANCIAL RESEARCH REPORT: {real_data.get('basic_info', {}).get('company_name', symbol)}

            ## EXECUTIVE SUMMARY
            - Company: {real_data.get('basic_info', {}).get('company_name', 'N/A')} (Ticker: {symbol})
            - Sector: {real_data.get('basic_info', {}).get('sector', 'N/A')}
            - Industry: {real_data.get('basic_info', {}).get('industry', 'N/A')}
            - Market Cap: ${real_data.get('basic_info', {}).get('market_cap', 0):,.0f}
            - Current Stock Price: ${real_data.get('price_data', {}).get('current_price', 0):.2f}
            - Investment Grade: [Analyze based on the real financial metrics provided]

            ## FINANCIAL PERFORMANCE ANALYSIS

            ### Current Stock Performance
            **Price Performance:**
            - Current Price: ${real_data.get('price_data', {}).get('current_price', 0):.2f}
            - 52-Week High: ${real_data.get('price_data', {}).get('52_week_high', 0):.2f}
            - 52-Week Low: ${real_data.get('price_data', {}).get('52_week_low', 0):.2f}
            - Distance from 52W High: {real_data.get('price_data', {}).get('price_from_52w_high', 0):.1f}%
            
            **Returns Analysis:**
            Use the REAL return data provided: {real_data.get('price_data', {}).get('returns', {})}

            ### Financial Strength Analysis
            Use the REAL financial statement data provided to analyze:
            - Revenue and profitability trends
            - Balance sheet strength
            - Cash flow generation
            - Debt levels and capital structure

            ## VALUATION ANALYSIS

            ### Key Valuation Metrics (REAL DATA)
            Use these EXACT valuation metrics from the real data:
            {self._format_valuation_metrics(real_data.get('valuation_metrics', {}))}

            ### Market Context
            Compare performance against:
            - S&P 500 1-Year Return: {real_data.get('market_data', {}).get('sp500_1y_return', 'N/A')}%
            - NASDAQ 1-Year Return: {real_data.get('market_data', {}).get('nasdaq_1y_return', 'N/A')}%
            - Current VIX (Fear Index): {real_data.get('market_data', {}).get('vix_current', 'N/A')}

            ## RISK ASSESSMENT

            ### Risk Metrics (REAL DATA)
            - Beta: {real_data.get('risk_metrics', {}).get('beta', 'N/A')}
            - Volatility (1Y): {real_data.get('risk_metrics', {}).get('volatility', 'N/A')}%
            - Maximum Drawdown: {real_data.get('risk_metrics', {}).get('max_drawdown', 'N/A')}%
            - Sharpe Ratio: {real_data.get('risk_metrics', {}).get('sharpe_ratio', 'N/A')}

            ### Peer Comparison
            Main Competitors: {self._format_peer_data(real_data.get('peer_comparison', {}))}

            ## ANALYST CONSENSUS & MARKET SENTIMENT

            ### Recent Analyst Activity
            {self._format_analyst_data(real_data.get('analyst_data', {}))}

            ### Recent News Impact
            {self._format_news_data(real_data.get('news_data', {}))}

            ## INVESTMENT RECOMMENDATION

            Based on the REAL financial data analysis, provide:
            1. **Investment Rating**: [BUY/HOLD/SELL] with confidence level
            2. **Key Strengths**: Based on actual financial metrics
            3. **Key Risks**: Based on real risk analysis
            4. **Price Target Rationale**: Using real valuation metrics
            5. **Investment Horizon**: Short/Medium/Long term outlook

            ## DATA QUALITY & RECENCY

            - Data Source: Live financial markets via Yahoo Finance and multiple APIs
            - Last Updated: {real_data.get('data_timestamp', 'N/A')}
            - Coverage: {len(real_data)} major data categories analyzed

            IMPORTANT: 
            - Use ONLY the real numbers provided - no placeholder values
            - All calculations must be based on the actual financial data
            - Provide specific, actionable insights based on real metrics
            - Include risk warnings where appropriate based on actual data
            """
            
            result = self._call_llm(prompt)
            
            return f"🔍 REAL-TIME FINANCIAL RESEARCH ({symbol}):\n\n{result}"
            
        except Exception as e:
            return f"Research Agent error: {str(e)}"
    
    def _format_real_data_for_analysis(self, data: Dict) -> str:
        """Format real data for LLM analysis"""
        formatted = []
        
        # Basic company info
        if 'basic_info' in data:
            formatted.append(f"COMPANY: {data['basic_info']}")
        
        # Price performance
        if 'price_data' in data:
            formatted.append(f"PRICE DATA: {data['price_data']}")
        
        # Financial statements
        if 'financial_statements' in data:
            formatted.append(f"FINANCIAL STATEMENTS: {data['financial_statements']}")
        
        # Valuation metrics
        if 'valuation_metrics' in data:
            formatted.append(f"VALUATION: {data['valuation_metrics']}")
        
        # Risk metrics
        if 'risk_metrics' in data:
            formatted.append(f"RISK METRICS: {data['risk_metrics']}")
        
        # Market context
        if 'market_data' in data:
            formatted.append(f"MARKET CONTEXT: {data['market_data']}")
        
        return "\n\n".join(formatted)
    
    def _format_valuation_metrics(self, metrics: Dict) -> str:
        """Format valuation metrics for display"""
        if not metrics:
            return "Valuation data not available"
        
        formatted = []
        formatted.append(f"- P/E Ratio (TTM): {metrics.get('pe_ratio', 'N/A')}")
        formatted.append(f"- Forward P/E: {metrics.get('forward_pe', 'N/A')}")
        formatted.append(f"- PEG Ratio: {metrics.get('peg_ratio', 'N/A')}")
        formatted.append(f"- Price-to-Book: {metrics.get('price_to_book', 'N/A')}")
        formatted.append(f"- Price-to-Sales: {metrics.get('price_to_sales', 'N/A')}")
        formatted.append(f"- EV/EBITDA: {metrics.get('ev_to_ebitda', 'N/A')}")
        formatted.append(f"- Enterprise Value: ${metrics.get('enterprise_value', 0):,.0f}")
        
        if metrics.get('dividend_yield', 0) > 0:
            formatted.append(f"- Dividend Yield: {metrics.get('dividend_yield', 0):.2f}%")
            formatted.append(f"- Dividend Rate: ${metrics.get('dividend_rate', 0):.2f}")
            formatted.append(f"- Payout Ratio: {metrics.get('payout_ratio', 0):.1f}%")
        
        return "\n".join(formatted)
    
    def _format_peer_data(self, peer_data: Dict) -> str:
        """Format peer comparison data"""
        if not peer_data or 'peers' not in peer_data:
            return "Peer data not available"
        
        peers = peer_data.get('peers', [])
        peer_metrics = peer_data.get('peer_metrics', [])
        
        if not peer_metrics:
            return f"Sector peers: {', '.join(peers)}"
        
        formatted = []
        for peer in peer_metrics:
            market_cap = peer.get('market_cap', 0)
            pe_ratio = peer.get('pe_ratio', 0)
            formatted.append(f"{peer.get('symbol')}: ${market_cap:,.0f} market cap, P/E {pe_ratio:.1f}")
        
        return " | ".join(formatted)
    
    def _format_analyst_data(self, analyst_data: Dict) -> str:
        """Format analyst recommendation data"""
        if not analyst_data:
            return "Analyst data not available"
        
        recommendations = analyst_data.get('recommendations', {})
        if recommendations:
            rec_summary = []
            for grade, count in recommendations.items():
                rec_summary.append(f"{grade}: {count}")
            return f"Recent Recommendations: {' | '.join(rec_summary)}"
        
        return f"Latest: {analyst_data.get('latest_recommendation', 'N/A')}"
    
    def _format_news_data(self, news_data: Dict) -> str:
        """Format recent news data"""
        if not news_data or 'recent_news' not in news_data:
            return "Recent news data not available"
        
        news_count = news_data.get('news_count', 0)
        recent_news = news_data.get('recent_news', [])
        
        if recent_news:
            latest_headline = recent_news[0].get('title', 'N/A')
            return f"Recent News Coverage: {news_count} articles tracked. Latest: '{latest_headline}'"
        
        return f"{news_count} recent news articles tracked"
    
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
📊 REAL-TIME MARKET DATA for {symbol}:

Company: {basic_info.get('company_name', 'N/A')}
Current Price: ${price_data.get('current_price', 0):.2f}
52-Week Range: ${price_data.get('52_week_low', 0):.2f} - ${price_data.get('52_week_high', 0):.2f}
Market Cap: ${basic_info.get('market_cap', 0):,.0f}

Performance:
- 1 Month: {price_data.get('returns', {}).get('1_month', 'N/A')}%
- 1 Year: {price_data.get('returns', {}).get('1_year', 'N/A')}%
- 5 Year: {price_data.get('returns', {}).get('5_year', 'N/A')}%

Volatility: {price_data.get('volatility_1y', 'N/A')}%
Average Volume: {price_data.get('trading_volume_avg', 0):,}
            """
            
        except Exception as e:
            return f"Error getting market data: {str(e)}"
        """
        Research comprehensive financial information about a company
        """
        try:
            prompt = f"""
            You are a senior financial research analyst. Conduct comprehensive financial research on: {company_info}

            IMPORTANT: Generate REALISTIC, SPECIFIC financial data. Do NOT use placeholder formats like "XX.X" or "XXX.XX". 
            Use actual realistic numbers that would be typical for companies in this sector.

            If this is a real company (Apple, Microsoft, Tesla, etc.), use approximate recent data based on your knowledge.
            If this is a general sector/industry question, create realistic representative data for a typical large-cap company in that sector.

            Provide a detailed professional financial research report with REALISTIC DATA and NUMBERS:

            # FINANCIAL RESEARCH REPORT

            ## EXECUTIVE SUMMARY
            - Company: [Full Name] (Ticker: [SYMBOL])
            - Sector: [Specific Industry Sector]
            - Market Cap: $[realistic number] billion 
            - Current Stock Price: $[realistic price] (+/- [realistic %]% YTD)
            - Investment Grade: [A+/A/B+/B/C] - [Brief one-sentence thesis]

            ## FINANCIAL PERFORMANCE ANALYSIS

            ### Revenue & Profitability (Recent Performance)
            **Revenue Growth:**
            - Current Year: $[realistic] billion (+[realistic]% YoY)
            - Previous Year: $[realistic] billion (+[realistic]% YoY) 
            - Year Before: $[realistic] billion (+[realistic]% YoY)
            - 3-Year CAGR: [realistic]%

            **Profitability Metrics:**
            - Gross Margin: [realistic]% (vs industry avg [realistic]%)
            - Operating Margin: [realistic]% (trend: improving/stable/declining)
            - Net Profit Margin: [realistic]%
            - ROE (Return on Equity): [realistic]%
            - ROA (Return on Assets): [realistic]%
            - ROIC (Return on Invested Capital): [realistic]%

            ### Balance Sheet Strength
            **Assets & Capital Structure:**
            - Total Assets: $[realistic] billion
            - Total Debt: $[realistic] billion
            - Cash & Cash Equivalents: $[realistic] billion
            - Debt-to-Equity Ratio: [realistic decimal]
            - Current Ratio: [realistic decimal]
            - Quick Ratio: [realistic decimal]
            - Interest Coverage Ratio: [realistic decimal]

            **Working Capital Analysis:**
            - Working Capital: $[realistic] billion
            - Days Sales Outstanding: [realistic] days
            - Inventory Turnover: [realistic] times
            - Free Cash Flow: $[realistic] billion

            ## VALUATION ANALYSIS

            ### Key Valuation Metrics
            - P/E Ratio (TTM): [realistic] (vs industry [realistic])
            - Forward P/E: [realistic]
            - PEG Ratio: [realistic decimal]
            - Price-to-Book: [realistic decimal]
            - Price-to-Sales: [realistic decimal]
            - EV/EBITDA: [realistic]
            - Enterprise Value: $[realistic] billion

            ### Dividend Analysis (if applicable)
            - Dividend Yield: [realistic]%
            - Dividend Payout Ratio: [realistic]%
            - 5-Year Dividend Growth Rate: [realistic]%
            - Dividend Coverage Ratio: [realistic decimal]

            ## MARKET POSITION & COMPETITIVE ANALYSIS

            ### Market Leadership
            - Market Share: [realistic]% (Rank #[realistic number] in industry)
            - Geographic Revenue Mix: [realistic]% domestic, [realistic]% international
            - Revenue by Segment: [List segments with realistic percentages]

            ### Competitive Landscape
            **Main Competitors with Approximate Market Caps:**
            1. [Competitor 1]: $[realistic] billion market cap
            2. [Competitor 2]: $[realistic] billion market cap  
            3. [Competitor 3]: $[realistic] billion market cap

            **Competitive Advantages:**
            - [Specific advantage 1 with quantifiable impact]
            - [Specific advantage 2 with quantifiable impact]
            - [Specific advantage 3 with quantifiable impact]

            **Moat Rating:** [Wide/Narrow/None] - [Specific justification with examples]

            ## RECENT DEVELOPMENTS

            ### Performance Highlights
            - Recent Quarter Revenue: $[realistic] billion (vs est. $[realistic] billion)
            - EPS: $[realistic] (vs est. $[realistic])
            - Revenue Growth: +[realistic]% YoY
            - Key Business Highlights: [2-3 specific, realistic developments]

            ### Management Outlook
            - Current Year Revenue Guidance: $[realistic] - $[realistic] billion
            - EPS Guidance: $[realistic] - $[realistic]
            - Capital Expenditure Plans: $[realistic] billion
            - Strategic Focus Areas: [2-3 specific initiatives]

            ## RISK ASSESSMENT

            ### Business Risks Analysis
            - **Cyclical Risk**: [High/Medium/Low] - [Specific explanation with impact]
            - **Competitive Risk**: [High/Medium/Low] - [Specific threats and timeline]
            - **Regulatory Risk**: [High/Medium/Low] - [Specific regulations and impact]
            - **Operational Risk**: [High/Medium/Low] - [Specific operational challenges]
            - **Financial Risk**: [High/Medium/Low] - [Debt sustainability analysis]

            ### ESG Factors
            - ESG Rating: [Realistic score/rating]
            - Carbon Footprint: [Realistic emissions data if relevant]
            - Board Diversity: [realistic]% diverse directors
            - CEO/Employee Pay Ratio: [realistic number]:1

            ## ANALYST CONSENSUS

            ### Wall Street Coverage Summary
            - Number of Analysts: [realistic number] covering
            - Strong Buy: [realistic] | Buy: [realistic] | Hold: [realistic] | Sell: [realistic]
            - Average Price Target: $[realistic] ([realistic]% upside/downside)
            - High Target: $[realistic] | Low Target: $[realistic]

            ### Institutional Holdings
            - Institutional Ownership: [realistic]%
            - Top Institutional Holders: [List 3-5 with realistic % holdings]
            - Recent Insider Activity: [Net buying/selling with realistic amounts]

            CRITICAL REQUIREMENTS:
            1. Use REALISTIC numbers throughout - no placeholders
            2. Make numbers internally consistent (ratios should calculate correctly)
            3. Use industry-appropriate ranges for all metrics
            4. Include specific, actionable insights
            5. Provide quantitative support for all qualitative statements

            Generate comprehensive research that would be suitable for institutional investment decisions.
            """
            
            result = self._call_llm(prompt)
            
            return f"🔍 COMPREHENSIVE FINANCIAL RESEARCH:\n\n{result}"
            
        except Exception as e:
            return f"Research Agent error: {str(e)}"
    
    def get_market_data(self, symbol: str) -> str:
        """
        Get basic market data for a stock symbol
        """
        try:
            # This would integrate with a real data source in production
            return f"Market data for {symbol} - This would contain real-time pricing and basic metrics"
        except Exception as e:
            return f"Error getting market data: {str(e)}"
