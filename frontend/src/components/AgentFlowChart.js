import React from 'react';

const AgentFlowChart = ({ steps, currentStep, isRunning, onStepClick, query }) => {
  const getStepIcon = (step) => {
    switch (step.status) {
      case 'completed':
        return '✓';
      case 'running':
        return '⟳';
      case 'error':
        return '✗';
      default:
        return step.id === 'research' ? '1' : step.id === 'analysis' ? '2' : '3';
    }
  };

  const formatDuration = (startTime, endTime) => {
    if (!startTime) return null;
    if (!endTime) return 'Running...';
    
    const duration = Math.round((endTime - startTime) / 1000);
    return `${duration}s`;
  };

  return (
    <div className="agent-flowchart">
      <div className="flowchart-header">
        <div className="query-display">
          <strong>Query:</strong> {query}
        </div>
      </div>

      <div className="flow-steps">
        {steps.map((step, index) => (
          <div 
            key={step.id}
            className={`flow-step ${step.status}`}
            onClick={() => onStepClick(step)}
          >
            <div className={`step-card ${step.status}`}>
              <div className={`step-icon ${step.status}`}>
                {getStepIcon(step)}
              </div>
              <div className="step-title">{step.name}</div>
              <div className="step-description">{step.description}</div>
              {(step.startTime || step.endTime) && (
                <div className="step-timing">
                  {formatDuration(step.startTime, step.endTime)}
                </div>
              )}
              {step.status === 'error' && (
                <div className="step-error-indicator">Error occurred</div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="process-status">
        {isRunning ? (
          <p>Analysis in progress... Click on any step to view details.</p>
        ) : (
          <p>Analysis complete. Click on any step to review the detailed output.</p>
        )}
      </div>
    </div>
  );
};

export default AgentFlowChart;
