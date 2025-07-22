import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <div className="loading-text">
        🤖 Multi-agents are analyzing your request...
      </div>
      <div style={{ 
        marginTop: '1rem', 
        fontSize: '0.9rem', 
        color: '#7f8c8d',
        fontStyle: 'italic'
      }}>
        This may take a few moments while our agents collaborate
      </div>
    </div>
  );
};

export default LoadingSpinner;
