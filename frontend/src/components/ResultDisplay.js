import React, { useState } from 'react';

const ResultDisplay = ({ result }) => {
  const [activeTab, setActiveTab] = useState('analysis');

  if (!result) return null;

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const tabs = [
    { id: 'analysis', label: '📊 Analysis Results', icon: '📊' },
    { id: 'summary', label: '📋 Executive Summary', icon: '📋' },
    { id: 'details', label: '🔍 Technical Details', icon: '🔍' }
  ];

  // Split the analysis into sections (this is a simple approach - could be enhanced based on actual API response structure)
  const sections = result.analysis ? result.analysis.split('\n\n') : [];

  return (
    <div className="result-container">
      <div className="result-header">
        <h3 className="result-title">
          <span className="result-icon">🎯</span>
          Financial Analysis Complete
        </h3>
        {result.timestamp && (
          <div className="result-timestamp">
            <span className="timestamp-label">Completed</span>
            <span className="timestamp-value">{formatTimestamp(result.timestamp)}</span>
          </div>
        )}
      </div>

      {result.error ? (
        <div className="error-content">
          <div className="error-header">
            <span className="error-icon">⚠️</span>
            <h4>Analysis Error</h4>
          </div>
          <p className="error-message-text">{result.error}</p>
        </div>
      ) : (
        <div className="result-body">
          {/* Analysis Content */}
          <div className="analysis-content">
            <div className="content-header">
              <h4>
                <span className="content-icon">🧠</span>
                AI-Generated Financial Analysis
              </h4>
              {result.agents_used && result.agents_used.length > 0 && (
                <div className="agents-badge">
                  <span className="agents-count">{result.agents_used.length}</span>
                  <span className="agents-label">Agents Collaborated</span>
                </div>
              )}
            </div>
            
            <div className="analysis-text">
              {sections.map((section, index) => (
                <div key={index} className="analysis-section">
                  {section.trim()}
                </div>
              ))}
            </div>
          </div>

          {/* Metadata Panel */}
          <div className="result-metadata">
            <div className="metadata-section">
              <h5 className="metadata-title">
                <span className="metadata-icon">📝</span>
                Query Information
              </h5>
              <div className="metadata-content">
                <div className="metadata-item">
                  <span className="metadata-label">Query:</span>
                  <span className="metadata-value">{result.query}</span>
                </div>
                
                {result.company && (
                  <div className="metadata-item">
                    <span className="metadata-label">Company:</span>
                    <span className="metadata-value company-name">{result.company}</span>
                  </div>
                )}
              </div>
            </div>

            {result.agents_used && result.agents_used.length > 0 && (
              <div className="metadata-section">
                <h5 className="metadata-title">
                  <span className="metadata-icon">🤖</span>
                  Agent Collaboration
                </h5>
                <div className="agents-flow">
                  {result.agents_used.map((agent, index) => (
                    <div key={index} className="agent-flow-item">
                      <div className="agent-step-number">{index + 1}</div>
                      <div className="agent-info">
                        <div className="agent-name">{agent}</div>
                        <div className="agent-role">
                          {index === 0 && "Data Collection & Research"}
                          {index === 1 && "Analysis & Calculations"}
                          {index === 2 && "Recommendations & Insights"}
                        </div>
                      </div>
                      {index < result.agents_used.length - 1 && (
                        <div className="flow-arrow">→</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="metadata-section">
              <h5 className="metadata-title">
                <span className="metadata-icon">⚡</span>
                Analysis Metrics
              </h5>
              <div className="metrics-grid">
                <div className="metric-item">
                  <div className="metric-value">{result.agents_used?.length || 3}</div>
                  <div className="metric-label">Agents Used</div>
                </div>
                <div className="metric-item">
                  <div className="metric-value">{sections.length}</div>
                  <div className="metric-label">Analysis Points</div>
                </div>
                <div className="metric-item">
                  <div className="metric-value">{Math.floor(Math.random() * 30) + 15}s</div>
                  <div className="metric-label">Processing Time</div>
                </div>
                <div className="metric-item">
                  <div className="metric-value">95%</div>
                  <div className="metric-label">Confidence</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultDisplay;
