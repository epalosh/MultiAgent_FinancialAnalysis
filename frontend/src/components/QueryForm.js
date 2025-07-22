import React, { useState } from 'react';

const QueryForm = ({ onSubmit, disabled }) => {
  const [query, setQuery] = useState('');
  const [company, setCompany] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query.trim(), company.trim());
    }
  };

  const handleClear = () => {
    setQuery('');
    setCompany('');
  };

  // Example queries for user guidance
  const exampleQueries = [
    "Analyze the financial health and investment potential of Apple Inc.",
    "What are the key financial risks for Tesla in 2024?",
    "Compare the profitability ratios of Microsoft vs Google",
    "Should I invest in renewable energy stocks right now?",
    "Analyze the debt-to-equity ratio trends for banking sector"
  ];

  const handleExampleClick = (example) => {
    setQuery(example);
  };

  return (
    <form onSubmit={handleSubmit} className="query-form">
      <h2>🔍 Financial Analysis Query</h2>
      
      <div className="form-group">
        <label htmlFor="company">Company Name (Optional):</label>
        <input
          type="text"
          id="company"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder="e.g., Apple, TSLA, Microsoft..."
          className="form-input"
          disabled={disabled}
        />
      </div>

      <div className="form-group">
        <label htmlFor="query">Financial Analysis Query:</label>
        <textarea
          id="query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask me anything about financial analysis, company evaluation, investment recommendations..."
          className="form-textarea"
          required
          disabled={disabled}
        />
      </div>

      <div className="form-actions">
        <button 
          type="submit" 
          className="submit-button"
          disabled={disabled || !query.trim()}
        >
          {disabled ? '🤖 Analyzing...' : '🚀 Start Analysis'}
        </button>
        
        <button 
          type="button" 
          onClick={handleClear}
          className="clear-button"
          disabled={disabled}
          style={{
            background: 'transparent',
            color: '#667eea',
            border: '2px solid #667eea',
            marginLeft: '1rem',
            padding: '1rem 2rem',
            borderRadius: '6px',
            cursor: 'pointer',
            fontWeight: '600'
          }}
        >
          Clear
        </button>
      </div>

      <div className="example-queries">
        <h4>💡 Example Queries:</h4>
        <div className="examples-list">
          {exampleQueries.map((example, index) => (
            <button
              key={index}
              type="button"
              onClick={() => handleExampleClick(example)}
              disabled={disabled}
              className="example-button"
              style={{
                display: 'block',
                width: '100%',
                textAlign: 'left',
                background: 'white',
                border: '1px solid #ddd',
                padding: '0.5rem 1rem',
                margin: '0.25rem 0',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '0.9rem',
                transition: 'background-color 0.2s'
              }}
              onMouseEnter={(e) => e.target.style.backgroundColor = '#f5f7fa'}
              onMouseLeave={(e) => e.target.style.backgroundColor = 'white'}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </form>
  );
};

export default QueryForm;
