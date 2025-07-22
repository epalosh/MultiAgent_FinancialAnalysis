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
        
        logger.info(f"🔍 Research agent request: {query}")
        
        # Get research agent output directly
        result = orchestrator.research_agent.research_company(query)
        
        logger.info(f"✅ Research completed - {len(result)} characters generated")
        
        return jsonify({
            'success': True,
            'result': result,
            'agent': 'Research Agent',
            'output_length': len(result)
        })
        
    except Exception as e:
        logger.error(f"❌ Error in research agent: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/agents/analysis', methods=['POST'])
def analysis_agent():
    try:
        data = request.get_json()
        query = data.get('query', '')
        context = data.get('context', '')  # Previous agent outputs for context
        
        logger.info(f"📊 Analysis agent request: {query}")
        
        # Get analysis agent output with context
        full_input = f"{query}\n\nContext from previous analysis:\n{context}" if context else query
        result = orchestrator.analysis_agent.analyze_data(full_input)
        
        logger.info(f"✅ Analysis completed - {len(result)} characters generated")
        
        return jsonify({
            'success': True,
            'result': result,
            'agent': 'Analysis Agent',
            'output_length': len(result)
        })
        
    except Exception as e:
        logger.error(f"❌ Error in analysis agent: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/agents/recommendation', methods=['POST'])
def recommendation_agent():
    try:
        data = request.get_json()
        query = data.get('query', '')
        context = data.get('context', '')  # Previous agent outputs for context
        
        logger.info(f"💡 Recommendation agent request: {query}")
        
        # Get recommendation agent output with full context
        full_input = f"{query}\n\nContext from previous analysis:\n{context}" if context else query
        result = orchestrator.recommendation_agent.generate_recommendation(full_input)
        
        logger.info(f"✅ Recommendations completed - {len(result)} characters generated")
        
        return jsonify({
            'success': True,
            'result': result,
            'agent': 'Recommendation Agent',
            'output_length': len(result)
        })
        
    except Exception as e:
        logger.error(f"❌ Error in recommendation agent: {str(e)}")
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
        
        logger.info(f"🚀 Starting comprehensive financial analysis for: {query}")
        
        # Run the multi-agent analysis with extended processing
        result = orchestrator.orchestrate_analysis(query, company)
        
        if result.get('success', True):  # Default to True if not specified for backward compatibility
            logger.info(f"✅ Analysis completed successfully - Generated {result.get('total_length', 'unknown')} characters")
            return jsonify({
                'success': True,
                'result': result
            })
        else:
            logger.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            return jsonify({
                'success': False,
                'error': result.get('error', 'Analysis failed')
            }), 500
        
    except Exception as e:
        logger.error(f"❌ Critical error in analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analyze-enhanced', methods=['POST'])
def analyze_financial_data_enhanced():
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        company = data.get('company', '')
        
        logger.info(f"🚀 Starting ENHANCED financial analysis with REAL data for: {query}")
        
        # Run the enhanced multi-agent analysis with real data
        result = orchestrator.orchestrate_enhanced_analysis(query, company)
        
        if result.get('success', True):
            logger.info(f"✅ Enhanced analysis completed successfully - Generated {result.get('total_length', 'unknown')} characters")
            return jsonify({
                'success': True,
                'result': result,
                'data_sources': result.get('data_sources', []),
                'enhanced': True
            })
        else:
            logger.error(f"❌ Enhanced analysis failed: {result.get('error', 'Unknown error')}")
            return jsonify({
                'success': False,
                'error': result.get('error', 'Enhanced analysis failed')
            }), 500
        
    except Exception as e:
        logger.error(f"❌ Critical error in enhanced analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/quick-analysis', methods=['POST'])
def quick_stock_analysis():
    try:
        data = request.get_json()
        
        if not data or 'symbol' not in data:
            return jsonify({'error': 'Stock symbol is required'}), 400
        
        symbol = data['symbol'].upper()
        
        logger.info(f"🔍 Quick analysis for: {symbol}")
        
        # Get quick analysis using enhanced research agent
        result = orchestrator.enhanced_research_agent.get_quick_analysis(symbol)
        
        logger.info(f"✅ Quick analysis completed for {symbol}")
        
        return jsonify({
            'success': True,
            'result': result,
            'symbol': symbol,
            'analysis_type': 'quick'
        })
        
    except Exception as e:
        logger.error(f"❌ Error in quick analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/compare-stocks', methods=['POST'])
def compare_stocks():
    try:
        data = request.get_json()
        
        if not data or 'symbols' not in data:
            return jsonify({'error': 'Stock symbols are required'}), 400
        
        symbols = data['symbols']
        if isinstance(symbols, str):
            symbols = [s.strip().upper() for s in symbols.split(',')]
        elif isinstance(symbols, list):
            symbols = [s.strip().upper() for s in symbols]
        else:
            return jsonify({'error': 'Invalid symbols format'}), 400
        
        logger.info(f"📊 Comparing stocks: {symbols}")
        
        # Get comparison analysis using enhanced analysis agent
        result = orchestrator.enhanced_analysis_agent.compare_stocks(symbols)
        
        logger.info(f"✅ Stock comparison completed for {len(symbols)} stocks")
        
        return jsonify({
            'success': True,
            'result': result,
            'symbols': symbols,
            'analysis_type': 'comparison'
        })
        
    except Exception as e:
        logger.error(f"❌ Error in stock comparison: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/market-data', methods=['POST'])
def get_market_data():
    try:
        data = request.get_json()
        
        if not data or 'symbol' not in data:
            return jsonify({'error': 'Stock symbol is required'}), 400
        
        symbol = data['symbol'].upper()
        
        logger.info(f"📈 Getting market data for: {symbol}")
        
        # Get real-time market data
        result = orchestrator.enhanced_research_agent.get_market_data(symbol)
        
        logger.info(f"✅ Market data retrieved for {symbol}")
        
        return jsonify({
            'success': True,
            'result': result,
            'symbol': symbol,
            'data_type': 'market_data'
        })
        
    except Exception as e:
        logger.error(f"❌ Error getting market data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-report', methods=['POST'])
def generate_comprehensive_report():
    try:
        data = request.get_json()
        query = data.get('query', '')
        research = data.get('research', '')
        analysis = data.get('analysis', '')
        recommendations = data.get('recommendations', '')
        
        logger.info(f"📋 Generating comprehensive report for: {query}")
        
        # Generate comprehensive integrated report using the orchestrator
        comprehensive_report = orchestrator._generate_comprehensive_report(
            query, research, analysis, recommendations
        )
        
        logger.info(f"✅ Comprehensive report generated - {len(comprehensive_report)} characters")
        
        return jsonify({
            'success': True,
            'comprehensive_report': comprehensive_report,
            'report_length': len(comprehensive_report)
        })
        
    except Exception as e:
        logger.error(f"❌ Error generating comprehensive report: {str(e)}")
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
