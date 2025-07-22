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
