import React, { useState } from 'react';

const QueryForm = ({ onSubmit }) => {
  const [query, setQuery] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const exampleQueries = [
    'Analyze Apple Inc. (AAPL) financial performance and investment potential',
    'Perform comprehensive analysis of Tesla Inc. (TSLA) including risks and opportunities',
    'Evaluate Microsoft Corporation (MSFT) quarterly earnings and market position',
    'Research Amazon.com Inc. (AMZN) competitive advantages and growth prospects',
    'Analyze the financial health and investment outlook for Google (GOOGL)',
    'Assess the investment potential of Nvidia Corporation (NVDA) in the AI market'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || isSubmitting) return;

    setIsSubmitting(true);
    try {
      await onSubmit(query.trim());
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleExampleClick = (exampleQuery) => {
    setQuery(exampleQuery);
  };

  return (
    <div className="query-form">
      <h2>Financial Analysis Query</h2>
      <p>Enter a company name or financial analysis request to begin the multi-agent research process.</p>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="query">Analysis Request</label>
          <textarea
            id="query"
            className="form-input form-textarea"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your financial analysis query here... (e.g., 'Analyze Apple Inc. financial performance and investment potential')"
            required
            disabled={isSubmitting}
          />
        </div>

        <div className="example-queries">
          <h4>Example Queries:</h4>
          <ul className="example-list">
            {exampleQueries.map((example, index) => (
              <li 
                key={index}
                className="example-item"
                onClick={() => handleExampleClick(example)}
                title="Click to use this example"
              >
                {example}
              </li>
            ))}
          </ul>
        </div>

        <div className="form-group">
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={!query.trim() || isSubmitting}
          >
            {isSubmitting ? 'Starting Analysis...' : 'Begin Financial Analysis'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default QueryForm;
