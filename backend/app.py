from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.financial_orchestrator import FinancialOrchestrator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize the financial orchestrator
orchestrator = FinancialOrchestrator()

@app.route('/api/agents/research', methods=['POST'])
def research_agent():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        logger.info(f"Research agent request: {query}")
        
        # Get research agent output directly
        result = orchestrator.research_agent.research_company(query)
        
        # Return the full detailed research output for the discourse
        return jsonify({
            'success': True,
            'result': f"✅ Research phase completed successfully. Generated comprehensive research report with detailed financial data, competitive analysis, and market intelligence.\n\nFULL RESEARCH OUTPUT:\n{result}",
            'agent': 'Research Agent'
        })
        
    except Exception as e:
        logger.error(f"Error in research agent: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/agents/analysis', methods=['POST'])
def analysis_agent():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        logger.info(f"Analysis agent request: {query}")
        
        # Get analysis agent output directly
        result = orchestrator.analysis_agent.analyze_data(query)
        
        # Return the full detailed analysis output for the discourse
        return jsonify({
            'success': True,
            'result': f"✅ Financial analysis completed successfully. Generated comprehensive financial analysis with detailed calculations, ratio analysis, and risk assessment.\n\nFULL ANALYSIS OUTPUT:\n{result}",
            'agent': 'Analysis Agent'
        })
        
    except Exception as e:
        logger.error(f"Error in analysis agent: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/agents/recommendation', methods=['POST'])
def recommendation_agent():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        logger.info(f"Recommendation agent request: {query}")
        
        # Get recommendation agent output directly
        result = orchestrator.recommendation_agent.generate_recommendation(query)
        
        # Return the full detailed recommendations output for the discourse
        return jsonify({
            'success': True,
            'result': f"✅ Investment strategy formulation completed successfully. Generated comprehensive investment recommendations with detailed analysis and actionable insights.\n\nFULL RECOMMENDATIONS OUTPUT:\n{result}",
            'agent': 'Recommendation Agent'
        })
        
    except Exception as e:
        logger.error(f"Error in recommendation agent: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_financial_data():
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        company = data.get('company', '')
        
        logger.info(f"Received analysis request for query: {query}")
        
        # Run the multi-agent analysis
        result = orchestrator.orchestrate_analysis(query, company)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/api/agents', methods=['GET'])
def get_agents():
    agents_info = orchestrator.get_agents_info()
    return jsonify(agents_info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
