from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import OpenAI
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
        
        # Initialize LLM
        self.llm = OpenAI(
            temperature=config.AGENT_TEMPERATURE,
            api_key=self.openai_api_key
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
        Main orchestration method that coordinates multiple agents
        """
        try:
            # Enhance the query with context
            enhanced_query = f"""
            Please analyze the following financial query: {query}
            {f'For company: {company}' if company else ''}
            
            Follow this process:
            1. First, use Research_Company to gather relevant financial information
            2. Then, use Analyze_Financial_Data to perform detailed analysis
            3. Finally, use Generate_Recommendations to provide actionable insights
            
            Provide a comprehensive response that includes all findings from each agent.
            """
            
            # Run the orchestrator agent
            result = self.orchestrator_agent.invoke({"input": enhanced_query})
            
            return {
                'query': query,
                'company': company,
                'analysis': result.get('output', str(result)),
                'agents_used': ['Research Agent', 'Analysis Agent', 'Recommendation Agent'],
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            return {
                'query': query,
                'company': company,
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
    
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
