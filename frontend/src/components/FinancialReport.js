import React, { useState } from 'react';

const FinancialReport = ({ report, query, steps, onNewAnalysis }) => {
  const [showTraceSteps, setShowTraceSteps] = useState(false);

  const handleStepTrace = (step) => {
    // This could open a modal or expand details
    console.log('Tracing step:', step);
  };

  const getCurrentTimestamp = () => {
    return new Date().toLocaleString();
  };

  const getCompletedSteps = () => {
    return steps.filter(step => step.status === 'completed');
  };

  // Format text with markdown-like formatting
  const formatText = (text) => {
    if (!text || typeof text !== 'string') return text;

    // Convert markdown-style formatting to HTML
    let formatted = text
      // Headers
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      // Bold text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/__(.*?)__/g, '<strong>$1</strong>')
      // Italic text
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/_(.*?)_/g, '<em>$1</em>')
      // Line breaks
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br/>');

    // Wrap in paragraphs if not already wrapped
    if (!formatted.includes('<h') && !formatted.includes('<p>')) {
      formatted = '<p>' + formatted + '</p>';
    }

    return formatted;
  };

  // Component to render formatted text
  const FormattedText = ({ children }) => {
    if (typeof children !== 'string') {
      return <pre>{JSON.stringify(children, null, 2)}</pre>;
    }

    const formattedText = formatText(children);
    return (
      <div 
        className="formatted-content"
        dangerouslySetInnerHTML={{ __html: formattedText }}
      />
    );
  };

  // Handle both string and object report formats
  const renderReport = () => {
    if (typeof report === 'string') {
      return <FormattedText>{report}</FormattedText>;
    }
    
    if (typeof report === 'object' && report !== null) {
      // Handle structured report object
      return (
        <div className="structured-report">
          {report.company && (
            <div className="report-section">
              <h3>Company Analysis</h3>
              <p><strong>Company:</strong> {report.company}</p>
            </div>
          )}
          
          {report.analysis && (
            <div className="report-section">
              <h3>Financial Analysis</h3>
              <FormattedText>
                {typeof report.analysis === 'string' ? report.analysis : JSON.stringify(report.analysis, null, 2)}
              </FormattedText>
            </div>
          )}
          
          {report.report_sections && (
            <div className="report-section">
              <h3>Detailed Report Sections</h3>
              {Array.isArray(report.report_sections) ? (
                report.report_sections.map((section, index) => (
                  <div key={index} className="report-subsection">
                    <FormattedText>
                      {typeof section === 'string' ? section : JSON.stringify(section, null, 2)}
                    </FormattedText>
                  </div>
                ))
              ) : (
                <FormattedText>
                  {typeof report.report_sections === 'string' ? report.report_sections : JSON.stringify(report.report_sections, null, 2)}
                </FormattedText>
              )}
            </div>
          )}
          
          {report.agents_used && (
            <div className="report-section">
              <h3>Agents Utilized</h3>
              {Array.isArray(report.agents_used) ? (
                <ul>
                  {report.agents_used.map((agent, index) => (
                    <li key={index}>{agent}</li>
                  ))}
                </ul>
              ) : (
                <p>{report.agents_used}</p>
              )}
            </div>
          )}
          
          {report.timestamp && (
            <div className="report-section">
              <h4>Report Generated</h4>
              <p>{report.timestamp}</p>
            </div>
          )}
        </div>
      );
    }
    
    // Fallback for any other data type
    return <pre>{JSON.stringify(report, null, 2)}</pre>;
  };

  return (
    <div className="financial-report">
      <div className="report-header">
        <h2>Financial Analysis Report</h2>
        <div className="report-metadata">
          <div>
            <strong>Generated:</strong> {getCurrentTimestamp()}
          </div>
          <div>
            <strong>Query:</strong> {query}
          </div>
          <div>
            <strong>Processing Time:</strong> {getCompletedSteps().length} agents completed
          </div>
        </div>
      </div>

      <div className="report-content">
        {renderReport()}
      </div>

      <div className="trace-steps">
        <h4>Analysis Process Trace</h4>
        <p>Click on any step below to review the detailed reasoning:</p>
        {getCompletedSteps().map((step, index) => (
          <div 
            key={step.id}
            className="trace-step"
            onClick={() => handleStepTrace(step)}
          >
            <div className="trace-step-icon completed">
              {index + 1}
            </div>
            <div className="trace-step-text">
              <strong>{step.name}:</strong> {step.description}
              {step.startTime && step.endTime && (
                <span className="trace-timing">
                  ({Math.round((step.endTime - step.startTime) / 1000)}s)
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="report-actions">
        <button onClick={onNewAnalysis} className="btn btn-primary">
          Start New Analysis
        </button>
        <button 
          onClick={() => setShowTraceSteps(!showTraceSteps)} 
          className="btn btn-secondary"
        >
          {showTraceSteps ? 'Hide' : 'Show'} Detailed Trace
        </button>
      </div>

      {showTraceSteps && (
        <div className="detailed-trace">
          <h4>Detailed Agent Outputs</h4>
          {getCompletedSteps().map((step, index) => (
            <div key={step.id} className="trace-detail">
              <h5>{step.name} Output</h5>
              <div className="trace-output">
                <pre>{step.output}</pre>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FinancialReport;
