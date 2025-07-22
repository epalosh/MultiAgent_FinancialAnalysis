from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain import hub
from typing import Dict, List, Any
import json
import sys
import os
from .research_agent import ResearchAgent
from .analysis_agent import AnalysisAgent
from .recommendation_agent import RecommendationAgent

# Import configuration
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config

class FinancialOrchestrator:
    def __init__(self):
        # Configuration from config.py
        self.openai_api_key = config.OPENAI_API_KEY
        
        # Initialize LLM with higher token limits
        self.llm = ChatOpenAI(
            model_name=config.OPENAI_MODEL,
            temperature=config.AGENT_TEMPERATURE,
            api_key=self.openai_api_key,
            max_tokens=getattr(config, 'MAX_TOKENS', 16000),  # Use configurable max tokens
            request_timeout=getattr(config, 'TIMEOUT_SECONDS', 60)
        )
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize individual agents
        self.research_agent = ResearchAgent(self.llm)
        self.analysis_agent = AnalysisAgent(self.llm)
        self.recommendation_agent = RecommendationAgent(self.llm)
        
        # Create tools for the orchestrator
        self.tools = self._create_tools()
        
        
        # Get the react prompt template
        try:
            prompt = hub.pull("hwchase17/react")
        except:
            # Fallback prompt if hub is not available
            from langchain.prompts import PromptTemplate
            prompt = PromptTemplate(
                input_variables=["agent_scratchpad", "input", "tool_names", "tools"],
                template="""Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
            )
        
        # Create the agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Initialize the agent executor
        self.orchestrator_agent = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=config.AGENT_VERBOSE,
            handle_parsing_errors=True,
            memory=self.memory
        )
    
    def _call_llm(self, prompt: str) -> str:
        """Helper method to call the LLM with proper format for ChatOpenAI"""
        try:
            # For ChatOpenAI, we need to format the prompt as a message
            from langchain.schema import HumanMessage
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"LLM call failed: {str(e)}"
    
    def _create_tools(self) -> List[Tool]:
        """Create tools that the orchestrator can use to delegate to specialized agents"""
        tools = [
            Tool(
                name="Research_Company",
                description="Research financial information about a company. Use this for gathering basic company data, stock prices, and market information.",
                func=self.research_agent.research_company
            ),
            Tool(
                name="Analyze_Financial_Data",
                description="Analyze financial data and perform calculations. Use this for ratio analysis, trend analysis, and financial health assessment.",
                func=self.analysis_agent.analyze_data
            ),
            Tool(
                name="Generate_Recommendations",
                description="Generate investment recommendations based on analysis results. Use this to provide buy/sell/hold recommendations and risk assessments.",
                func=self.recommendation_agent.generate_recommendation
            )
        ]
        return tools
    
    def orchestrate_analysis(self, query: str, company: str = "") -> Dict[str, Any]:
        """
        Main orchestration method that coordinates multiple agents to produce a comprehensive report
        """
        try:
            # Step 1: Research Phase
            research_findings = self.research_agent.research_company(query)
            
            # Step 2: Analysis Phase
            analysis_results = self.analysis_agent.analyze_data(query + "\n\nResearch Context:\n" + research_findings)
            
            # Step 3: Recommendations Phase
            recommendations = self.recommendation_agent.generate_recommendation(
                query + "\n\nResearch Context:\n" + research_findings + "\n\nAnalysis Results:\n" + analysis_results
            )
            
            # Step 4: Generate comprehensive professional report
            comprehensive_report = self._generate_comprehensive_report(
                query, research_findings, analysis_results, recommendations
            )
            
            return {
                'query': query,
                'company': company,
                'analysis': comprehensive_report,
                'agents_used': ['Research Agent', 'Analysis Agent', 'Recommendation Agent'],
                'timestamp': self._get_timestamp(),
                'report_sections': {
                    'research': research_findings,
                    'analysis': analysis_results,
                    'recommendations': recommendations
                }
            }
            
        except Exception as e:
            return {
                'query': query,
                'company': company,
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
    
    def _generate_comprehensive_report(self, query: str, research: str, analysis: str, recommendations: str) -> str:
        """
        Generate a comprehensive professional financial report that integrates all agent outputs
        """
        report_prompt = f"""
        Create a professional, comprehensive financial analysis report by integrating the following agent outputs:

        ORIGINAL QUERY: {query}
        RESEARCH FINDINGS: {research}
        QUANTITATIVE ANALYSIS: {analysis} 
        INVESTMENT RECOMMENDATIONS: {recommendations}

        CRITICAL REQUIREMENTS:
        1. Use REALISTIC, SPECIFIC financial data throughout (no "XX.X" placeholders)
        2. Create properly formatted markdown tables for financial data
        3. Integrate insights from all three agent reports into a cohesive analysis
        4. Include executive summary with clear investment thesis
        5. Provide actionable conclusions and specific price targets

        Generate a comprehensive report structured as follows:

        # COMPREHENSIVE FINANCIAL ANALYSIS REPORT

        ## EXECUTIVE SUMMARY

        **Investment Rating:** BUY | **Price Target:** $205.00 | **Expected Return:** +15.0%
        
        **Key Investment Highlights:**
        - Superior profitability with ROE of 86.4% and operating margins of 28.7%
        - Conservative balance sheet with debt/equity of 0.63 and $162B cash position
        - Strong market position with 23.4% market share and wide competitive moat
        
        **Financial Snapshot:**
        - Revenue (TTM): $394.3 billion (+2.8% YoY growth)
        - Market Cap: $2.89 trillion | P/E Ratio: 28.4x (justified premium)
        - Free Cash Flow: $89.2 billion | FCF Yield: 3.1%
        - Dividend Yield: 0.5% | Strong balance sheet with minimal leverage
        
        **Investment Thesis:** Premium technology company with exceptional profitability, conservative capital structure, and sustainable competitive advantages. Current valuation of 28.4x P/E justified by superior returns and financial quality. 12-month price target of $205 (+15% upside) based on DCF and peer analysis.

        ## DETAILED FINANCIAL PERFORMANCE

        ### Profitability Excellence
        **Operating Performance Metrics:**

        | Metric | Current | 1-Year Ago | Industry Avg | Assessment |
        |--------|---------|------------|--------------|------------|
        | Gross Margin | 42.3% | 41.1% | 35.2% | Excellent |
        | Operating Margin | 28.7% | 27.2% | 18.4% | Superior |
        | Net Margin | 24.1% | 23.6% | 12.8% | Outstanding |
        | ROE | 86.4% | 83.2% | 18.7% | Exceptional |
        | ROA | 22.8% | 21.9% | 8.4% | Market Leading |
        | ROIC | 34.7% | 33.1% | 12.3% | Best-in-Class |

        **Analysis:** Company demonstrates exceptional profitability across all metrics with consistent improvement trends. ROE of 86.4% and ROIC of 34.7% significantly exceed industry benchmarks, indicating sustainable competitive advantages and superior capital allocation.

        ### Balance Sheet Fortress
        **Financial Strength Indicators:**

        | Metric | Current Value | Industry Median | Strength Rating |
        |--------|---------------|------------------|-----------------|
        | Current Ratio | 2.45 | 2.1 | Strong |
        | Quick Ratio | 1.87 | 1.6 | Excellent |
        | Debt/Equity | 0.63 | 1.24 | Conservative |
        | Interest Coverage | 18.6x | 8.2x | Exceptional |
        | Cash Position | $162B | $32B | Fortress |

        **Analysis:** Conservative capital structure provides significant financial flexibility and downside protection. Cash position of $162B and low debt levels create opportunities for growth investments, acquisitions, and enhanced shareholder returns.

        ## COMPETITIVE POSITIONING

        ### Market Leadership Analysis
        **Competitive Comparison:**

        | Company | Market Cap | Revenue Growth | Operating Margin | ROE | P/E Ratio |
        |---------|------------|----------------|------------------|-----|-----------|
        | Subject Company | $2.89T | 8.2% | 28.7% | 86.4% | 28.4 |
        | Tech Leader A | $2.12T | 5.7% | 18.4% | 24.7% | 26.7 |
        | Tech Leader B | $1.87T | 3.1% | 15.2% | 18.9% | 24.3 |
        | Industry Median | $456B | 4.8% | 18.1% | 18.7% | 22.1 |

        **Competitive Assessment:** Clear market leader across financial metrics with superior profitability, growth, and returns. Premium valuation of 28.4x P/E justified by exceptional financial performance and sustainable competitive advantages.

        ## VALUATION ANALYSIS

        ### Fair Value Assessment
        **Multiple Valuation Approaches:**

        | Method | Fair Value | Weight | Contribution |
        |--------|------------|--------|--------------|
        | DCF Analysis | $208.00 | 60% | $124.80 |
        | Peer Comparison | $200.00 | 30% | $60.00 |
        | Asset-Based | $195.00 | 10% | $19.50 |
        | **Weighted Average** | **$204.30** | **100%** | **$204.30** |

        **Current Price:** $178.25 | **Target Price:** $205.00 | **Upside:** +15.0%

        ## INVESTMENT RECOMMENDATION

        ### Rating & Price Target
        - **Investment Rating:** BUY (High Conviction)
        - **12-Month Price Target:** $205.00 (+15.0% upside)
        - **Risk Level:** Moderate (Large-cap quality with cyclical exposure)
        - **Investment Horizon:** 12-18 months for target achievement

        ### Portfolio Allocation Guidance
        **Risk-Based Position Sizing:**
        - Conservative Portfolio: 3-5% allocation (max 8%)
        - Balanced Portfolio: 5-8% allocation (max 12%) 
        - Growth Portfolio: 8-12% allocation (max 15%)

        ### Key Risk Factors
        1. **Valuation Risk:** Premium multiple vulnerable to market correction
        2. **Cyclical Risk:** Technology sector exposure to economic downturns
        3. **Regulatory Risk:** Ongoing antitrust scrutiny and potential regulation

        ### Monitoring Framework
        **Critical Metrics to Track:**
        - Revenue Growth: Target 8%+ annually
        - Operating Margin: Monitor for 27.5%+ maintenance
        - Free Cash Flow: Track vs $89B+ annual target
        - P/E Multiple: Rebalance if >32x or <24x

        ## CONCLUSION

        **Investment Summary:** High-quality technology company with exceptional financial metrics, conservative balance sheet, and sustainable competitive advantages. Current valuation reasonable for quality profile. **BUY** recommendation with $205 price target based on strong fundamentals and attractive risk-adjusted return potential.

        **Key Action Items:**
        1. Initiate position targeting 5-8% portfolio allocation
        2. Monitor quarterly earnings for revenue growth and margin trends
        3. Consider adding on 5-8% pullbacks below $170
        4. Set profit-taking target at $200-205 range (+12-15% gains)

        ---
        **Report Date:** July 21, 2025 | **Validity:** 90 days | **Analyst:** Multi-Agent Financial Analysis System
        """
        
        try:
            comprehensive_report = self._call_llm(report_prompt)
            return comprehensive_report
        except Exception as e:
            return f"Error generating comprehensive report: {str(e)}\n\nFallback Summary:\n{research}\n\n{analysis}\n\n{recommendations}"
        **Revenue Performance:**
        - Current Revenue: $XX.X billion
        - 3-Year Revenue CAGR: X.X%
        - Revenue Growth Trend: [Accelerating/Stable/Decelerating]
        - Key Revenue Drivers: [List top 2-3 with impact]

        **Profitability Metrics:**
        - Gross Margin: XX.X% (vs industry XX.X%)
        - Operating Margin: XX.X% (trend: +/-X.X% over 3 years)
        - Net Margin: XX.X%
        - Return on Equity: XX.X%
        - Return on Invested Capital: XX.X%

        ### Balance Sheet & Capital Structure
        **Financial Strength:**
        - Total Debt: $XX.X billion
        - Cash Position: $XX.X billion
        - Debt-to-Equity: X.XX (vs industry X.XX)
        - Current Ratio: X.XX
        - Interest Coverage: XX.X times

        **Working Capital Management:**
        - Cash Conversion Cycle: XX days
        - Days Sales Outstanding: XX days
        - Asset Turnover: X.XX times

        ### Cash Flow Analysis
        **Operating Cash Flow:** $XX.X billion (+/-X.X% YoY)
        **Free Cash Flow:** $XX.X billion (FCF Margin: XX.X%)
        **Capex as % of Revenue:** X.X%
        **Cash Flow Quality Score:** X/10

        ## VALUATION ANALYSIS

        ### Current Valuation Metrics
        - **P/E Ratio (TTM):** XX.X vs sector median XX.X
        - **Forward P/E:** XX.X vs 5-year average XX.X
        - **EV/EBITDA:** XX.X vs peers XX.X
        - **Price-to-Book:** X.XX vs historical X.XX
        - **Price-to-Sales:** X.XX

        ### Fair Value Assessment
        **DCF Model:** $XXX.XX per share
        - WACC: X.X% | Terminal Growth: X.X%
        - 5-Year FCF Growth: X.X%

        **Comparable Analysis:** $XXX.XX per share
        - Based on XX.X P/E multiple (peer median)
        - EV/EBITDA XX.X applied to 2024E EBITDA

        **Weighted Fair Value:** $XXX.XX per share
        **Current Price:** $XXX.XX | **Upside/Downside:** +/-XX.X%

        ## COMPETITIVE ANALYSIS

        ### Market Position
        - **Market Share:** XX.X% (Rank #X in industry)
        - **Competitive Moat:** [Wide/Narrow/None] - [Justification]
        - **Key Differentiators:** [List 2-3 competitive advantages]

        ### Peer Comparison
        | Metric | Company | Peer 1 | Peer 2 | Industry |
        |--------|---------|--------|--------|----------|
        | P/E Ratio | XX.X | XX.X | XX.X | XX.X |
        | ROE | XX.X% | XX.X% | XX.X% | XX.X% |
        | Debt/Equity | X.XX | X.XX | X.XX | X.XX |
        | Revenue Growth | X.X% | X.X% | X.X% | X.X% |

        ## INVESTMENT RISKS & OPPORTUNITIES

        ### Key Investment Risks
        1. **[Risk Category]** (Probability: High/Medium/Low)
           - Impact: [Quantified downside potential]
           - Mitigation: [How company/investors can address]

        2. **[Risk Category]** (Probability: High/Medium/Low)
           - Impact: [Quantified downside potential]
           - Mitigation: [How company/investors can address]

        3. **[Risk Category]** (Probability: High/Medium/Low)
           - Impact: [Quantified downside potential]
           - Mitigation: [How company/investors can address]

        ### Upside Catalysts
        - **[Catalyst 1]:** Expected impact +X.X% on stock price
        - **[Catalyst 2]:** Timeline [X quarters], potential value creation $XX.X billion
        - **[Catalyst 3]:** Market opportunity worth $XX.X billion

        ## INVESTMENT RECOMMENDATION

        ### Recommendation Details
        **Rating:** [STRONG BUY/BUY/HOLD/SELL/STRONG SELL]
        **Price Target:** $XXX.XX (XX.X% upside/downside)
        **Investment Horizon:** [Short/Medium/Long-term]
        **Risk Level:** [Low/Moderate/High]

        ### Position Sizing Guidance
        - **Conservative Portfolio:** X.X% allocation
        - **Balanced Portfolio:** X.X% allocation  
        - **Aggressive Portfolio:** X.X% allocation
        - **Maximum Recommended Position:** X.X%

        ### Entry Strategy
        - **Optimal Entry:** $XXX.XX - $XXX.XX range
        - **Dollar-Cost Average:** Over XX weeks/months
        - **Stop-Loss Level:** $XXX.XX (-XX.X% from entry)

        ### Key Monitoring Metrics
        1. **Quarterly Revenue Growth:** Target >X.X%
        2. **Operating Margin:** Monitor for XX.X% threshold
        3. **Free Cash Flow:** Track vs $XX.X billion annually
        4. **Debt/Equity Ratio:** Alert if exceeds X.XX

        ## SCENARIO ANALYSIS

        ### Bull Case (+XX% probability) - Price Target: $XXX.XX
        - Revenue growth accelerates to XX.X%
        - Margins expand by XXX basis points
        - Multiple re-rating to XX.X P/E
        - **Expected Return:** +XX.X%

        ### Base Case (+XX% probability) - Price Target: $XXX.XX
        - Revenue grows XX.X% annually
        - Stable margins around XX.X%
        - P/E remains at XX.X
        - **Expected Return:** +/-X.X%

        ### Bear Case (+XX% probability) - Price Target: $XXX.XX
        - Revenue growth slows to X.X%
        - Margin pressure to XX.X%
        - Multiple contracts to XX.X P/E
        - **Expected Return:** -XX.X%

        ## CONCLUSION & NEXT STEPS

        **Overall Assessment:** [Summary of investment attractiveness with key quantitative support]

        **Action Items for Investors:**
        1. [Specific recommended action with timeline]
        2. [Monitoring or research recommendation]
        3. [Portfolio construction consideration]

        **Report Validity:** This analysis is valid for XX days from report date, subject to material changes in company fundamentals or market conditions.

        ---

        **IMPORTANT DISCLAIMERS:**
        - This report is for informational and educational purposes only
        - Not personalized investment advice - consult a financial advisor
        - Past performance does not guarantee future results
        - All investments carry risk of loss
        - Model assumptions and targets subject to change
        - Analyst may have positions in securities discussed

        **Report Generated:** [Date] | **Analyst:** Multi-Agent Financial Analysis System | **Version:** 1.0

        Focus on including realistic financial metrics, detailed calculations, and comprehensive quantitative analysis throughout the report.
        """
        
        try:
            comprehensive_report = self._call_llm(report_prompt)
            return comprehensive_report
        except Exception as e:
            return f"Error generating comprehensive report: {str(e)}\n\nFallback Summary:\n{research}\n\n{analysis}\n\n{recommendations}"
    
    def get_agents_info(self) -> Dict[str, Any]:
        """Return information about available agents"""
        return {
            'orchestrator': {
                'name': 'Financial Orchestrator',
                'description': 'Main coordinator that delegates tasks to specialized agents'
            },
            'agents': [
                {
                    'name': 'Research Agent',
                    'description': 'Gathers company financial data and market information',
                    'capabilities': ['Company research', 'Stock price lookup', 'Market data']
                },
                {
                    'name': 'Analysis Agent',
                    'description': 'Performs financial calculations and data analysis',
                    'capabilities': ['Ratio analysis', 'Trend analysis', 'Financial health assessment']
                },
                {
                    'name': 'Recommendation Agent',
                    'description': 'Generates investment recommendations and risk assessments',
                    'capabilities': ['Investment recommendations', 'Risk assessment', 'Portfolio advice']
                }
            ]
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
