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
    {
      text: "Analyze the financial health and investment potential of Apple Inc.",
      company: "AAPL",
      category: "🍎 Company Analysis"
    },
    {
      text: "What are the key financial risks for Tesla in 2024?",
      company: "TSLA",
      category: "⚡ Risk Assessment"
    },
    {
      text: "Compare the profitability ratios of Microsoft vs Google",
      company: "MSFT vs GOOGL",
      category: "📊 Comparative Analysis"
    },
    {
      text: "Should I invest in renewable energy stocks right now?",
      company: "",
      category: "🌱 Sector Analysis"
    },
    {
      text: "Analyze the debt-to-equity ratio trends for banking sector",
      company: "",
      category: "🏦 Industry Metrics"
    }
  ];

  const handleExampleClick = (example) => {
    setQuery(example.text);
    setCompany(example.company);
  };

  return (
    <div className="query-form">
      <div className="form-header">
        <h2>
          <span className="form-icon">🎯</span>
          Financial Analysis Query
        </h2>
        <div className="form-subtitle">
          Ask our AI agents anything about financial analysis, investments, or market insights
        </div>
      </div>
      
      <form onSubmit={handleSubmit} className="query-form-content">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="company" className="form-label">
              <span className="label-icon">🏢</span>
              Company/Symbol
              <span className="label-optional">(Optional)</span>
            </label>
            <input
              type="text"
              id="company"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              placeholder="e.g., AAPL, Tesla, Microsoft..."
              className="form-input"
              disabled={disabled}
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="query" className="form-label">
            <span className="label-icon">💭</span>
            Your Financial Query
            <span className="label-required">*</span>
          </label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Describe what financial analysis or insights you need..."
            className="form-textarea"
            required
            disabled={disabled}
            rows={4}
          />
          <div className="textarea-counter">
            {query.length} characters
          </div>
        </div>

        <div className="form-actions">
          <button 
            type="submit" 
            className="submit-button primary"
            disabled={disabled || !query.trim()}
          >
            {disabled ? (
              <>
                <span className="button-spinner"></span>
                AI Agents Analyzing...
              </>
            ) : (
              <>
                <span className="button-icon">🚀</span>
                Start Analysis
              </>
            )}
          </button>
          
          <button 
            type="button" 
            onClick={handleClear}
            className="submit-button secondary"
            disabled={disabled}
          >
            <span className="button-icon">🗑️</span>
            Clear
          </button>
        </div>
      </form>

      <div className="example-queries">
        <h4 className="examples-title">
          <span className="examples-icon">💡</span>
          Quick Start Examples
        </h4>
        <div className="examples-grid">
          {exampleQueries.map((example, index) => (
            <button
              key={index}
              type="button"
              onClick={() => handleExampleClick(example)}
              disabled={disabled}
              className="example-button"
              title={`Click to use: ${example.text}`}
            >
              <div className="example-category">{example.category}</div>
              <div className="example-text">{example.text}</div>
              {example.company && (
                <div className="example-company">→ {example.company}</div>
              )}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default QueryForm;
