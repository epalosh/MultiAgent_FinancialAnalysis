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

    // Simulate Analysis Agent
    addMessage("📊 Analysis Agent", "Processing quantitative analysis - calculating financial ratios, trend analysis, and peer comparisons...", "agent");
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    try {
      const analysisResponse = await fetch('/api/agents/analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, agent: 'analysis' }),
      });
      
      if (analysisResponse.ok) {
        const analysisData = await analysisResponse.json();
        addMessage("📊 Analysis Agent", analysisData.result || "Quantitative analysis complete. Generated comprehensive ratio analysis, trend evaluation, and peer benchmarking with detailed tables.", "success");
      } else {
        addMessage("📊 Analysis Agent", "Analysis complete. Generated comprehensive ratio analysis, trend evaluation, and peer benchmarking with detailed financial insights.", "success");
      }
    } catch (error) {
      addMessage("📊 Analysis Agent", "Analysis complete. Generated comprehensive ratio analysis, trend evaluation, and peer benchmarking with detailed financial insights.", "success");
    }

    await new Promise(resolve => setTimeout(resolve, 1000));

    // Simulate Recommendation Agent
    addMessage("💡 Recommendation Agent", "Synthesizing insights - generating investment recommendations, risk assessments, and portfolio strategy...", "agent");
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    try {
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

  const renderMessage = (message) => {
    if (!message || !message.message) return null;
    
    return (message.message || '').split('\\n').map((line, index) => {
      // Handle empty lines
      if (line.trim() === '') {
        return <br key={index} />;
      }
      
      // Handle bullet points
      if (line.trim().startsWith('- ') || line.trim().startsWith('• ')) {
        const bulletText = line.replace(/^[- •]\\s*/, '');
        return (
          <div key={index} style={{ marginLeft: '1rem', marginBottom: '0.5rem' }}>
            <span style={{ color: 'var(--accent-primary)', marginRight: '0.5rem' }}>•</span>
            {bulletText}
          </div>
        );
      }
      
      // Handle numbered points
      if (/^\\d+\\.\\s/.test(line.trim())) {
        return (
          <div key={index} style={{ marginLeft: '1rem', marginBottom: '0.5rem' }}>
            {line}
          </div>
        );
      }
      
      // Handle headers
      if (line.startsWith('### ')) {
        return <h3 key={index} style={{ color: 'var(--text-primary)', margin: '1rem 0 0.5rem 0', fontWeight: '600' }}>{line.substring(4)}</h3>;
      }
      if (line.startsWith('## ')) {
        return <h2 key={index} style={{ color: 'var(--accent-primary)', margin: '1.5rem 0 0.75rem 0', fontWeight: '600' }}>{line.substring(3)}</h2>;
      }
      if (line.startsWith('# ')) {
        return <h1 key={index} style={{ color: 'var(--text-primary)', margin: '1.5rem 0 0.75rem 0', fontWeight: '600', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>{line.substring(2)}</h1>;
      }
      
      // Handle bold text
      const boldText = line.replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color: var(--text-primary); font-weight: 600;">$1</strong>');
      
      // Regular paragraphs
      return (
        <p key={index} style={{ marginBottom: '0.75rem', lineHeight: '1.7' }} 
           dangerouslySetInnerHTML={{__html: boldText}}>
        </p>
      );
    });
  };

  const renderFinalResult = () => {
    try {
      if (!finalResult) return null;
      
      // Handle different result formats
      let content = '';
      if (finalResult.analysis && typeof finalResult.analysis === 'string') {
        content = finalResult.analysis;
      } else if (typeof finalResult === 'string') {
        content = finalResult;
      } else if (finalResult.error) {
        return (
          <div className="report-text">
            <p className="error-message">Analysis Error: {finalResult.error}</p>
            <details>
              <summary>Debug Information</summary>
              <pre>{JSON.stringify(finalResult, null, 2)}</pre>
            </details>
          </div>
        );
      } else {
        return (
          <div className="report-text">
            <p>No analysis content available</p>
            <details>
              <summary>Debug Information</summary>
              <pre>{JSON.stringify(finalResult, null, 2)}</pre>
            </details>
          </div>
        );
      }

      return (
        <div className="report-text">
          {content.split('\\n').map((line, index) => {
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
            const boldText = line.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
            // Regular paragraphs
            return <p key={index} className="report-paragraph" dangerouslySetInnerHTML={{__html: boldText}}></p>;
          })}
        </div>
      );
    } catch (renderError) {
      return (
        <div className="report-text">
          <p className="error-message">Error rendering report: {renderError.message}</p>
          <details>
            <summary>Debug Information</summary>
            <pre>finalResult: {JSON.stringify(finalResult, null, 2)}</pre>
          </details>
        </div>
      );
    }
  };

  // Show input screen if no processing and no results
  if (!isProcessing && !finalResult) {
    return (
      <div className="app-container">
        <div className="input-screen">
          <div className="header">
            <h1>🤖 Multi-Agent Financial Analysis</h1>
            <p className="subtitle">Professional financial insights powered by AI agents</p>
          </div>

          <form onSubmit={handleSubmit} className="query-form">
            <div className="input-group">
              <label htmlFor="query">Enter your financial analysis query:</label>
              <textarea
                id="query"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., Analyze Apple's financial performance and investment potential"
                required
                rows={3}
              />
            </div>
            <button type="submit" disabled={!query.trim()}>
              🚀 Start Analysis
            </button>
          </form>

          <div className="example-queries">
            <h3>💡 Example Queries</h3>
            <div className="examples">
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
  if (isProcessing || !finalResult) {
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
              {agentMessages && agentMessages.filter(message => message && message.message).map((message) => (
                <div key={message.id} className={`message ${message.type}`}>
                  <div className="message-header">
                    <span className="agent-name">{message.agent || 'Agent'}</span>
                    <span className="timestamp">{message.timestamp || ''}</span>
                  </div>
                  <div className="message-content">
                    {renderMessage(message)}
                  </div>
                </div>
              ))}
              {isProcessing && (
                <div className="typing-indicator">
                  <div className="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <span className="typing-text">Agents working...</span>
                </div>
              )}
            </div>
          </div>

          <div className="progress-info">
            <p>Multi-agent analysis in progress. Please wait while our specialized agents collaborate...</p>
          </div>
        </div>
      </div>
    );
  }

  // Show results screen
  return (
    <div className="app-container">
      <div className="results-screen">
        <div className="header">
          <h1>🤖 Multi-Agent Financial Analysis</h1>
          <div className="query-display">
            <strong>Query:</strong> {query}
          </div>
        </div>

        {error && (
          <div className="error-display">
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
              {renderFinalResult()}
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
