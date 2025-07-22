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
        Perform financial analysis (optimized for speed)
        """
        try:
            prompt = f"""
            Analyze the following financial information: {data}
            
            Provide a focused financial analysis (400-600 words) covering:

            ## Financial Ratio Analysis
            - Liquidity ratios (current ratio, quick ratio)
            - Profitability ratios (ROE, ROA, profit margins)
            - Leverage ratios (debt-to-equity, interest coverage)
            - Efficiency ratios (asset turnover, inventory turnover)

            ## Performance Assessment
            - Revenue and earnings trends
            - Margin analysis and sustainability
            - Cash flow strength
            - Balance sheet quality

            ## Valuation Analysis
            - Current valuation metrics (P/E, P/B, EV/EBITDA)
            - Historical valuation comparison
            - Peer valuation comparison
            - Fair value assessment

            ## Risk Analysis
            - Financial risk factors
            - Operational leverage
            - Credit risk assessment
            - Market sensitivity

            ## Key Findings
            - Strengths and opportunities
            - Weaknesses and threats
            - Overall financial health score (1-10)
            - Key metrics to monitor

            Include specific numbers, ratios, and percentages in your analysis.
            """
            
            result = self._call_llm(prompt)
            
            return f"📈 FINANCIAL ANALYSIS RESULTS:\n\n{result}"
            
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
        Perform comprehensive financial analysis and calculations
        """
        try:
            prompt = f"""
            As a CFA charterholder and senior financial analyst with 20+ years of experience at top investment firms, perform the most comprehensive and detailed financial analysis possible on the following financial information: {data}
            
            INSTRUCTIONS: Provide an extremely detailed, in-depth analysis covering ALL aspects below. Be verbose and thorough. This analysis should be comprehensive enough for institutional investors making large allocation decisions. Include specific calculations, detailed reasoning, and quantitative support for every statement.

            Please provide comprehensive analysis covering:
            
            1. EXHAUSTIVE FINANCIAL RATIO ANALYSIS
            - Complete Liquidity Ratios Analysis:
              * Current Ratio = Current Assets / Current Liabilities (calculate and interpret with 5-year trend)
              * Quick Ratio = (Current Assets - Inventory) / Current Liabilities (detailed analysis)
              * Cash Ratio = Cash & Equivalents / Current Liabilities (liquidity strength assessment)
              * Operating Cash Flow Ratio = Operating Cash Flow / Current Liabilities
              * Working Capital analysis with detailed components breakdown
              * Days Sales Outstanding (DSO), Days Inventory Outstanding (DIO), Days Payable Outstanding (DPO)
              * Cash conversion cycle analysis with efficiency implications
            
            - Comprehensive Profitability Ratios Analysis:
              * Return on Equity (ROE) with detailed DuPont analysis breakdown:
                - Net Profit Margin analysis
                - Asset Turnover analysis  
                - Equity Multiplier analysis
              * Return on Assets (ROA) with detailed component analysis
              * Return on Invested Capital (ROIC) vs WACC analysis
              * Gross Profit Margin analysis by segment/product line
              * Operating Profit Margin with operating leverage analysis
              * EBITDA Margin and sustainability assessment
              * Net Profit Margin with quality of earnings analysis
              * Asset turnover ratios (total, fixed, working capital)
            
            - Detailed Leverage Ratios Analysis:
              * Debt-to-Equity ratio with optimal capital structure assessment
              * Debt-to-Assets ratio and asset coverage analysis
              * Times Interest Earned (TIE) ratio and debt service capability
              * EBITDA to Interest Coverage ratio
              * Debt Service Coverage Ratio (DSCR)
              * Financial Leverage Multiplier and risk implications
              * Net Debt to EBITDA analysis with covenant compliance
              * Credit rating implications and default probability assessment
            
            - Complete Efficiency Ratios Analysis:
              * Total Asset Turnover and efficiency trends
              * Fixed Asset Turnover and capital productivity
              * Inventory Turnover with supply chain efficiency analysis
              * Receivables Turnover and collection effectiveness
              * Payables Turnover and supplier relationship management
              * Working Capital Turnover and operational efficiency
              * Revenue per Employee and productivity metrics
            
            - Comprehensive Valuation Ratios Analysis:
              * Price-to-Earnings (P/E) ratio analysis (trailing, forward, PEG)
              * Price-to-Book (P/B) ratio with book value quality assessment
              * Price-to-Sales (P/S) ratio with revenue quality analysis
              * Enterprise Value to EBITDA (EV/EBITDA) with peer comparison
              * Enterprise Value to Sales (EV/Sales) analysis
              * Enterprise Value to Free Cash Flow (EV/FCF)
              * Dividend Yield and payout ratio sustainability analysis
              * Price-to-Cash Flow ratios and cash generation quality
            
            2. DETAILED TREND ANALYSIS & HISTORICAL PERFORMANCE
            - Comprehensive Historical Performance Analysis (5-10 years):
              * Revenue growth analysis by segment, geography, and product line
              * Detailed margin expansion/contraction analysis with drivers
              * Cash flow growth trends and quality assessment
              * Balance sheet evolution and capital structure changes
              * Return metrics trends and consistency analysis
            
            - Complete Growth Rates Analysis:
              * Revenue CAGR analysis with segment breakdown
              * Earnings growth rates (EPS, operating income, net income)
              * Free cash flow growth analysis and sustainability
              * Book value and tangible book value growth
              * Dividend growth rate and policy consistency
            
            - Detailed Seasonality and Cyclical Patterns:
              * Quarterly seasonality analysis with statistical significance
              * Business cycle correlation and economic sensitivity
              * Industry cyclicality and positioning analysis
              * Volatility patterns and earnings predictability
            
            - Performance Consistency and Quality Analysis:
              * Earnings volatility and predictability metrics
              * Cash flow consistency and accrual quality
              * Revenue recognition quality and sustainability
              * One-time items impact and normalized performance
            
            3. COMPREHENSIVE FINANCIAL HEALTH ASSESSMENT
            - Complete Balance Sheet Strength Analysis:
              * Asset quality and composition analysis
              * Liability structure and maturity profile assessment
              * Off-balance sheet obligations and contingent liabilities
              * Working capital adequacy and optimization opportunities
              * Capital structure optimization and cost of capital analysis
            
            - Detailed Cash Flow Analysis:
              * Operating Cash Flow quality and sustainability
              * Free Cash Flow generation and conversion rates
              * Cash Flow from Investing activities and capex analysis
              * Cash Flow from Financing activities and capital allocation
              * Cash flow coverage ratios and financial flexibility
              * Cash burn analysis and runway calculations
            
            - Working Capital Management Efficiency:
              * Working capital components analysis and trends
              * Operating cycle and cash conversion efficiency
              * Seasonal working capital requirements
              * Working capital as % of sales analysis
              * Supplier and customer payment terms optimization
            
            - Capital Allocation Effectiveness:
              * Return on invested capital (ROIC) vs cost of capital (WACC)
              * Capital expenditure efficiency and ROI analysis
              * M&A track record and value creation assessment
              * Dividend policy and shareholder return analysis
              * Share buyback programs and timing effectiveness
            
            4. EXTENSIVE COMPETITIVE & PEER ANALYSIS
            - Comprehensive Performance vs Industry Benchmarks:
              * Profitability metrics comparison with detailed peer analysis
              * Efficiency ratios benchmarking and best practices
              * Growth rates comparison and market share analysis
              * Valuation multiples relative positioning
              * Credit quality comparison and financial strength ranking
            
            - Detailed Competitive Positioning Analysis:
              * Market share trends and competitive dynamics
              * Pricing power assessment and competitive moats
              * Cost structure analysis and competitive advantages
              * Product/service differentiation and value proposition
              * Operational efficiency vs competitors
            
            - Market Leadership and Innovation Analysis:
              * R&D spending and innovation metrics
              * Patent portfolio and intellectual property strength
              * Technology adoption and digital transformation progress
              * Market leadership indicators and brand strength
            
            5. COMPREHENSIVE RISK ANALYSIS & ASSESSMENT
            - Detailed Credit Risk Assessment:
              * Default probability modeling and credit scoring
              * Covenant compliance analysis and financial flexibility
              * Liquidity risk assessment and funding sources
              * Refinancing risk and debt maturity analysis
              * Industry credit cycle positioning
            
            - Complete Operational Risk Analysis:
              * Business model sustainability and scalability
              * Key man risk and management depth assessment
              * Operational leverage and fixed cost structure
              * Supply chain risks and supplier concentration
              * Customer concentration and retention analysis
            
            - Market and Systematic Risk Factors:
              * Beta analysis and systematic risk exposure
              * Interest rate sensitivity and duration analysis
              * Currency exposure and hedging effectiveness
              * Commodity price risk and pass-through ability
              * Regulatory risk and compliance requirements
            
            6. DETAILED QUALITY OF EARNINGS ANALYSIS
            - Revenue Recognition Quality Assessment:
              * Revenue recognition policies and conservatism
              * Channel stuffing and revenue timing analysis
              * Related party transactions and revenue quality
              * Organic vs inorganic growth analysis
              * Revenue visibility and backlog analysis
            
            - Earnings Quality and Sustainability Analysis:
              * Non-recurring items and normalized earnings
              * Accruals analysis and earnings management indicators
              * Cash earnings vs reported earnings analysis
              * Working capital changes impact on earnings
              * Pension and other post-employment benefit impacts
            
            - Accounting Quality Assessment:
              * Accounting policy aggressiveness and conservatism
              * Asset impairment history and adequacy of reserves
              * Goodwill and intangible assets valuation
              * Inventory accounting and valuation methods
              * Depreciation and amortization policies
            
            7. ADVANCED FINANCIAL MODELING & PROJECTIONS
            - Detailed 5-Year Financial Projections:
              * Revenue forecasting by segment with drivers analysis
              * Margin projections with operating leverage implications
              * Working capital forecasting and cash flow projections
              * Capital expenditure requirements and timing
              * Debt service and refinancing requirements
            
            - Sensitivity Analysis and Scenario Modeling:
              * Key variable sensitivity analysis (growth, margins, multiples)
              * Monte Carlo simulation for key metrics
              * Stress testing under various economic scenarios
              * Break-even analysis and downside protection
            
            - Valuation Model Inputs and Assumptions:
              * Cost of equity calculation (CAPM with adjustments)
              * Cost of debt analysis and credit spread assessment
              * WACC calculation with detailed component analysis
              * Terminal value assumptions and growth rate justification
              * Tax rate normalization and policy impact analysis
            
            8. ESG FACTORS AND SUSTAINABILITY ANALYSIS
            - Environmental Impact Assessment:
              * Carbon footprint and climate risk analysis
              * Environmental compliance and regulatory exposure
              * Sustainability initiatives and green revenue streams
              * Resource efficiency and waste management
            
            - Social Responsibility and Governance:
              * Employee satisfaction and retention metrics
              * Diversity and inclusion metrics and progress
              * Customer satisfaction and brand reputation
              * Corporate governance quality and board effectiveness
            
            Provide extensive quantitative support for every statement with specific calculations, percentages, ratios, and detailed analytical reasoning. Include year-over-year changes, trend analysis, and peer comparisons wherever possible.

            This should be an extremely comprehensive institutional-quality financial analysis report of at least 3000-4000 words with detailed calculations and professional insights suitable for major investment decisions.
            
            Format as a professional financial analysis with clear sections, subsections, and bullet points for easy navigation and reference.
            """
            
            result = self._call_llm(prompt)
            
            return f"📈 COMPREHENSIVE FINANCIAL ANALYSIS & DETAILED CALCULATIONS:\n\n{result}"
            
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
