import React from 'react';

const AgentStatus = ({ agents }) => {
  const agentIcons = {
    'Research Agent': '🔍',
    'Analysis Agent': '📊',
    'Recommendation Agent': '💡',
    'Financial Orchestrator': '🎯'
  };

  const agentColors = {
    'Research Agent': '#3b82f6',
    'Analysis Agent': '#8b5cf6',
    'Recommendation Agent': '#10b981',
    'Financial Orchestrator': '#f59e0b'
  };

  return (
    <div className="agent-network">
      {agents.length === 0 ? (
        <div className="loading-agents">
          <div className="loading-dots">
            <div className="loading-dot"></div>
            <div className="loading-dot"></div>
            <div className="loading-dot"></div>
          </div>
          <p>Initializing AI Agents...</p>
        </div>
      ) : (
        <>
          <div className="network-status">
            <div className="status-indicator online">
              <div className="status-pulse"></div>
            </div>
            <div className="status-text">
              <div className="status-title">Network Online</div>
              <div className="status-subtitle">{agents.length} Agents Ready</div>
            </div>
          </div>

          <div className="agents-list">
            {agents.map((agent, index) => (
              <div key={index} className="agent-card">
                <div className="agent-header">
                  <div 
                    className="agent-avatar"
                    style={{ backgroundColor: agentColors[agent.name] || '#6b7280' }}
                  >
                    <span className="agent-icon">
                      {agentIcons[agent.name] || '🤖'}
                    </span>
                  </div>
                  <div className="agent-info">
                    <div className="agent-name">{agent.name}</div>
                    <div className="agent-status">Ready</div>
                  </div>
                </div>
                
                <div className="agent-description">{agent.description}</div>
                
                {agent.capabilities && agent.capabilities.length > 0 && (
                  <div className="agent-capabilities">
                    <h6 className="capabilities-title">Core Functions:</h6>
                    <div className="capabilities-tags">
                      {agent.capabilities.map((capability, capIndex) => (
                        <span key={capIndex} className="capability-tag">
                          {capability}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="network-info">
            <div className="info-card">
              <h6 className="info-title">
                <span className="info-icon">⚡</span>
                How It Works
              </h6>
              <div className="workflow-steps">
                <div className="workflow-step">
                  <div className="step-number">1</div>
                  <div className="step-text">Research Agent collects data</div>
                </div>
                <div className="workflow-step">
                  <div className="step-number">2</div>
                  <div className="step-text">Analysis Agent processes information</div>
                </div>
                <div className="workflow-step">
                  <div className="step-number">3</div>
                  <div className="step-text">Recommendation Agent provides insights</div>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default AgentStatus;
