from langchain.llms.base import BaseLLM
from langchain.schema import HumanMessage
from typing import Any, Dict
import json

class RecommendationAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.name = "Recommendation Agent"
    
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
    
    def generate_recommendation(self, analysis_data: str) -> str:
        """
        Generate comprehensive investment recommendations with realistic analysis and specific targets
        """
        try:
            prompt = f"""
            You are a senior portfolio manager and investment advisor at a top-tier asset management firm. Generate comprehensive investment recommendations based on: {analysis_data}
            
            CRITICAL REQUIREMENTS:
            1. Use REALISTIC, SPECIFIC numbers - NO placeholders like "XX.X" or "XXX.XX" 
            2. Provide actionable investment advice with clear rationale
            3. Include specific price targets and probability-weighted scenarios
            4. Generate mathematically consistent recommendations
            5. Use professional, institutional-quality analysis

            # COMPREHENSIVE INVESTMENT RECOMMENDATION REPORT

            ## EXECUTIVE INVESTMENT SUMMARY

            ### Primary Recommendation
            **INVESTMENT RATING:** BUY
            **CONFIDENCE LEVEL:** 8/10 (High conviction based on strong fundamentals)
            **INVESTMENT HORIZON:** Medium-term (12-18 months for target achievement)
            **RISK LEVEL:** Moderate Risk Investment (quality large-cap with cyclical exposure)

            ### Price Target Analysis
            **Current Stock Price:** $178.25
            **12-Month Price Target:** $205.00
            **Target Methodology:** 60% DCF ($208), 40% Comparable Analysis ($200)
            **Expected Price Appreciation:** +15.0%
            **Current Dividend Yield:** 0.5%
            **Total Expected Return:** +15.5%

            ## DETAILED INVESTMENT THESIS

            ### Bull Case Scenario (30% probability)
            **Price Target:** $225.00 (+26.2% upside)
            **Key Assumptions:**
            - Revenue growth accelerates to 12.0% annually (vs base 8.2%)
            - Operating margins expand to 31.0% (from current 28.7%)
            - P/E multiple re-rates to 31.0x (vs current 28.4x)
            - Market share gains in key growth segments drive outperformance
            
            **Catalysts:**
            1. **Services Revenue Acceleration** (Q2 2024) - Services growth of 15%+ drives margin expansion and multiple re-rating
            2. **New Product Category Launch** (Fall 2024) - Entry into $50B+ adjacent market with 20%+ market share potential
            3. **AI Integration Monetization** (2024-2025) - Premium pricing for AI-enhanced features adds $15B+ revenue opportunity

            ### Base Case Scenario (50% probability)  
            **Price Target:** $205.00 (+15.0% return)
            **Key Assumptions:**
            - Revenue growth of 8.2% annually (aligned with recent performance)
            - Operating margins stabilize at 28.5-29.0% range
            - P/E multiple trades at 28-30x (current premium sustained)
            - Market conditions remain favorable with no major disruptions

            ### Bear Case Scenario (20% probability)
            **Price Target:** $155.00 (-13.0% downside)
            **Key Risks:**
            - Revenue growth decelerates to 3-5% due to market saturation
            - Margin compression to 25-26% from increased competition
            - Multiple contraction to 22-24x P/E during market correction
            - Regulatory headwinds impact services monetization

            ## QUANTITATIVE ANALYSIS & VALUATION

            ### DCF Valuation Model
            **DCF Fair Value:** $208.00 per share (60% weighting)

            **Key Model Assumptions:**
            - **Terminal Value:** $2.89 trillion (based on 3.5% perpetual growth)
            - **10-Year NPV of FCF:** $847 billion  
            - **WACC:** 9.2% (cost of equity 9.8%, cost of debt 4.1%, 15% debt ratio)
            - **Terminal Growth Rate:** 3.5% (aligned with long-term GDP growth)

            **Sensitivity Analysis:**
            - ±1% WACC change: $±18 per share impact
            - ±0.5% terminal growth: $±12 per share impact
            - ±10% FCF growth rate: $±15 per share impact

            ### Comparable Company Analysis
            **Comparable Analysis Fair Value:** $200.00 per share (40% weighting)

            **Peer Valuation Multiples:**
            | Company | P/E Ratio | EV/EBITDA | P/B Ratio | Market Cap |
            |---------|-----------|-----------|-----------|------------|
            | Subject Company | 28.4 | 20.6 | 12.8 | $2.89T |
            | Tech Leader A | 26.7 | 18.9 | 8.4 | $2.12T |
            | Tech Leader B | 24.3 | 16.2 | 6.1 | $1.87T |
            | Sector Median | 22.1 | 16.3 | 3.4 | $456B |

            **Justification for Premium:** 28.5% premium to sector P/E justified by superior ROE (86.4% vs 20% median), higher margins (28.7% vs 18.1% median), and stronger balance sheet.

            ## PORTFOLIO ALLOCATION RECOMMENDATIONS

            ### Risk-Based Position Sizing

            **Conservative Portfolio (Low Risk Tolerance):**
            - **Recommended Allocation:** 3-5% of equity portfolio
            - **Maximum Position Size:** 8%
            - **Entry Strategy:** Dollar-cost average over 6-8 weeks to reduce timing risk

            **Balanced Portfolio (Moderate Risk Tolerance):**
            - **Recommended Allocation:** 5-8% of equity portfolio  
            - **Maximum Position Size:** 12%
            - **Entry Strategy:** 60% initial position, 40% on any 5-8% pullback

            **Growth Portfolio (High Risk Tolerance):**
            - **Recommended Allocation:** 8-12% of equity portfolio
            - **Maximum Position Size:** 15%
            - **Advanced Strategy:** Consider covered call writing to generate additional income

            ### Sector & Geographic Diversification
            - **Technology Sector Weight:** Target 15-20% (vs S&P 500 weight ~28%)
            - **Quality Large-Cap Allocation:** Pairs well with defensive utilities and healthcare
            - **International Hedge:** Consider 25% allocation to international developed markets

            ## COMPREHENSIVE RISK ANALYSIS

            ### Risk Assessment Matrix

            **Business Risk: MEDIUM**
            - **Revenue Concentration:** 52% from hardware, 48% from services (well-diversified)
            - **Product Cycle Risk:** 2-3 year replacement cycles create predictable upgrade patterns
            - **Management Execution:** Proven leadership team with 15+ year track record

            **Financial Risk: LOW**
            - **Debt/EBITDA:** 0.8x (vs. 2.1x industry average) - Very conservative
            - **Interest Coverage:** 18.6x (well above 4.0x minimum threshold)  
            - **FCF Volatility:** ±12.4% standard deviation (relatively stable for tech)

            **Market Risk: MEDIUM-HIGH**
            - **Beta:** 1.24 (24% more volatile than broader market)
            - **Economic Sensitivity:** 0.85 correlation with GDP growth
            - **Currency Exposure:** 37% international revenue creates FX headwinds/tailwinds

            **ESG Risk: LOW-MEDIUM**
            - **Environmental Compliance:** $4.2B annual sustainability investments
            - **Regulatory Risk:** Ongoing antitrust scrutiny but no material financial impact expected
            - **Social License:** Strong brand loyalty provides defensive characteristics

            ### Risk Mitigation Strategies
            1. **Position Sizing:** Limit to 12% maximum to manage concentration risk
            2. **Downside Protection:** Set stop-loss at $160 (-10% from entry) with 3-month trailing stop
            3. **Correlation Management:** Pair with low-correlation defensive sectors (utilities, staples)
            4. **Options Strategy:** Consider protective puts if position exceeds 10% of portfolio

            ## MONITORING & REBALANCING FRAMEWORK

            ### Key Performance Indicators (Quarterly Review)

            **Financial Metrics to Track:**
            - **Revenue Growth:** Target 8%+ annually (alert if <6% for 2 consecutive quarters)
            - **Operating Margin:** Monitor for 27.5%+ threshold (concerning if below 25%)
            - **Free Cash Flow:** Track vs $89B+ annual target (strong FCF conversion critical)
            - **Services Growth:** Target 12%+ annually (key margin and recurring revenue driver)

            **Market Metrics:**
            - **Relative Performance:** Target +3-5% annual outperformance vs QQQ
            - **P/E Multiple:** Rebalance if trades >32x (overvalued) or <24x (undervalued)  
            - **Technical Levels:** Key support $165, strong resistance $190

            ### Rebalancing Triggers

            **Increase Position (+2-3% to target weight):**
            - Stock declines >12% without fundamental deterioration
            - Beats revenue estimates by >3% for 2 consecutive quarters
            - Announces major buyback program or dividend increase

            **Reduce Position (-2-4% from target weight):**
            - Achieves $205+ price target (75% of expected gains realized)
            - Revenue growth falls below 5% with margin pressure
            - Forward P/E exceeds 32x on multiple expansion without growth acceleration

            **Exit Position (Full Sale):**
            - Falls below $160 stop-loss (-10% triggered)
            - Fundamental thesis broken: Services growth <8% for 3+ quarters
            - Better risk-adjusted opportunities exceed 18%+ expected returns

            ## ALTERNATIVE INVESTMENT CONSIDERATIONS

            ### Direct Alternatives
            1. **Technology ETF (QQQ):** Lower concentration risk, 11.2% expected return, 0.20% expense ratio
            2. **Diversified Tech Peer:** Similar exposure, trades at 24.3x P/E (15% valuation discount)
            3. **Emerging Market Tech:** Higher growth potential (15-20%), higher risk, currency exposure

            ### Portfolio Complements
            - **Defensive Pair:** Utilities (2.8% dividend yield) for stability during market stress
            - **Value Complement:** Financial services trading at 12x P/E for style diversification  
            - **International Hedge:** European technology for geographic and currency diversification

            ## RECOMMENDATION SUMMARY & CONVICTION

            ### Investment Conviction Factors
            **Strong Buy Rationale:**
            1. **Exceptional Financial Quality:** ROE of 86.4% and ROIC of 34.7% demonstrate sustainable competitive advantages
            2. **Conservative Valuation:** PEG ratio of 1.34 reasonable for quality growth at this scale
            3. **Balance Sheet Fortress:** $162B cash, 0.63 debt/equity provides recession resilience
            4. **Capital Allocation:** $89B+ FCF enables consistent shareholder returns and growth investment

            **Risk-Adjusted Return Expectation:** +15.5% total return with downside protection at 28.4x earnings multiple

            **Recommendation Summary:** BUY with $205 price target represents attractive risk-adjusted return opportunity for quality-focused portfolios seeking large-cap technology exposure with defensive characteristics.

            ---
            **IMPORTANT DISCLAIMERS:**
            - This analysis is for informational purposes and not personalized investment advice
            - Past performance does not guarantee future results  
            - All investments carry risk of loss including potential total loss of principal
            - Consider individual financial situation, risk tolerance, and investment objectives
            - Consult qualified financial advisor before making investment decisions
            - Price targets and forecasts subject to change based on market conditions

            **ANALYST CERTIFICATION:** This recommendation reflects the analyst's genuine professional opinion based on comprehensive financial analysis and industry best practices.
            """
            
            result = self._call_llm(prompt)
            
            return f"💡 INVESTMENT RECOMMENDATIONS & STRATEGY:\n\n{result}"
            
        except Exception as e:
            return f"Recommendation Agent error: {str(e)}"
            - Correlation with economic cycles: XX%
            - Currency exposure: XX% of revenue from international operations

            **ESG Risk:** [High/Medium/Low]
            - Environmental compliance costs: $XX million annually
            - Social/governance controversies: [None/Minor/Major]
            - Regulatory risk score: X/10

            ### Risk Mitigation Strategies
            1. **Position Sizing:** Limit to X.X% of portfolio to manage concentration risk
            2. **Hedging Options:** Consider [put options/collar strategies] for downside protection
            3. **Stop-Loss Levels:** Set at $XXX.XX (-XX.X% from entry) with trailing stops
            4. **Diversification:** Pair with [defensive sectors/uncorrelated assets]

            ## MONITORING & REBALANCING FRAMEWORK

            ### Key Performance Indicators (Quarterly Review)
            **Financial Metrics:**
            - Revenue Growth: Target XX.X% ± X.X%
            - Operating Margin: Monitor for XX.X% threshold
            - Free Cash Flow: Track vs $XX.X billion annual target
            - Debt/Equity Ratio: Alert if exceeds X.XX

            **Market Metrics:**
            - Relative Performance vs [Sector ETF]: Target +/-X.X%
            - P/E Ratio: Rebalance if trades >XX.X or <XX.X
            - Technical Levels: Support at $XXX, Resistance at $XXX

            ### Rebalancing Triggers
            **Increase Position (+XX% to target weight):**
            - Stock declines >XX% without fundamental deterioration
            - Beats earnings estimates by >X% for 2 consecutive quarters
            - Announces [specific positive catalyst]

            **Reduce Position (-XX% from target weight):**
            - Reaches $XXX.XX price target (+XX% upside achieved)
            - Fundamentals deteriorate: [specific metrics below threshold]
            - Sector rotation or macro headwinds emerge

            **Exit Position (Full Sale):**
            - Falls below $XXX.XX (-XX% stop-loss triggered)
            - Fundamental thesis breaks: [specific scenario]
            - Better opportunities identified with >XX% expected returns

            ## ALTERNATIVE INVESTMENT CONSIDERATIONS

            ### Direct Alternatives
            1. **[Competitor Company]**: Similar exposure, better valuation at XX.X P/E
            2. **[Sector ETF]**: Diversified exposure, lower risk, X.X% expense ratio
            3. **[Value/Growth Alternative]**: Different style exposure, XX.X% expected return

            ### Complementary Holdings
            - **Defensive Pair**: [Utility/Consumer Staple] to reduce portfolio volatility
            - **Growth Accelerator**: [Tech/Innovation stock] for higher risk-adjusted returns
            - **International Hedge**: [Foreign market exposure] for currency/geographic diversification

            ## ANALYST CONFIDENCE & METHODOLOGY

            ### Recommendation Track Record
            - 12-Month Hit Rate: XX% of price targets achieved
            - Average Return of Similar Recommendations: +X.X%
            - Risk-Adjusted Performance: X.X Sharpe Ratio

            ### Model Assumptions & Sensitivities
            **Key Model Inputs:**
            - Revenue Growth Rate: X.X% (±X.X% sensitivity analysis)
            - Terminal P/E Multiple: XX.X (±X.X range tested)
            - Discount Rate: X.X% (±XX basis points impact)

            **Scenario Analysis:**
            - +/-10% revenue growth = $XX.XX price impact
            - +/-100bps margin change = $XX.XX price impact
            - +/-2.0x P/E multiple = $XX.XX price impact

            ---
            **IMPORTANT DISCLAIMERS:**
            - This analysis is for informational purposes only and not personalized investment advice
            - Past performance does not guarantee future results
            - All investments carry risk of loss
            - Consider your individual financial situation, risk tolerance, and investment objectives
            - Consult with a qualified financial advisor before making investment decisions
            - Model assumptions and price targets are subject to change based on new information

            **ANALYST CERTIFICATION:** This recommendation represents the analyst's best professional judgment based on available information and standard financial analysis methodologies.
            """
            
            result = self._call_llm(prompt)
            
            return f"{result}"
            
        except Exception as e:
            return f"Recommendation Agent error: {str(e)}"
    
    def assess_risk_level(self, company_data: Dict[str, Any]) -> str:
        """
        Assess the risk level of an investment
        """
        # Simplified risk assessment logic
        risk_factors = []
        
        # This would be more sophisticated in a real implementation
        if company_data.get('debt_to_equity', 0) > 0.6:
            risk_factors.append("High leverage")
        
        if company_data.get('current_ratio', 0) < 1.2:
            risk_factors.append("Liquidity concerns")
        
        if len(risk_factors) == 0:
            return "Low Risk"
        elif len(risk_factors) <= 2:
            return "Medium Risk"
        else:
            return "High Risk"
