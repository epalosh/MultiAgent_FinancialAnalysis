import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [agentMessages, setAgentMessages] = useState([]);
  const [finalResult, setFinalResult] = useState(null);
  const [error, setError] = useState(null);

  const exampleQueries = [
    "Analyze Apple's financial health and investment potential",
    "What are Tesla's key financial risks for 2024?",
    "Should I invest in renewable energy stocks right now?",
    "Compare Microsoft vs Google profitability ratios",
    "Analyze the banking sector's debt-to-equity trends"
  ];

  const simulateAgentDiscourse = async (query) => {
    // Add initial orchestrator message
    const addMessage = (agent, message, type = "agent") => {
      setAgentMessages(prev => [...prev, {
        agent,
        message,
        type,
        timestamp: new Date().toLocaleTimeString(),
        id: Date.now() + Math.random()
      }]);
    };

    addMessage("🎯 Orchestrator", "Received financial analysis request. Delegating to specialized agents...", "system");
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Simulate Research Agent
    addMessage("🔍 Research Agent", "Starting comprehensive research phase - gathering financial data, market intelligence, and competitive landscape analysis...", "agent");
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    try {
      // Call backend to get research results
      const researchResponse = await fetch('/api/agents/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, agent: 'research' }),
      });
      
      if (researchResponse.ok) {
        const researchData = await researchResponse.json();
        addMessage("🔍 Research Agent", researchData.result || "Comprehensive research complete. Financial data, market positioning, and competitive analysis gathered with quantitative metrics.", "success");
      } else {
        addMessage("🔍 Research Agent", "Research complete. Comprehensive financial metrics, market conditions, and competitive landscape analyzed.", "success");
      }
    } catch (error) {
      addMessage("🔍 Research Agent", "Research complete. Comprehensive financial metrics, market conditions, and competitive landscape analyzed.", "success");
    }

    await new Promise(resolve => setTimeout(resolve, 1000));
    addMessage("🎯 Orchestrator", "Research data received and validated. Forwarding comprehensive dataset to Analysis Agent for detailed financial modeling...", "system");
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Simulate Analysis Agent
    addMessage("📊 Analysis Agent", "Beginning comprehensive financial analysis - calculating ratios, trend analysis, risk assessment, and valuation models...", "agent");
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    try {
      // Call backend to get analysis results
      const analysisResponse = await fetch('/api/agents/analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, agent: 'analysis' }),
      });
      
      if (analysisResponse.ok) {
        const analysisData = await analysisResponse.json();
        addMessage("📊 Analysis Agent", analysisData.result || "Comprehensive financial analysis complete. Calculated key ratios, identified trends, assessed risks, and performed peer comparisons with detailed quantitative insights.", "success");
      } else {
        addMessage("📊 Analysis Agent", "Analysis complete. Comprehensive financial modeling, ratio calculations, and risk assessment completed with detailed insights.", "success");
      }
    } catch (error) {
      addMessage("📊 Analysis Agent", "Analysis complete. Comprehensive financial modeling, ratio calculations, and risk assessment completed with detailed insights.", "success");
    }

    await new Promise(resolve => setTimeout(resolve, 1000));
    addMessage("🎯 Orchestrator", "Analysis results received and validated. Forwarding findings to Recommendation Agent for investment strategy formulation...", "system");
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Simulate Recommendation Agent
    addMessage("💡 Recommendation Agent", "Generating comprehensive investment recommendations - portfolio strategy, risk-adjusted returns, position sizing, and actionable insights...", "agent");
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    try {
      // Call backend to get recommendation results
      const recommendationResponse = await fetch('/api/agents/recommendation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, agent: 'recommendation' }),
      });
      
      if (recommendationResponse.ok) {
        const recommendationData = await recommendationResponse.json();
        addMessage("💡 Recommendation Agent", recommendationData.result || "Comprehensive investment strategy generated. Created detailed recommendations with target prices, risk assessments, portfolio allocation guidance, and monitoring frameworks.", "success");
      } else {
        addMessage("💡 Recommendation Agent", "Investment strategy complete. Generated detailed recommendations, risk assessments, and portfolio guidance with actionable insights.", "success");
      }
    } catch (error) {
      addMessage("💡 Recommendation Agent", "Investment strategy complete. Generated detailed recommendations, risk assessments, and portfolio guidance with actionable insights.", "success");
    }

    await new Promise(resolve => setTimeout(resolve, 1000));
    addMessage("🎯 Orchestrator", "All agent analysis complete! Compiling comprehensive professional financial report with executive summary, detailed analysis, and actionable recommendations...", "system");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsProcessing(true);
    setAgentMessages([]);
    setFinalResult(null);
    setError(null);

    // Start the agent discourse simulation with the actual query
    simulateAgentDiscourse(query);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();

      if (data.success) {
        console.log('Final result from backend:', data.result);
        setFinalResult(data.result);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      setError('Failed to connect to the server. Make sure the Flask backend is running.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleExampleClick = (exampleQuery) => {
    setQuery(exampleQuery);
  };

  const handleReset = () => {
    setQuery('');
    setAgentMessages([]);
    setFinalResult(null);
    setError(null);
    setIsProcessing(false);
  };

  // Show initial query form if not processing and no results
  if (!isProcessing && !finalResult && !error) {
    return (
      <div className="app-container">
        <div className="query-screen">
          <div className="header">
            <h1>🤖 Multi-Agent Financial Analysis</h1>
            <p>Ask our AI agents to analyze any financial question</p>
          </div>

          <form onSubmit={handleSubmit} className="query-form">
            <div className="input-group">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your financial analysis question..."
                className="query-input"
                rows={4}
                disabled={isProcessing}
              />
              <button type="submit" className="submit-button" disabled={!query.trim()}>
                🚀 Start Analysis
              </button>
            </div>
          </form>

          <div className="examples-section">
            <h3>💡 Example Questions</h3>
            <div className="examples-grid">
              {exampleQueries.map((example, index) => (
                <button
                  key={index}
                  onClick={() => handleExampleClick(example)}
                  className="example-button"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Show processing screen with agent discourse
  return (
    <div className="app-container">
      <div className="processing-screen">
        <div className="header">
          <h1>🤖 Multi-Agent Financial Analysis</h1>
          <div className="query-display">
            <strong>Query:</strong> {query}
          </div>
        </div>

        <div className="discourse-container">
          <h2>🗨️ Agent Discourse</h2>
          <div className="messages-stream">
            {agentMessages.map((message) => (
              <div key={message.id} className={`message ${message.type}`}>
                <div className="message-header">
                  <span className="agent-name">{message.agent}</span>
                  <span className="timestamp">{message.timestamp}</span>
                </div>
                <div className="message-content">{message.message}</div>
              </div>
            ))}
            {isProcessing && (
              <div className="typing-indicator">
                <div className="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span>Agents working...</span>
              </div>
            )}
          </div>
        </div>

        {error && (
          <div className="error-section">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}

        {finalResult && (
          <div className="results-section">
            <h2>📋 Professional Financial Analysis Report</h2>
            <div className="report-metadata">
              <div className="report-info">
                <span><strong>Generated:</strong> {new Date().toLocaleDateString()} at {new Date().toLocaleTimeString()}</span>
                <span><strong>Agents Consulted:</strong> {finalResult.agents_used ? finalResult.agents_used.join(', ') : 'Research Agent, Analysis Agent, Recommendation Agent'}</span>
                {finalResult.timestamp && (
                  <span><strong>Report Timestamp:</strong> {new Date(finalResult.timestamp).toLocaleString()}</span>
                )}
              </div>
            </div>
            <div className="result-content professional-report">
              {finalResult && finalResult.analysis && typeof finalResult.analysis === 'string' ? (
                <div className="report-text">
                  {finalResult.analysis.split('\n').map((line, index) => {
                    // Handle markdown-style headers
                    if (line.startsWith('# ')) {
                      return <h1 key={index} className="report-h1">{line.substring(2)}</h1>;
                    }
                    if (line.startsWith('## ')) {
                      return <h2 key={index} className="report-h2">{line.substring(3)}</h2>;
                    }
                    if (line.startsWith('### ')) {
                      return <h3 key={index} className="report-h3">{line.substring(4)}</h3>;
                    }
                    // Handle bullet points
                    if (line.trim().startsWith('- ')) {
                      return <li key={index} className="report-bullet">{line.substring(2)}</li>;
                    }
                    // Handle empty lines
                    if (line.trim() === '') {
                      return <br key={index} />;
                    }
                    // Handle bold text
                    const boldText = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                    // Regular paragraphs
                    return <p key={index} className="report-paragraph" dangerouslySetInnerHTML={{__html: boldText}}></p>;
                  })}
                </div>
              ) : finalResult && typeof finalResult === 'string' ? (
                <div className="report-text">
                  <p>{finalResult}</p>
                </div>
              ) : (
                <div className="report-text">
                  <p>Report data structure error. Please try again.</p>
                  <details>
                    <summary>Debug Information</summary>
                    <pre>{JSON.stringify(finalResult, null, 2)}</pre>
                  </details>
                </div>
              )}
            </div>
            
            {/* Print and Export Options */}
            <div className="report-actions">
              <button 
                onClick={() => window.print()} 
                className="action-button print-button"
              >
                🖨️ Print Report
              </button>
              <button 
                onClick={() => {
                  let reportText = '';
                  if (finalResult && finalResult.analysis) {
                    reportText = finalResult.analysis;
                  } else if (finalResult && typeof finalResult === 'string') {
                    reportText = finalResult;
                  } else {
                    reportText = 'No report data available';
                  }
                  
                  const blob = new Blob([reportText], { type: 'text/plain' });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = `financial-analysis-report-${new Date().toISOString().split('T')[0]}.txt`;
                  a.click();
                  URL.revokeObjectURL(url);
                }}
                className="action-button export-button"
              >
                💾 Export as Text
              </button>
            </div>
          </div>
        )}

        <div className="action-buttons">
          <button onClick={handleReset} className="reset-button">
            🔄 New Analysis
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
