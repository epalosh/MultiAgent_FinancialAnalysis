import React, { useState, useEffect } from 'react';
import './App.css';
import QueryForm from './components/QueryForm';
import ResultDisplay from './components/ResultDisplay';
import AgentStatus from './components/AgentStatus';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [agents, setAgents] = useState([]);
  const [error, setError] = useState(null);

  // Fetch agents information on component mount
  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await fetch('/api/agents');
      if (response.ok) {
        const data = await response.json();
        setAgents(data.agents || []);
      }
    } catch (err) {
      console.error('Failed to fetch agents:', err);
    }
  };

  const handleAnalysis = async (query, company) => {
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, company }),
      });

      const data = await response.json();

      if (data.success) {
        setAnalysisResult(data.result);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      setError('Failed to connect to the server. Make sure the Flask backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 Multi-Agent Financial Analysis System</h1>
        <p>Powered by LangChain Multi-Agent Orchestration</p>
      </header>

      <main className="App-main">
        <div className="content-container">
          {/* Left sidebar with agent status */}
          <aside className="sidebar">
            <AgentStatus agents={agents} />
          </aside>

          {/* Main content area */}
          <section className="main-content">
            <QueryForm onSubmit={handleAnalysis} disabled={isLoading} />
            
            {isLoading && <LoadingSpinner />}
            
            {error && (
              <div className="error-message">
                <h3>❌ Error</h3>
                <p>{error}</p>
              </div>
            )}
            
            {analysisResult && <ResultDisplay result={analysisResult} />}
          </section>
        </div>
      </main>

      <footer className="App-footer">
        <p>Multi-Agent Financial Analysis System - Built with React, Flask, and LangChain</p>
      </footer>
    </div>
  );
}

export default App;
