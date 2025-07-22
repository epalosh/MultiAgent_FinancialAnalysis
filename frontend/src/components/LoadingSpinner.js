import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="loading-container">
      <div className="modern-spinner">
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
        <div className="spinner-center">
          <span className="spinner-icon">🤖</span>
        </div>
      </div>
      <div className="loading-text">
        <span className="loading-title">AI Agents Processing</span>
        <span className="loading-subtitle">Advanced financial analysis in progress</span>
      </div>
    </div>
  );
};

export default LoadingSpinner;
