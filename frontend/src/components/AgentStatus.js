import React from 'react';

const AgentStatus = ({ agents }) => {
  return (
    <div className="agent-status">
      <h3>🤖 Available Agents</h3>
      
      {agents.length === 0 ? (
        <div style={{ 
          textAlign: 'center', 
          color: '#7f8c8d', 
          padding: '2rem',
          fontStyle: 'italic'
        }}>
          Loading agents...
        </div>
      ) : (
        <ul className="agent-list">
          {agents.map((agent, index) => (
            <li key={index} className="agent-item">
              <div className="agent-name">{agent.name}</div>
              <div className="agent-description">{agent.description}</div>
              
              {agent.capabilities && agent.capabilities.length > 0 && (
                <div className="agent-capabilities">
                  <h5>Capabilities:</h5>
                  <div className="capabilities-list">
                    {agent.capabilities.map((capability, capIndex) => (
                      <span key={capIndex} className="capability-tag">
                        {capability}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
      
      <div style={{ 
        marginTop: '2rem', 
        padding: '1rem', 
        background: '#f8f9fc', 
        borderRadius: '6px',
        fontSize: '0.9rem',
        color: '#5a6c7d'
      }}>
        <h4 style={{ marginBottom: '0.5rem', color: '#2c3e50' }}>How it works:</h4>
        <ol style={{ paddingLeft: '1.2rem', lineHeight: '1.5' }}>
          <li>Research Agent gathers financial data</li>
          <li>Analysis Agent performs calculations</li>
          <li>Recommendation Agent provides insights</li>
          <li>Orchestrator coordinates the workflow</li>
        </ol>
      </div>
    </div>
  );
};

export default AgentStatus;
