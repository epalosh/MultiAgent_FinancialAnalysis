import React, { useState } from 'react';

const QueryForm = ({ onSubmit }) => {
  const [query, setQuery] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const exampleQueries = [
    'Give a comprehensive data-driven report on Microsoft (MSFT) stock.',
    'Provide key indicators for Tesla (TSLA) and its performance for the rest of the year'
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
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="query">Analysis Request</label>
          <textarea
            id="query"
            className="form-input form-textarea"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your financial analysis query here... (e.g., 'Analyze any publicly traded stock: AAPL, TSLA, MSFT, GME, etc.')"
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
