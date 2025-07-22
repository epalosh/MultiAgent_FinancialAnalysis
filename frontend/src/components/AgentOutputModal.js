import React from 'react';

const AgentOutputModal = ({ step, isOpen, onClose }) => {
  if (!isOpen || !step) return null;

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
      // Tables (basic support)
      .replace(/\|(.+)\|/g, (match, content) => {
        const cells = content.split('|').map(cell => cell.trim());
        return '<tr>' + cells.map(cell => `<td>${cell}</td>`).join('') + '</tr>';
      })
      // Line breaks
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br/>');

    // Wrap in paragraphs if not already wrapped
    if (!formatted.includes('<h') && !formatted.includes('<p>') && !formatted.includes('<table>')) {
      formatted = '<p>' + formatted + '</p>';
    }

    return formatted;
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return '#28a745';
      case 'running': return '#007bff';
      case 'failed': return '#dc3545';
      default: return '#6c757d';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return '✅';
      case 'running': return '🔄';
      case 'failed': return '❌';
      default: return '⏳';
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <span className="agent-icon" style={{ color: getStatusColor(step.status) }}>
              {getStatusIcon(step.status)}
            </span>
            <h2>{step.name} - Full Output</h2>
          </div>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        
        <div className="modal-body">
          <div className="agent-meta">
            <div className="meta-item">
              <strong>Status:</strong> 
              <span className={`status-badge ${step.status}`} style={{ color: getStatusColor(step.status) }}>
                {step.status.charAt(0).toUpperCase() + step.status.slice(1)}
              </span>
            </div>
            {step.startTime && (
              <div className="meta-item">
                <strong>Started:</strong> {step.startTime.toLocaleTimeString()}
              </div>
            )}
            {step.endTime && (
              <div className="meta-item">
                <strong>Completed:</strong> {step.endTime.toLocaleTimeString()}
              </div>
            )}
            {step.outputLength && (
              <div className="meta-item">
                <strong>Output Length:</strong> {step.outputLength.toLocaleString()} characters
              </div>
            )}
          </div>

          <div className="output-container">
            {step.output ? (
              <div 
                className="formatted-output"
                dangerouslySetInnerHTML={{ __html: formatText(step.output) }}
              />
            ) : (
              <div className="no-output">
                <p>No output available for this step yet.</p>
                {step.status === 'running' && <p>Agent is currently processing...</p>}
                {step.status === 'failed' && <p>Agent encountered an error during processing.</p>}
              </div>
            )}
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn btn-primary" onClick={onClose}>Close</button>
          {step.output && (
            <button 
              className="btn btn-secondary"
              onClick={() => {
                navigator.clipboard.writeText(step.output);
                alert('Output copied to clipboard!');
              }}
            >
              Copy Output
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default AgentOutputModal;
