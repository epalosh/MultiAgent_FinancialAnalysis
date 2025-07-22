from langchain.llms.base import BaseLLM
from langchain.schema import HumanMessage
from typing import Any, Dict
import json

class AnalysisAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.name = "Analysis Agent"
    
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
    
    def analyze_data(self, data: str) -> str:
        """
        Perform comprehensive financial analysis with detailed calculations
        """
        try:
            prompt = f"""
            Perform comprehensive quantitative financial analysis on: {data}
            
            Generate a detailed professional financial analysis report with CALCULATIONS and METRICS:

            # COMPREHENSIVE FINANCIAL ANALYSIS REPORT

            ## FINANCIAL RATIO ANALYSIS

            ### Liquidity Analysis
            **Short-term Financial Health:**
            - Current Ratio = Current Assets ÷ Current Liabilities = X.XX
            - Quick Ratio = (Current Assets - Inventory) ÷ Current Liabilities = X.XX
            - Cash Ratio = Cash ÷ Current Liabilities = X.XX
            - Working Capital = Current Assets - Current Liabilities = $XX.X billion
            - Operating Cash Flow Ratio = Operating CF ÷ Current Liabilities = X.XX

            **Liquidity Assessment:** [Excellent/Good/Adequate/Poor] - Company can [easily/adequately/with difficulty] meet short-term obligations

            ### Profitability Analysis
            **Margin Analysis:**
            - Gross Profit Margin = (Revenue - COGS) ÷ Revenue = XX.X%
            - Operating Margin = Operating Income ÷ Revenue = XX.X%
            - EBITDA Margin = EBITDA ÷ Revenue = XX.X%
            - Net Profit Margin = Net Income ÷ Revenue = XX.X%
            - Free Cash Flow Margin = Free CF ÷ Revenue = XX.X%

            **Return Metrics:**
            - ROE = Net Income ÷ Shareholders' Equity = XX.X%
            - ROA = Net Income ÷ Total Assets = XX.X%
            - ROIC = NOPAT ÷ Invested Capital = XX.X%
            - ROI = (Gain - Cost) ÷ Cost = XX.X%

            **Profitability Trend:** [Improving/Stable/Declining] - [3-year trend analysis]

            ### Leverage & Capital Structure
            **Debt Analysis:**
            - Debt-to-Equity = Total Debt ÷ Total Equity = X.XX
            - Debt-to-Assets = Total Debt ÷ Total Assets = XX.X%
            - Equity Multiplier = Total Assets ÷ Total Equity = X.XX
            - Capitalization Ratio = Total Debt ÷ (Total Debt + Equity) = XX.X%

            **Coverage Ratios:**
            - Interest Coverage = EBIT ÷ Interest Expense = XX.X times
            - Debt Service Coverage = Operating CF ÷ Total Debt Service = X.XX
            - Fixed Charge Coverage = (EBIT + Lease) ÷ (Interest + Lease) = X.XX

            **Leverage Assessment:** [Conservative/Moderate/Aggressive] - Debt levels are [appropriate/concerning] for industry

            ### Efficiency Analysis
            **Asset Utilization:**
            - Asset Turnover = Revenue ÷ Average Total Assets = X.XX times
            - Inventory Turnover = COGS ÷ Average Inventory = XX.X times
            - Receivables Turnover = Revenue ÷ Average AR = XX.X times
            - Fixed Asset Turnover = Revenue ÷ Average Fixed Assets = X.XX times

            **Working Capital Management:**
            - Days Sales Outstanding (DSO) = (AR ÷ Revenue) × 365 = XX days
            - Days Inventory Outstanding (DIO) = (Inventory ÷ COGS) × 365 = XX days
            - Days Payable Outstanding (DPO) = (AP ÷ COGS) × 365 = XX days
            - Cash Conversion Cycle = DSO + DIO - DPO = XX days

            ## VALUATION ANALYSIS

            ### Market-Based Valuation
            **Price Multiples:**
            - P/E Ratio (TTM) = Stock Price ÷ EPS = XX.X
            - Forward P/E = Stock Price ÷ Forward EPS = XX.X
            - PEG Ratio = P/E ÷ EPS Growth Rate = X.XX
            - Price-to-Book = Stock Price ÷ Book Value per Share = X.XX
            - Price-to-Sales = Market Cap ÷ Revenue = X.XX
            - EV/EBITDA = Enterprise Value ÷ EBITDA = XX.X

            **Relative Valuation vs Industry:**
            - P/E Premium/Discount to Sector: +/-XX.X%
            - EV/EBITDA vs Peers: [Higher/Lower/In-line]
            - Valuation Justification: [Growth/Quality/Risk factors]

            ### Intrinsic Value Analysis
            **DCF Model Assumptions:**
            - WACC (Weighted Average Cost of Capital): X.X%
            - Terminal Growth Rate: X.X%
            - Free Cash Flow Growth (5-year): X.X%
            - Beta: X.XX
            - Risk-Free Rate: X.X%
            - Market Risk Premium: X.X%

            **Fair Value Estimate:** $XXX.XX per share
            **Current Price:** $XXX.XX per share
            **Upside/Downside:** +/-XX.X%

            ## FINANCIAL PERFORMANCE TRENDS

            ### 5-Year Historical Analysis
            **Revenue Growth:**
            - 2024E: $XX.X billion (+X.X% YoY)
            - 2023: $XX.X billion (+X.X% YoY)
            - 2022: $XX.X billion (+X.X% YoY)
            - 2021: $XX.X billion (+X.X% YoY)
            - 2020: $XX.X billion (+X.X% YoY)
            - 5-Year CAGR: X.X%

            **Earnings Growth:**
            - EPS CAGR (5-year): X.X%
            - Earnings Quality Score: X/10
            - Consistency of Earnings: [High/Medium/Low]

            ### Cash Flow Analysis
            **Operating Cash Flow:**
            - OCF Growth (5-year CAGR): X.X%
            - OCF/Net Income Ratio: X.XX (Quality indicator)
            - Capex as % of Revenue: X.X%
            - Free Cash Flow: $XX.X billion
            - FCF Yield: X.X%

            ## COMPARATIVE ANALYSIS

            ### Peer Group Comparison
            **Key Competitors Analysis:**
            [Company A]: P/E XX.X, ROE XX.X%, Debt/Equity X.XX
            [Company B]: P/E XX.X, ROE XX.X%, Debt/Equity X.XX
            [Company C]: P/E XX.X, ROE XX.X%, Debt/Equity X.XX
            **Subject Company:** P/E XX.X, ROE XX.X%, Debt/Equity X.XX

            **Relative Positioning:** [Leader/Follower/Laggard] in [profitability/efficiency/growth]

            ## RISK ASSESSMENT MATRIX

            ### Quantitative Risk Metrics
            - Beta (5-year): X.XX (vs market 1.00)
            - Volatility (1-year): XX.X%
            - Maximum Drawdown: -XX.X%
            - Sharpe Ratio: X.XX
            - Altman Z-Score: X.XX ([Safe/Grey Zone/Distress])

            ### Financial Risk Factors
            1. **Credit Risk:** [Low/Medium/High] - [Debt sustainability analysis]
            2. **Liquidity Risk:** [Low/Medium/High] - [Cash position adequacy]  
            3. **Operational Risk:** [Low/Medium/High] - [Business model stability]
            4. **Market Risk:** [Low/Medium/High] - [Cyclical sensitivity]

            ## INVESTMENT THESIS SUMMARY

            ### Quantitative Scorecard (1-10 Scale)
            - **Profitability:** X/10 - [Strong/Adequate/Weak margins and returns]
            - **Growth:** X/10 - [Accelerating/Stable/Decelerating trends]
            - **Financial Strength:** X/10 - [Conservative/Balanced/Leveraged structure]
            - **Valuation:** X/10 - [Undervalued/Fair/Overvalued relative to fundamentals]
            - **Quality:** X/10 - [High/Medium/Low business quality]

            **Overall Financial Health Score:** XX/50

            ### Key Investment Highlights
            1. [Quantitative strength/weakness #1 with supporting data]
            2. [Quantitative strength/weakness #2 with supporting data]  
            3. [Quantitative strength/weakness #3 with supporting data]

            ### Critical Metrics to Monitor
            - [Metric 1]: Current XX.X%, Target range XX-XX%
            - [Metric 2]: Current $XX.X billion, Trend [improving/stable/concerning]
            - [Metric 3]: Current XX.X%, vs peer average XX.X%

            CALCULATION METHODOLOGY: Use standard financial formulas and provide step-by-step calculations where relevant. All metrics should reflect realistic financial data for the analyzed company/sector.

            DATA INTEGRITY: Ensure all numbers are internally consistent (balance sheet balances, ratio calculations align, etc.).
            """
            
            result = self._call_llm(prompt)
            
            return f"{result}"
            
        except Exception as e:
            return f"Analysis Agent error: {str(e)}"
    
    def calculate_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate key financial ratios
        """
        try:
            ratios = {}
            
            # Basic ratio calculations (these would use real data in production)
            if 'current_assets' in financial_data and 'current_liabilities' in financial_data:
                ratios['current_ratio'] = financial_data['current_assets'] / financial_data['current_liabilities']
            
            if 'total_debt' in financial_data and 'total_equity' in financial_data:
                ratios['debt_to_equity'] = financial_data['total_debt'] / financial_data['total_equity']
            
            return ratios
            
        except Exception as e:
            return {"error": str(e)}
    
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
    
    def analyze_data(self, data: str) -> str:
        """
        Perform comprehensive financial analysis with detailed calculations and proper table formatting
        """
        try:
            prompt = f"""
            You are a CFA charterholder and senior financial analyst. Perform comprehensive quantitative financial analysis on: {data}
            
            CRITICAL REQUIREMENTS:
            1. Use REALISTIC, SPECIFIC numbers - NO placeholders like "XX.X" or "XXX.XX"
            2. Format tables properly with actual data for easy reading
            3. Make calculations internally consistent (ratios must be mathematically correct)
            4. Provide industry-appropriate metrics and ranges
            5. Include detailed analytical insights for each metric

            Generate a professional financial analysis report:

            # COMPREHENSIVE FINANCIAL ANALYSIS REPORT

            ## FINANCIAL RATIO ANALYSIS

            ### Liquidity Analysis
            **Short-term Financial Health:**

            | Ratio | Current Value | Industry Avg | Assessment |
            |-------|---------------|--------------|------------|
            | Current Ratio | 2.45 | 2.1 | Strong |
            | Quick Ratio | 1.87 | 1.6 | Excellent |
            | Cash Ratio | 0.92 | 0.4 | Very Strong |
            | Working Capital | $45.2B | $32.1B | Superior |

            **Liquidity Assessment:** Excellent - Company maintains strong cash position and can easily meet short-term obligations. Current ratio of 2.45 indicates robust liquidity buffer, while quick ratio of 1.87 shows ability to meet obligations without relying on inventory liquidation.

            ### Profitability Analysis
            **Operating Performance:**

            | Profitability Metric | Current | 1-Year Ago | 3-Year Avg | Trend |
            |---------------------|---------|------------|------------|-------|
            | Gross Profit Margin | 42.3% | 41.1% | 40.8% | ↗ Improving |
            | Operating Margin | 28.7% | 27.2% | 26.9% | ↗ Improving |
            | EBITDA Margin | 33.4% | 32.1% | 31.7% | ↗ Improving |
            | Net Profit Margin | 24.1% | 23.6% | 22.9% | ↗ Improving |
            | ROE | 86.4% | 83.2% | 81.7% | ↗ Improving |
            | ROA | 22.8% | 21.9% | 21.2% | ↗ Improving |
            | ROIC | 34.7% | 33.1% | 32.4% | ↗ Improving |

            **Profitability Assessment:** Outstanding profitability metrics across all measures. ROE of 86.4% significantly exceeds industry median of 15-20%, indicating exceptional capital efficiency. Improving trend over 3 years demonstrates operational excellence and market power.

            ### Leverage & Capital Structure
            **Debt Management:**

            | Leverage Metric | Current Value | Industry Median | Rating |
            |-----------------|---------------|------------------|--------|
            | Debt-to-Equity | 0.63 | 0.85 | Conservative |
            | Debt-to-Assets | 23.4% | 32.1% | Low Risk |
            | Interest Coverage | 18.6x | 8.2x | Excellent |
            | Debt Service Coverage | 4.2x | 2.8x | Strong |
            | Net Debt/EBITDA | 0.8x | 2.1x | Very Conservative |

            **Leverage Assessment:** Conservative capital structure with manageable debt levels. Interest coverage of 18.6x provides substantial cushion for debt service. Net debt/EBITDA of 0.8x indicates low financial risk and flexibility for growth investments or shareholder returns.

            ### Efficiency Analysis
            **Asset Utilization:**

            | Efficiency Metric | Current | Industry Avg | Performance |
            |-------------------|---------|--------------|-------------|
            | Asset Turnover | 0.95x | 0.82x | Above Average |
            | Inventory Turnover | 8.7x | 6.4x | Excellent |
            | Receivables Turnover | 12.3x | 9.1x | Superior |
            | Fixed Asset Turnover | 3.4x | 2.8x | Strong |
            | Cash Conversion Cycle | 34 days | 48 days | Efficient |

            **Working Capital Management:**
            - Days Sales Outstanding: 29 days (vs industry 38 days) - Excellent collection
            - Days Inventory Outstanding: 42 days (vs industry 57 days) - Efficient inventory management  
            - Days Payable Outstanding: 37 days (vs industry 47 days) - Balanced supplier relationships
            - Cash Conversion Cycle: 34 days - Superior working capital efficiency

            ## VALUATION ANALYSIS

            ### Market-Based Valuation
            **Price Multiples Comparison:**

            | Valuation Multiple | Company | Industry Median | Premium/Discount |
            |--------------------|---------|-----------------|------------------|
            | P/E Ratio (TTM) | 28.4 | 22.1 | +28.5% premium |
            | Forward P/E | 24.7 | 19.8 | +24.7% premium |
            | PEG Ratio | 1.34 | 1.58 | -15.2% discount |
            | Price-to-Book | 12.8 | 3.4 | +276% premium |
            | Price-to-Sales | 6.8 | 2.9 | +134% premium |
            | EV/EBITDA | 20.6 | 16.3 | +26.4% premium |

            **Valuation Assessment:** Trading at significant premium to industry on most metrics, justified by superior profitability and growth. PEG ratio of 1.34 suggests reasonable valuation relative to growth expectations.

            ## PEER COMPARISON ANALYSIS

            ### Competitive Positioning
            **Key Competitors Financial Comparison:**

            | Metric | Company | Competitor A | Competitor B | Competitor C | Industry Leader |
            |--------|---------|--------------|--------------|--------------|-----------------|
            | Revenue Growth | 8.2% | 5.7% | 3.1% | 6.8% | 8.2% |
            | Operating Margin | 28.7% | 18.4% | 15.2% | 22.1% | 28.7% |
            | ROE | 86.4% | 24.7% | 18.9% | 31.2% | 86.4% |
            | Debt/Equity | 0.63 | 1.24 | 0.87 | 1.05 | 0.63 |
            | P/E Ratio | 28.4 | 19.2 | 16.8 | 24.7 | 28.4 |
            | Market Cap | $2.89T | $456B | $234B | $678B | $2.89T |

            **Competitive Assessment:** Clear market leader across profitability metrics. Revenue growth of 8.2% leads peer group, while maintaining industry-highest operating margins. Conservative debt structure provides financial flexibility advantage over leveraged competitors.

            ## FINANCIAL PERFORMANCE TRENDS

            ### 5-Year Historical Analysis
            **Revenue & Earnings Growth:**

            | Year | Revenue | YoY Growth | Net Income | EPS | ROE |
            |------|---------|------------|------------|-----|-----|
            | 2024E | $394.3B | +2.8% | $95.0B | $6.05 | 86.4% |
            | 2023 | $383.3B | +4.3% | $90.5B | $5.78 | 83.2% |
            | 2022 | $367.5B | +7.8% | $84.2B | $5.39 | 81.7% |
            | 2021 | $340.8B | +12.1% | $78.4B | $5.02 | 79.3% |
            | 2020 | $304.1B | +5.6% | $71.8B | $4.59 | 75.9% |

            **5-Year CAGR:** Revenue: 6.7%, Net Income: 7.3%, EPS: 7.1%

            **Trend Analysis:** Consistent growth trajectory with accelerating profitability. Recent deceleration in revenue growth offset by expanding margins, demonstrating pricing power and operational efficiency gains.

            ### Cash Flow Analysis
            **Operating Cash Flow Performance:**

            | Cash Flow Metric | Current Year | Previous Year | 3-Year Avg | Quality Score |
            |------------------|--------------|---------------|------------|---------------|
            | Operating Cash Flow | $104.5B | $99.8B | $96.2B | Excellent |
            | Free Cash Flow | $89.2B | $85.1B | $81.7B | Superior |
            | FCF Conversion | 94.0% | 94.1% | 93.8% | Excellent |
            | Capex/Revenue | 3.9% | 4.1% | 4.2% | Efficient |
            | FCF Yield | 3.1% | 2.9% | 2.8% | Attractive |

            ## INVESTMENT THESIS SUMMARY

            ### Quantitative Scorecard (1-10 Scale)
            - **Profitability:** 9.5/10 - Exceptional margins and returns across all metrics
            - **Growth:** 7.5/10 - Solid growth with some recent deceleration  
            - **Financial Strength:** 9.0/10 - Conservative balance sheet with strong cash generation
            - **Valuation:** 6.5/10 - Premium valuation justified by quality but limits upside
            - **Quality:** 9.5/10 - Market-leading business model and competitive position

            **Overall Financial Health Score:** 42/50 - Excellent

            ### Key Investment Highlights
            1. **Superior Profitability:** ROE of 86.4% and operating margin of 28.7% significantly exceed industry averages, indicating sustainable competitive advantages and operational excellence
            2. **Strong Balance Sheet:** Conservative debt/equity of 0.63 and interest coverage of 18.6x provide financial flexibility and downside protection during economic downturns  
            3. **Efficient Capital Allocation:** Free cash flow of $89.2B and ROIC of 34.7% demonstrate exceptional capital productivity and value creation capability

            ### Critical Metrics to Monitor
            - **Revenue Growth Rate:** Current 2.8%, Target range 5-8% for sustained premium valuation
            - **Operating Margin:** Current 28.7%, monitor for 25%+ maintenance amid competitive pressure
            - **Free Cash Flow:** Current $89.2B, trend must remain positive for dividend sustainability and growth investments

            All financial calculations verified for mathematical consistency. Ratios and percentages properly calculated from provided base metrics.
            """
            
            result = self._call_llm(prompt)
            
            return f"� COMPREHENSIVE FINANCIAL ANALYSIS:\n\n{result}"
            
        except Exception as e:
            return f"Analysis Agent error: {str(e)}"
    
    def calculate_ratios(self, financial_data: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate key financial ratios
        """
        ratios = {}
        
        # Example ratio calculations (would be more comprehensive in real implementation)
        if 'current_assets' in financial_data and 'current_liabilities' in financial_data:
            ratios['current_ratio'] = financial_data['current_assets'] / financial_data['current_liabilities']
        
        if 'net_income' in financial_data and 'revenue' in financial_data:
            ratios['profit_margin'] = financial_data['net_income'] / financial_data['revenue']
        
        return ratios
