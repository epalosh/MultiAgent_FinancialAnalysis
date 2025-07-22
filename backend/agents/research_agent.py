from langchain.llms.base import BaseLLM
from langchain.schema import HumanMessage
from typing import Any, Dict
import json

class ResearchAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.name = "Research Agent"
    
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
    
    def research_company(self, company_info: str) -> str:
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
