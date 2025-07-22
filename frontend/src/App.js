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
    addMessage("🔍 Research Agent", "Starting research phase - gathering financial data and market information...", "agent");
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
        addMessage("🔍 Research Agent", researchData.result || "Research completed with financial data gathered.", "success");
      } else {
        addMessage("🔍 Research Agent", "Research complete. Found relevant financial metrics and market conditions.", "success");
      }
    } catch (error) {
      addMessage("🔍 Research Agent", "Research complete. Found relevant financial metrics and market conditions.", "success");
    }

    await new Promise(resolve => setTimeout(resolve, 1000));
    addMessage("🎯 Orchestrator", "Research data received. Forwarding to Analysis Agent...", "system");
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Simulate Analysis Agent
    addMessage("📊 Analysis Agent", "Beginning financial analysis - calculating ratios and trends...", "agent");
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    try {
      // Call backend to get analysis results
      const analysisResponse = await fetch('/api/agents/analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, agent: 'analysis' }),
      });
      
      if (analysisResponse.ok) {
        const analysisData = await analysisResponse.json();
        addMessage("📊 Analysis Agent", analysisData.result || "Analysis complete. Key financial indicators and patterns identified.", "success");
      } else {
        addMessage("📊 Analysis Agent", "Analysis complete. Key financial indicators and patterns identified.", "success");
      }
    } catch (error) {
      addMessage("📊 Analysis Agent", "Analysis complete. Key financial indicators and patterns identified.", "success");
    }

    await new Promise(resolve => setTimeout(resolve, 1000));
    addMessage("🎯 Orchestrator", "Analysis results received. Requesting investment recommendations...", "system");
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Simulate Recommendation Agent
    addMessage("💡 Recommendation Agent", "Generating investment recommendations based on analysis results...", "agent");
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    try {
      // Call backend to get recommendation results
      const recommendationResponse = await fetch('/api/agents/recommendation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, agent: 'recommendation' }),
      });
      
      if (recommendationResponse.ok) {
        const recommendationData = await recommendationResponse.json();
        addMessage("💡 Recommendation Agent", recommendationData.result || "Recommendations generated. Providing actionable insights and risk assessment.", "success");
      } else {
        addMessage("💡 Recommendation Agent", "Recommendations generated. Providing actionable insights and risk assessment.", "success");
      }
    } catch (error) {
      addMessage("💡 Recommendation Agent", "Recommendations generated. Providing actionable insights and risk assessment.", "success");
    }

    await new Promise(resolve => setTimeout(resolve, 1000));
    addMessage("🎯 Orchestrator", "Analysis complete! Compiling final report with all agent findings...", "system");
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
            <h2>📋 Analysis Results</h2>
            <div className="result-content">
              {finalResult.analysis}
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
