from langchain.llms.base import BaseLLM
from langchain.schema import HumanMessage
from typing import Any, Dict, List
import json
import sys
import os
import numpy as np
from datetime import datetime

# Add the services directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.enhanced_financial_data_service import EnhancedFinancialDataService

class EnhancedAnalysisAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.name = "Enhanced Analysis Agent"
        self.data_service = EnhancedFinancialDataService()
    
    def _call_llm(self, prompt: str) -> str:
        """Helper method to call the LLM with proper format"""
        try:
            if hasattr(self.llm, 'predict_messages') or 'Chat' in str(type(self.llm)):
                response = self.llm.invoke([HumanMessage(content=prompt)])
                return response.content if hasattr(response, 'content') else str(response)
            else:
                return self.llm.invoke(prompt)
        except Exception as e:
            return f"LLM call failed: {str(e)}"
    
    def analyze_financial_data(self, research_data: str) -> str:
        """
        Perform detailed financial analysis using real market data
        """
        try:
            # Extract symbol from research data
            symbol = self._extract_symbol_from_research(research_data)
            
            if not symbol:
                return self._analyze_research_text_only(research_data)
            
            # Get fresh real data for analysis
            print(f"🔄 Performing real-time analysis for {symbol}...")
            real_data = self.data_service.get_comprehensive_stock_data(symbol)
            
            if "error" in real_data:
                return self._analyze_research_text_only(research_data)
            
            # Perform comprehensive analysis with real data
            analysis = self._perform_comprehensive_analysis(symbol, real_data, research_data)
            
            return f"📊 **ENHANCED FINANCIAL ANALYSIS** ({symbol})\n📈 Real-time Data Analysis Complete\n\n{analysis}"
            
        except Exception as e:
            return f"Enhanced Analysis Agent error: {str(e)}"
    
    def _extract_symbol_from_research(self, research_data: str) -> str:
        """Extract stock symbol from research data"""
        import re
        
        # Look for patterns that indicate stock symbols
        patterns = [
            r'\(([A-Z]{1,5})\)',  # Symbol in parentheses
            r'Ticker: ([A-Z]{1,5})',  # After "Ticker:"
            r'Symbol: ([A-Z]{1,5})',  # After "Symbol:"
            r'REPORT.*?([A-Z]{2,5})\)',  # In report headers
        ]
        
        for pattern in patterns:
            match = re.search(pattern, research_data)
            if match:
                return match.group(1)
        
        return None
    
    def _analyze_research_text_only(self, research_data: str) -> str:
        """Analyze research data when no symbol is available"""
        
        prompt = f"""
        You are a senior financial analyst reviewing a research report. Analyze the provided research data and provide additional insights, validations, and risk assessments.
        
        RESEARCH DATA TO ANALYZE:
        {research_data}
        
        Provide a comprehensive financial analysis covering:
        
        # 📊 FINANCIAL ANALYSIS REVIEW
        
        ## 🔍 DATA VALIDATION & QUALITY ASSESSMENT
        - Assess the completeness and reliability of the financial data presented
        - Identify any missing critical metrics or data points
        - Comment on the recency and relevance of the information
        
        ## 📈 PERFORMANCE ANALYSIS DEEP DIVE
        - Analyze the financial performance trends mentioned
        - Compare performance metrics against industry benchmarks (if available)
        - Identify strengths and weaknesses in the financial profile
        
        ## 💰 VALUATION ASSESSMENT
        - Review the valuation metrics and their appropriateness
        - Assess if the company appears fairly valued, overvalued, or undervalued
        - Identify key valuation drivers and risks
        
        ## ⚠️ RISK ANALYSIS
        - Identify financial, operational, and market risks
        - Assess the company's financial stability and liquidity
        - Evaluate competitive position and industry challenges
        
        ## 🎯 INVESTMENT IMPLICATIONS
        - Provide investment thesis validation or challenges
        - Suggest areas requiring additional research
        - Recommend investment approach based on risk profile
        
        ## 📋 ANALYTICAL RECOMMENDATIONS
        - Suggest additional metrics or data points that would strengthen the analysis
        - Recommend monitoring key performance indicators
        - Provide guidance on investment timing and strategy
        
        Focus on providing actionable insights and professional-grade financial analysis.
        """
        
        return self._call_llm(prompt)
    
    def _perform_comprehensive_analysis(self, symbol: str, real_data: Dict, research_data: str) -> str:
        """Perform comprehensive analysis using real financial data"""
        
        # Extract key metrics for calculations
        price_data = real_data.get('price_data', {})
        financial_statements = real_data.get('financial_statements', {})
        valuation_metrics = real_data.get('valuation_metrics', {})
        risk_metrics = real_data.get('risk_metrics', {})
        market_data = real_data.get('market_data', {})
        
        # Perform advanced calculations
        advanced_metrics = self._calculate_advanced_metrics(real_data)
        investment_score = self._calculate_investment_score(real_data)
        risk_assessment = self._perform_risk_assessment(real_data)
        
        prompt = f"""
        You are a quantitative financial analyst with expertise in advanced financial modeling. You have access to REAL, LIVE financial data for {symbol} and need to provide a comprehensive analytical assessment.
        
        **ORIGINAL RESEARCH DATA:**
        {research_data[:1500]}...
        
        **REAL-TIME FINANCIAL DATA FOR ANALYSIS:**
        {json.dumps(real_data, indent=2)[:3000]}...
        
        **ADVANCED CALCULATED METRICS:**
        {json.dumps(advanced_metrics, indent=2)}
        
        **QUANTITATIVE INVESTMENT SCORE:** {investment_score}/100
        
        **RISK ASSESSMENT SUMMARY:**
        {json.dumps(risk_assessment, indent=2)}
        
        Provide a comprehensive financial analysis using this real data:

        # 📊 ENHANCED FINANCIAL ANALYSIS: {symbol}
        
        ## 🔢 QUANTITATIVE ANALYSIS
        
        ### Advanced Financial Metrics (Calculated from Real Data)
        **Profitability Analysis:**
        {self._format_profitability_analysis(real_data, advanced_metrics)}
        
        **Efficiency Metrics:**
        {self._format_efficiency_analysis(real_data, advanced_metrics)}
        
        **Liquidity & Solvency:**
        {self._format_liquidity_analysis(real_data, advanced_metrics)}
        
        ## 📈 PERFORMANCE BENCHMARKING
        
        ### Market Performance vs Benchmarks
        **Relative Performance:**
        - Stock 1-Year Return: {price_data.get('returns', {}).get('1_year', 'N/A'):.1f}%
        - S&P 500 1-Year: {market_data.get('sp500_1y_return', 'N/A'):.1f}%
        - Outperformance: {(price_data.get('returns', {}).get('1_year', 0) - market_data.get('sp500_1y_return', 0)):.1f}%
        - Risk-Adjusted Return (Sharpe): {risk_metrics.get('sharpe_ratio', 0):.2f}
        
        ### Valuation Comparison
        **Current Valuation Metrics:**
        - P/E Ratio: {valuation_metrics.get('pe_ratio', 0):.1f} (Industry avg: estimate based on sector)
        - P/B Ratio: {valuation_metrics.get('price_to_book', 0):.2f}
        - EV/EBITDA: {valuation_metrics.get('ev_to_ebitda', 0):.1f}
        - PEG Ratio: {valuation_metrics.get('peg_ratio', 0):.2f} ({'Undervalued' if valuation_metrics.get('peg_ratio', 2) < 1 else 'Fairly Valued' if valuation_metrics.get('peg_ratio', 2) < 1.5 else 'Overvalued'})
        
        ## ⚠️ COMPREHENSIVE RISK ANALYSIS
        
        ### Systematic Risk Assessment
        - **Market Risk (Beta):** {risk_metrics.get('beta', 0):.2f} ({'Low' if risk_metrics.get('beta', 1) < 0.8 else 'Moderate' if risk_metrics.get('beta', 1) < 1.2 else 'High'} correlation with market)
        - **Volatility Risk:** {risk_metrics.get('volatility', 0):.1f}% annual volatility
        - **Downside Risk (Max Drawdown):** {risk_metrics.get('max_drawdown', 0):.1f}%
        - **Value at Risk (95%):** {risk_metrics.get('var_95', 0):.2f}% daily VaR
        
        ### Financial Risk Assessment
        {self._format_financial_risk_analysis(risk_assessment)}
        
        ## 🎯 INVESTMENT RECOMMENDATION FRAMEWORK
        
        ### Quantitative Investment Score: {investment_score}/100
        {self._format_investment_score_breakdown(investment_score, advanced_metrics)}
        
        ### Strategic Investment Analysis
        **Investment Strengths (Data-Driven):**
        {self._identify_investment_strengths(real_data, advanced_metrics)}
        
        **Investment Risks (Quantified):**
        {self._identify_investment_risks(real_data, risk_assessment)}
        
        ### Portfolio Allocation Guidance
        **Recommended Portfolio Weight:** {self._calculate_portfolio_weight(investment_score, risk_metrics)}%
        **Investment Horizon:** {self._recommend_investment_horizon(real_data, risk_metrics)}
        **Risk Management:** {self._recommend_risk_management(risk_assessment)}
        
        ## 📊 SCENARIO ANALYSIS
        
        ### Bull Case Scenario
        {self._generate_bull_case(real_data, advanced_metrics)}
        
        ### Bear Case Scenario  
        {self._generate_bear_case(real_data, risk_assessment)}
        
        ### Base Case Expectation
        {self._generate_base_case(real_data)}
        
        ## 🔍 MONITORING & ACTION ITEMS
        
        ### Key Metrics to Track
        1. **Financial Health:** Monitor quarterly earnings, cash flow, and debt levels
        2. **Market Position:** Track relative performance vs sector and market
        3. **Valuation Changes:** Watch for P/E expansion/contraction
        4. **Risk Indicators:** Monitor volatility and correlation changes
        
        ### Trigger Points for Review
        - **Buy More:** If price drops >15% without fundamental deterioration
        - **Trim Position:** If valuation exceeds 1.5x fair value estimate
        - **Exit Signal:** If investment score drops below 40/100
        
        ---
        **Analysis Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        **Data Confidence:** High (Real-time financial data)
        **Next Review:** Quarterly earnings or significant market events
        """
        
        return self._call_llm(prompt)
    
    def _calculate_advanced_metrics(self, data: Dict) -> Dict:
        """Calculate advanced financial metrics from real data"""
        try:
            metrics = {}
            
            # Get data sections
            financial_statements = data.get('financial_statements', {})
            valuation_metrics = data.get('valuation_metrics', {})
            price_data = data.get('price_data', {})
            
            # Income statement metrics
            income_statement = financial_statements.get('income_statement', {})
            balance_sheet = financial_statements.get('balance_sheet', {})
            
            revenue = income_statement.get('total_revenue', 0)
            net_income = income_statement.get('net_income', 0)
            total_assets = balance_sheet.get('total_assets', 0)
            total_equity = balance_sheet.get('total_equity', 0)
            market_cap = valuation_metrics.get('market_cap', 0)
            
            # Calculate advanced ratios
            if revenue > 0:
                metrics['asset_turnover'] = total_assets / revenue if total_assets > 0 else 0
                metrics['revenue_per_employee'] = revenue / data.get('basic_info', {}).get('employees', 1) if data.get('basic_info', {}).get('employees', 0) > 0 else 0
            
            if total_equity > 0:
                metrics['roe'] = (net_income / total_equity) * 100 if net_income > 0 else 0
                metrics['book_value_per_share'] = total_equity / (market_cap / price_data.get('current_price', 1)) if market_cap > 0 and price_data.get('current_price', 0) > 0 else 0
            
            if total_assets > 0:
                metrics['roa'] = (net_income / total_assets) * 100 if net_income > 0 else 0
            
            # Price momentum indicators
            returns = price_data.get('returns', {})
            if returns:
                metrics['momentum_score'] = (
                    returns.get('1_month', 0) * 0.2 +
                    returns.get('3_month', 0) * 0.3 +
                    returns.get('6_month', 0) * 0.3 +
                    returns.get('1_year', 0) * 0.2
                )
            
            return metrics
            
        except Exception as e:
            return {"error": f"Error calculating advanced metrics: {str(e)}"}
    
    def _calculate_investment_score(self, data: Dict) -> int:
        """Calculate overall investment score (0-100)"""
        try:
            score = 50  # Base score
            
            valuation_metrics = data.get('valuation_metrics', {})
            risk_metrics = data.get('risk_metrics', {})
            price_data = data.get('price_data', {})
            financial_statements = data.get('financial_statements', {})
            
            # Valuation scoring (25 points)
            pe_ratio = valuation_metrics.get('pe_ratio', 0)
            if 0 < pe_ratio < 15:
                score += 15  # Undervalued
            elif 15 <= pe_ratio <= 25:
                score += 10  # Fairly valued
            elif pe_ratio > 25:
                score += 5   # Overvalued
            
            peg_ratio = valuation_metrics.get('peg_ratio', 0)
            if 0 < peg_ratio < 1:
                score += 10
            elif 1 <= peg_ratio <= 1.5:
                score += 5
            
            # Financial health scoring (25 points)
            current_ratio = risk_metrics.get('current_ratio', 0)
            if current_ratio > 1.5:
                score += 10
            elif current_ratio > 1:
                score += 5
            
            debt_to_equity = risk_metrics.get('debt_to_equity', 0)
            if debt_to_equity < 0.3:
                score += 10
            elif debt_to_equity < 0.6:
                score += 5
            
            # Profitability scoring (25 points)
            margins = financial_statements.get('margins', {})
            net_margin = margins.get('net_margin', 0)
            if net_margin > 20:
                score += 15
            elif net_margin > 10:
                score += 10
            elif net_margin > 5:
                score += 5
            
            operating_margin = margins.get('operating_margin', 0)
            if operating_margin > 25:
                score += 10
            elif operating_margin > 15:
                score += 5
            
            # Performance scoring (25 points)
            returns = price_data.get('returns', {})
            one_year_return = returns.get('1_year', 0)
            if one_year_return > 20:
                score += 15
            elif one_year_return > 10:
                score += 10
            elif one_year_return > 0:
                score += 5
            
            volatility = risk_metrics.get('volatility', 0)
            if volatility < 20:
                score += 10
            elif volatility < 30:
                score += 5
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50  # Default score on error
    
    def _perform_risk_assessment(self, data: Dict) -> Dict:
        """Perform comprehensive risk assessment"""
        try:
            risk_assessment = {
                "overall_risk": "Moderate",
                "risk_factors": [],
                "risk_score": 50  # 0-100, higher = riskier
            }
            
            risk_metrics = data.get('risk_metrics', {})
            financial_statements = data.get('financial_statements', {})
            
            risk_score = 50  # Base risk score
            
            # Volatility risk
            volatility = risk_metrics.get('volatility', 0)
            if volatility > 40:
                risk_assessment["risk_factors"].append("High volatility (>40%)")
                risk_score += 15
            elif volatility > 25:
                risk_assessment["risk_factors"].append("Moderate volatility")
                risk_score += 8
            
            # Beta risk
            beta = risk_metrics.get('beta', 1)
            if beta > 1.5:
                risk_assessment["risk_factors"].append("High market correlation")
                risk_score += 10
            elif beta < 0.5:
                risk_assessment["risk_factors"].append("Low market correlation")
                risk_score -= 5
            
            # Debt risk
            debt_to_equity = risk_metrics.get('debt_to_equity', 0)
            if debt_to_equity > 1.0:
                risk_assessment["risk_factors"].append("High debt levels")
                risk_score += 15
            elif debt_to_equity > 0.6:
                risk_assessment["risk_factors"].append("Moderate debt levels")
                risk_score += 8
            
            # Liquidity risk
            current_ratio = risk_metrics.get('current_ratio', 0)
            if current_ratio < 1:
                risk_assessment["risk_factors"].append("Liquidity concerns")
                risk_score += 20
            elif current_ratio < 1.2:
                risk_assessment["risk_factors"].append("Tight liquidity")
                risk_score += 10
            
            # Profitability risk
            margins = financial_statements.get('margins', {})
            net_margin = margins.get('net_margin', 0)
            if net_margin < 0:
                risk_assessment["risk_factors"].append("Negative profitability")
                risk_score += 25
            elif net_margin < 5:
                risk_assessment["risk_factors"].append("Low profitability")
                risk_score += 15
            
            risk_assessment["risk_score"] = max(0, min(100, risk_score))
            
            # Overall risk categorization
            if risk_score < 40:
                risk_assessment["overall_risk"] = "Low"
            elif risk_score < 60:
                risk_assessment["overall_risk"] = "Moderate"
            elif risk_score < 80:
                risk_assessment["overall_risk"] = "High"
            else:
                risk_assessment["overall_risk"] = "Very High"
            
            return risk_assessment
            
        except Exception as e:
            return {"overall_risk": "Unknown", "risk_factors": ["Risk calculation error"], "risk_score": 50}
    
    def _format_profitability_analysis(self, data: Dict, advanced_metrics: Dict) -> str:
        """Format profitability analysis"""
        margins = data.get('financial_statements', {}).get('margins', {})
        income_statement = data.get('financial_statements', {}).get('income_statement', {})
        
        return f"""- Gross Margin: {margins.get('gross_margin', 0):.1f}%
- Operating Margin: {margins.get('operating_margin', 0):.1f}%
- Net Margin: {margins.get('net_margin', 0):.1f}%
- ROE: {advanced_metrics.get('roe', 0):.1f}%
- ROA: {advanced_metrics.get('roa', 0):.1f}%
- Revenue: ${income_statement.get('total_revenue', 0):,.0f}"""
    
    def _format_efficiency_analysis(self, data: Dict, advanced_metrics: Dict) -> str:
        """Format efficiency analysis"""
        return f"""- Asset Turnover: {advanced_metrics.get('asset_turnover', 0):.2f}x
- Revenue per Employee: ${advanced_metrics.get('revenue_per_employee', 0):,.0f}
- Book Value per Share: ${advanced_metrics.get('book_value_per_share', 0):.2f}"""
    
    def _format_liquidity_analysis(self, data: Dict, advanced_metrics: Dict) -> str:
        """Format liquidity analysis"""
        risk_metrics = data.get('risk_metrics', {})
        balance_sheet = data.get('financial_statements', {}).get('balance_sheet', {})
        
        return f"""- Current Ratio: {risk_metrics.get('current_ratio', 0):.2f}
- Debt-to-Equity: {risk_metrics.get('debt_to_equity', 0):.2f}
- Cash & Equivalents: ${balance_sheet.get('cash_and_equivalents', 0):,.0f}
- Working Capital: ${balance_sheet.get('working_capital', 0):,.0f}"""
    
    def _format_financial_risk_analysis(self, risk_assessment: Dict) -> str:
        """Format financial risk analysis"""
        risk_factors = risk_assessment.get('risk_factors', [])
        risk_score = risk_assessment.get('risk_score', 50)
        overall_risk = risk_assessment.get('overall_risk', 'Moderate')
        
        return f"""**Overall Risk Level:** {overall_risk} (Score: {risk_score}/100)
**Key Risk Factors:**
{chr(10).join([f"- {factor}" for factor in risk_factors]) if risk_factors else "- No significant risk factors identified"}"""
    
    def _format_investment_score_breakdown(self, score: int, advanced_metrics: Dict) -> str:
        """Format investment score breakdown"""
        if score >= 80:
            rating = "Strong Buy"
            description = "Excellent investment opportunity with strong fundamentals"
        elif score >= 70:
            rating = "Buy"
            description = "Good investment opportunity with solid fundamentals"
        elif score >= 60:
            rating = "Hold/Moderate Buy"
            description = "Decent investment with some attractive qualities"
        elif score >= 40:
            rating = "Hold"
            description = "Mixed signals, suitable for conservative investors"
        else:
            rating = "Sell/Avoid"
            description = "Significant concerns, high risk investment"
        
        return f"""**Investment Rating:** {rating}
**Score Interpretation:** {description}
**Key Scoring Factors:** Valuation metrics, financial health, profitability, and performance trends"""
    
    def _identify_investment_strengths(self, data: Dict, advanced_metrics: Dict) -> str:
        """Identify key investment strengths based on real data"""
        strengths = []
        
        # Check profitability
        margins = data.get('financial_statements', {}).get('margins', {})
        if margins.get('net_margin', 0) > 15:
            strengths.append(f"High profitability (Net margin: {margins.get('net_margin', 0):.1f}%)")
        
        # Check financial health
        risk_metrics = data.get('risk_metrics', {})
        if risk_metrics.get('current_ratio', 0) > 1.5:
            strengths.append(f"Strong liquidity (Current ratio: {risk_metrics.get('current_ratio', 0):.2f})")
        
        # Check valuation
        valuation_metrics = data.get('valuation_metrics', {})
        if 0 < valuation_metrics.get('pe_ratio', 100) < 15:
            strengths.append(f"Attractive valuation (P/E: {valuation_metrics.get('pe_ratio', 0):.1f})")
        
        # Check performance
        returns = data.get('price_data', {}).get('returns', {})
        if returns.get('1_year', 0) > 10:
            strengths.append(f"Strong 1-year performance ({returns.get('1_year', 0):+.1f}%)")
        
        return "\n".join([f"1. {strength}" for strength in strengths[:3]]) if strengths else "1. Requires deeper analysis to identify strengths"
    
    def _identify_investment_risks(self, data: Dict, risk_assessment: Dict) -> str:
        """Identify key investment risks based on real data"""
        risks = risk_assessment.get('risk_factors', [])
        
        # Add specific quantified risks
        additional_risks = []
        
        volatility = data.get('risk_metrics', {}).get('volatility', 0)
        if volatility > 30:
            additional_risks.append(f"High price volatility ({volatility:.1f}% annually)")
        
        max_drawdown = data.get('risk_metrics', {}).get('max_drawdown', 0)
        if max_drawdown < -20:
            additional_risks.append(f"Significant drawdown risk (Max: {max_drawdown:.1f}%)")
        
        all_risks = risks + additional_risks
        return "\n".join([f"{i+1}. {risk}" for i, risk in enumerate(all_risks[:3])]) if all_risks else "1. Standard market risks apply"
    
    def _calculate_portfolio_weight(self, investment_score: int, risk_metrics: Dict) -> float:
        """Calculate recommended portfolio weight"""
        base_weight = investment_score / 100 * 10  # Base 0-10%
        
        # Adjust for volatility
        volatility = risk_metrics.get('volatility', 25)
        if volatility > 40:
            base_weight *= 0.5
        elif volatility < 20:
            base_weight *= 1.5
        
        return min(15, max(1, base_weight))  # Cap between 1-15%
    
    def _recommend_investment_horizon(self, data: Dict, risk_metrics: Dict) -> str:
        """Recommend investment time horizon"""
        volatility = risk_metrics.get('volatility', 25)
        
        if volatility > 40:
            return "Long-term (3+ years) - High volatility requires patience"
        elif volatility < 20:
            return "Medium to Long-term (1-3 years) - Stable for various horizons"
        else:
            return "Medium-term (1-2 years) - Moderate volatility profile"
    
    def _recommend_risk_management(self, risk_assessment: Dict) -> str:
        """Recommend risk management strategies"""
        risk_score = risk_assessment.get('risk_score', 50)
        
        if risk_score > 70:
            return "Use stop-losses at -15%, position sizing <5% of portfolio"
        elif risk_score > 50:
            return "Monitor closely, consider stop-loss at -20%"
        else:
            return "Standard risk management, regular portfolio rebalancing"
    
    def _generate_bull_case(self, data: Dict, advanced_metrics: Dict) -> str:
        """Generate bull case scenario"""
        strengths = []
        margins = data.get('financial_statements', {}).get('margins', {})
        
        if margins.get('net_margin', 0) > 10:
            strengths.append("margin expansion continues")
        
        returns = data.get('price_data', {}).get('returns', {})
        if returns.get('1_year', 0) > 0:
            strengths.append("positive momentum sustains")
        
        return f"Strong execution on {', '.join(strengths[:2]) if strengths else 'business fundamentals'} could drive 25-40% upside over 12 months"
    
    def _generate_bear_case(self, data: Dict, risk_assessment: Dict) -> str:
        """Generate bear case scenario"""
        risks = risk_assessment.get('risk_factors', [])
        max_drawdown = data.get('risk_metrics', {}).get('max_drawdown', -10)
        
        if risks:
            return f"If {risks[0].lower()} materializes, could see {max_drawdown:.0f}% to -30% downside"
        else:
            return "Market downturn could drive -20% to -30% correction from current levels"
    
    def _generate_base_case(self, data: Dict) -> str:
        """Generate base case scenario"""
        returns = data.get('price_data', {}).get('returns', {})
        one_year = returns.get('1_year', 0)
        
        expected_return = max(-10, min(20, one_year * 0.6))  # Moderate future expectation
        
        return f"Expect {expected_return:+.0f}% to {expected_return + 10:+.0f}% total return over next 12 months based on current fundamentals"
    
    def compare_stocks(self, symbols: List[str]) -> str:
        """Compare multiple stocks using real data"""
        try:
            if len(symbols) < 2:
                return "Please provide at least 2 stock symbols for comparison"
            
            print(f"🔄 Comparing {len(symbols)} stocks using real data...")
            
            comparison_data = {}
            for symbol in symbols:
                data = self.data_service.get_comprehensive_stock_data(symbol.upper())
                if "error" not in data:
                    comparison_data[symbol.upper()] = data
            
            if len(comparison_data) < 2:
                return "Unable to fetch sufficient data for comparison"
            
            # Generate comparison analysis
            analysis = self._generate_stock_comparison(comparison_data)
            
            return f"📊 **MULTI-STOCK COMPARISON ANALYSIS**\n\n{analysis}"
            
        except Exception as e:
            return f"Error in stock comparison: {str(e)}"
    
    def _generate_stock_comparison(self, comparison_data: Dict) -> str:
        """Generate comprehensive stock comparison"""
        
        # Build comparison metrics
        comparison_metrics = {}
        for symbol, data in comparison_data.items():
            valuation = data.get('valuation_metrics', {})
            price_data = data.get('price_data', {})
            risk_metrics = data.get('risk_metrics', {})
            
            comparison_metrics[symbol] = {
                'current_price': price_data.get('current_price', 0),
                'market_cap': valuation.get('market_cap', 0),
                'pe_ratio': valuation.get('pe_ratio', 0),
                'price_to_book': valuation.get('price_to_book', 0),
                '1_year_return': price_data.get('returns', {}).get('1_year', 0),
                'volatility': risk_metrics.get('volatility', 0),
                'beta': risk_metrics.get('beta', 0),
                'dividend_yield': valuation.get('dividend_yield', 0)
            }
        
        prompt = f"""
        You are performing a comparative analysis of multiple stocks using real financial data. Provide a comprehensive comparison focusing on investment merits of each stock.
        
        **REAL COMPARISON DATA:**
        {json.dumps(comparison_metrics, indent=2)}
        
        **DETAILED DATA FOR EACH STOCK:**
        {json.dumps({k: v for k, v in comparison_data.items()}, indent=2)[:2000]}...
        
        Generate a professional comparative analysis:

        # 📊 MULTI-STOCK COMPARATIVE ANALYSIS
        
        ## 📈 PERFORMANCE COMPARISON
        
        ### Price Performance (1-Year Returns)
        {self._format_performance_comparison(comparison_metrics)}
        
        ### Risk-Adjusted Performance
        {self._format_risk_adjusted_comparison(comparison_metrics)}
        
        ## 💰 VALUATION COMPARISON
        
        ### Key Valuation Metrics
        {self._format_valuation_comparison(comparison_metrics)}
        
        ### Value vs Growth Assessment
        {self._assess_value_vs_growth(comparison_metrics)}
        
        ## ⚠️ RISK PROFILE COMPARISON
        
        ### Risk Metrics Comparison
        {self._format_risk_comparison(comparison_metrics)}
        
        ## 🎯 INVESTMENT RECOMMENDATION RANKING
        
        Rank these stocks from best to worst investment opportunity based on the real data analysis:
        
        1. **[Best Stock]** - [Detailed reasoning based on real metrics]
        2. **[Second Stock]** - [Detailed reasoning based on real metrics]  
        3. **[Third Stock]** - [Detailed reasoning based on real metrics]
        
        ## 📋 PORTFOLIO ALLOCATION SUGGESTIONS
        
        **Diversified Portfolio Approach:**
        - Conservative Investor: [Allocation percentages and reasoning]
        - Moderate Investor: [Allocation percentages and reasoning]
        - Aggressive Investor: [Allocation percentages and reasoning]
        
        **Key Insights:**
        - Best value play: [Stock and reasoning]
        - Best growth prospect: [Stock and reasoning]
        - Best dividend yield: [Stock and reasoning]
        - Lowest risk option: [Stock and reasoning]
        
        ## 🔍 MONITORING RECOMMENDATIONS
        
        **Key Events to Watch:**
        - [Specific upcoming catalysts for each stock]
        - [Earnings dates and key metrics to monitor]
        - [Technical levels and price targets]
        
        Use only the real financial data provided to support all conclusions and recommendations.
        """
        
        return self._call_llm(prompt)
    
    def _format_performance_comparison(self, metrics: Dict) -> str:
        """Format performance comparison"""
        performance_data = []
        for symbol, data in metrics.items():
            performance_data.append(f"- {symbol}: {data['1_year_return']:+.1f}%")
        return "\n".join(performance_data)
    
    def _format_risk_adjusted_comparison(self, metrics: Dict) -> str:
        """Format risk-adjusted comparison"""
        risk_adj_data = []
        for symbol, data in metrics.items():
            volatility = data['volatility']
            return_val = data['1_year_return']
            risk_adj_return = return_val / volatility if volatility > 0 else 0
            risk_adj_data.append(f"- {symbol}: {risk_adj_return:.2f} (Return/Volatility)")
        return "\n".join(risk_adj_data)
    
    def _format_valuation_comparison(self, metrics: Dict) -> str:
        """Format valuation comparison"""
        val_data = []
        for symbol, data in metrics.items():
            val_data.append(f"- {symbol}: P/E {data['pe_ratio']:.1f}, P/B {data['price_to_book']:.2f}, Div {data['dividend_yield']:.1f}%")
        return "\n".join(val_data)
    
    def _assess_value_vs_growth(self, metrics: Dict) -> str:
        """Assess value vs growth characteristics"""
        assessments = []
        for symbol, data in metrics.items():
            pe_ratio = data['pe_ratio']
            pb_ratio = data['price_to_book']
            
            if pe_ratio > 0 and pe_ratio < 15 and pb_ratio < 2:
                style = "Value"
            elif pe_ratio > 25 or data['1_year_return'] > 20:
                style = "Growth"
            else:
                style = "Blend"
            
            assessments.append(f"- {symbol}: {style} characteristics")
        return "\n".join(assessments)
    
    def _format_risk_comparison(self, metrics: Dict) -> str:
        """Format risk comparison"""
        risk_data = []
        for symbol, data in metrics.items():
            risk_level = "Low" if data['volatility'] < 20 else "Moderate" if data['volatility'] < 30 else "High"
            risk_data.append(f"- {symbol}: {risk_level} risk (Vol: {data['volatility']:.1f}%, Beta: {data['beta']:.2f})")
        return "\n".join(risk_data)
