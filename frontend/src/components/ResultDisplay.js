import React from 'react';

const ResultDisplay = ({ result }) => {
  if (!result) return null;

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="result-container">
      <div className="result-header">
        <h3 className="result-title">📊 Analysis Results</h3>
        {result.timestamp && (
          <span className="result-timestamp">
            {formatTimestamp(result.timestamp)}
          </span>
        )}
      </div>

      {result.error ? (
        <div className="error-content">
          <h4 style={{ color: '#e74c3c', marginBottom: '1rem' }}>❌ Analysis Error</h4>
          <p style={{ color: '#c0392b' }}>{result.error}</p>
        </div>
      ) : (
        <div>
          <div className="result-content">
            {result.analysis}
          </div>

          <div className="result-meta">
            <div className="meta-item">
              <span className="meta-label">Query:</span> {result.query}
            </div>
            
            {result.company && (
              <div className="meta-item">
                <span className="meta-label">Company:</span> {result.company}
              </div>
            )}
            
            {result.agents_used && result.agents_used.length > 0 && (
              <div className="meta-item">
                <span className="meta-label">Agents Used:</span>
                <div className="agents-used">
                  {result.agents_used.map((agent, index) => (
                    <span key={index} className="agent-tag">
                      {agent}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultDisplay;
