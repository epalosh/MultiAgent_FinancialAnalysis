import React from 'react';

const LoadingSpinner = ({ message = 'Processing analysis...' }) => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <div className="loading-message">{message}</div>
    </div>
  );
};

export default LoadingSpinner;
