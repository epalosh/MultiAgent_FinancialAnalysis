from langchain.llms.base import BaseLLM
from typing import Any, Dict
from langchain.schema import HumanMessage
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
        Research comprehensive financial information about a company or financial topic
        """
        try:
            prompt = f"""
            As a financial research analyst, research the following: {company_info}
            
            Provide a focused research report (400-600 words) covering:

            ## Company Overview
            - Company identification (ticker, exchange, sector)
            - Business model and primary revenue streams
            - Market position and competitive landscape

            ## Financial Highlights
            - Key financial metrics (revenue, profit margins, debt levels)
            - Recent financial performance trends
            - Balance sheet strength indicators

            ## Market Analysis
            - Current stock performance and valuation
            - Peer comparison with key competitors
            - Industry trends and market conditions

            ## Recent Developments
            - Latest earnings results and guidance
            - Major strategic initiatives or announcements
            - Regulatory or market changes affecting the company

            ## Risk Factors
            - Primary business and financial risks
            - Industry and market risks
            - Competitive threats

            Be concise but include specific financial data, ratios, and percentages where available.
            """
            
            1. COMPREHENSIVE COMPANY/SECTOR IDENTIFICATION & OVERVIEW
            - Complete company identification with ticker symbol, exchange, and market classification
            - Detailed business model analysis including all revenue streams with percentage breakdown
            - Complete operational structure including subsidiaries, joint ventures, and partnerships
            - Comprehensive geographic presence analysis with revenue by region/country
            - Market capitalization analysis with float, insider ownership, and institutional holdings
            - Complete corporate structure including ownership, governance, and organizational hierarchy
            - Detailed industry classification (GICS, SIC codes) and sector positioning
            - Business lifecycle stage analysis (startup, growth, mature, decline)
            
            2. EXHAUSTIVE FINANCIAL PERFORMANCE ANALYSIS
            - Complete 5-year historical financial performance analysis:
              * Revenue analysis by segment, geography, and product line
              * Detailed profitability analysis (gross, operating, EBITDA, net margins)
              * Complete cash flow analysis (operating, investing, financing)
              * Balance sheet evolution analysis with key metrics trends
            - Comprehensive quarterly trend analysis for the last 12 quarters
            - Detailed seasonality and cyclicality patterns with quantitative analysis
            - Complete working capital management analysis and efficiency metrics
            - Detailed capital allocation history and ROI analysis
            - Comprehensive dividend/buyback history and policy analysis
            - Complete debt structure analysis including maturity profile and covenant details
            
            3. DETAILED FINANCIAL RATIOS & METRICS ANALYSIS
            - Complete liquidity ratio analysis:
              * Current ratio, quick ratio, cash ratio with 5-year trends
              * Operating cash flow to current liabilities analysis
              * Days sales outstanding, inventory turnover, payables period
            - Comprehensive profitability ratio analysis:
              * ROE, ROA, ROIC with DuPont analysis breakdown
              * Gross, operating, EBITDA, and net profit margins with trend analysis
              * Asset turnover ratios by category
            - Detailed leverage ratio analysis:
              * Debt-to-equity, debt-to-assets, interest coverage ratios
              * Financial leverage multiplier and debt service coverage
              * Credit metrics and rating implications
            - Complete valuation ratio analysis:
              * P/E (trailing, forward), PEG, P/B, P/S ratios
              * EV/EBITDA, EV/Sales, EV/FCF analysis
              * Dividend yield and payout ratio analysis
            
            4. COMPREHENSIVE MARKET POSITION & COMPETITIVE LANDSCAPE
            - Detailed market share analysis with historical trends and competitive positioning
            - Complete competitive landscape mapping including:
              * Direct competitors with detailed comparison
              * Indirect competitors and substitute products/services
              * Competitive advantages and moats analysis (economic, technological, regulatory)
              * Pricing power assessment and competitive dynamics
            - Comprehensive industry structure analysis (Porter's Five Forces):
              * Supplier bargaining power
              * Buyer bargaining power  
              * Threat of new entrants
              * Threat of substitutes
              * Competitive rivalry intensity
            - Detailed market size and growth analysis (TAM, SAM, SOM)
            - Complete value chain analysis and positioning
            - Comprehensive SWOT analysis with detailed implications
            
            5. EXHAUSTIVE RECENT DEVELOPMENTS & NEWS ANALYSIS
            - Complete earnings reports analysis for last 8 quarters:
              * Earnings surprises and guidance analysis
              * Management commentary themes and outlook
              * Analyst reaction and estimate revisions
              * Market reaction and volatility analysis
            - Detailed strategic initiatives analysis:
              * M&A activity and integration progress
              * New product launches and market reception
              * Geographic expansion and market entry strategies
              * Technology investments and digital transformation
            - Comprehensive management changes and corporate governance:
              * Leadership transitions and track records
              * Board composition and independence analysis
              * Executive compensation and alignment
              * Governance controversies or improvements
            - Complete regulatory and legal developments:
              * Regulatory approvals or setbacks
              * Legal proceedings and potential impacts
              * Compliance history and risk factors
            
            6. DETAILED MACROECONOMIC & INDUSTRY FACTORS
            - Comprehensive industry cyclicality and economic sensitivity analysis:
              * GDP correlation and elasticity analysis
              * Interest rate sensitivity and duration analysis
              * Inflation impact and pricing power assessment
              * Currency exposure and hedging strategies
            - Detailed macroeconomic scenario analysis:
              * Economic expansion scenario impacts
              * Recession scenario stress testing
              * Inflation scenario analysis
              * Interest rate cycle implications
            - Complete ESG factors and sustainability analysis:
              * Environmental impact and carbon footprint
              * Social responsibility and stakeholder management
              * Governance quality and board effectiveness
              * Regulatory ESG compliance and future requirements
            - Comprehensive geopolitical and regulatory risk analysis
            
            7. DETAILED TECHNICAL AND QUANTITATIVE ANALYSIS
            - Complete stock price performance analysis:
              * 1, 3, 6 month, 1, 3, 5 year performance vs benchmarks
              * Volatility analysis and risk-adjusted returns
              * Technical indicators and chart patterns
              * Support and resistance levels analysis
            - Comprehensive trading volume and liquidity analysis:
              * Average daily volume trends
              * Bid-ask spreads and market depth
              * Institutional ownership changes
              * Short interest and days to cover analysis
            
            8. MANAGEMENT QUALITY & CORPORATE GOVERNANCE ASSESSMENT
            - Detailed management team analysis:
              * CEO and C-suite track records and experience
              * Management tenure and succession planning
              * Previous company performance and value creation
              * Communication quality and transparency
            - Comprehensive corporate governance evaluation:
              * Board independence and expertise
              * Audit committee effectiveness
              * Shareholder rights and activism history
              * Executive compensation alignment
            
            9. COMPLETE PEER COMPARISON AND BENCHMARKING
            - Detailed peer group selection and rationale
            - Comprehensive financial metrics comparison:
              * Profitability metrics vs peers
              * Valuation multiples relative analysis
              * Growth rates comparison
              * Capital allocation efficiency
            - Complete operational benchmarking:
              * Market share trends vs competitors
              * Operational efficiency metrics
              * Innovation and R&D comparison
              * Customer satisfaction and retention
            
            10. FORWARD-LOOKING ANALYSIS AND PROJECTIONS
            - Detailed future growth drivers and catalysts:
              * Product pipeline and launch schedule
              * Market expansion opportunities
              * Operational leverage and margin expansion potential
              * Strategic initiatives and their expected impact
            - Comprehensive risk factors and potential headwinds:
              * Industry headwinds and competitive threats
              * Regulatory and legal risks
              * Execution risks and operational challenges
              * Macroeconomic sensitivity and scenario analysis
            
            Provide extensive quantitative data, specific percentages, dollar amounts, growth rates, and ratios throughout the analysis. Include detailed calculations and show your analytical reasoning. This should be an exhaustive institutional-quality research report of at least 2500-3500 words.
            
            Format your response as a structured research report with clear sections and subsections for easy navigation and analysis.
            """
            
            result = self._call_llm(prompt)
            
            return f"📊 COMPREHENSIVE FINANCIAL RESEARCH REPORT & DETAILED ANALYSIS:\n\n{result}"
            
        except Exception as e:
            return f"Research Agent error: {str(e)}"
    
    def get_market_data(self, symbol: str) -> str:
        """
        Get market data for a stock symbol
        """
        # In a real implementation, this would connect to a financial API
        return f"Mock market data for {symbol}: Current price $100, Volume: 1M shares, P/E: 15.5"
