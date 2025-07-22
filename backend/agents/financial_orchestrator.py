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
        Generate a comprehensive professional financial report
        """
        report_prompt = f"""
        Create a professional financial analysis report based on:

        QUERY: {query}
        RESEARCH: {research}
        ANALYSIS: {analysis} 
        RECOMMENDATIONS: {recommendations}

        Create a comprehensive report (800-1200 words) with:

        # EXECUTIVE SUMMARY
        [200 word summary covering investment recommendation, key metrics, and target price]

        # INVESTMENT THESIS
        [300 words covering key arguments, competitive advantages, and value drivers]

        # FINANCIAL ANALYSIS
        [300 words covering ratio analysis, profitability trends, and financial projections]

        # RISK ASSESSMENT
        [200 words covering primary risks and mitigation strategies]

        # RECOMMENDATIONS
        [200 words covering specific recommendations, position sizing, and monitoring points]

        Include specific financial metrics, ratios, and quantitative analysis.
        Add disclaimers emphasizing this is research, not personalized advice.
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
