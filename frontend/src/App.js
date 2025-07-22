import React, { useState, useEffect } from 'react';
import './App.css';
import QueryForm from './components/QueryForm';
import AgentFlowChart from './components/AgentFlowChart';
import FinancialReport from './components/FinancialReport';
import LoadingSpinner from './components/LoadingSpinner';

const App = () => {
  const [analysisState, setAnalysisState] = useState({
    isRunning: false,
    currentStep: 0,
    query: '',
    steps: [],
    finalReport: null,
    error: null
  });

  const [selectedStep, setSelectedStep] = useState(null);

  const handleQuerySubmit = async (query) => {
    setAnalysisState({
      isRunning: true,
      currentStep: 0,
      query,
      steps: [],
      finalReport: null,
      error: null
    });

    try {
      // Initialize steps
      const initialSteps = [
        { 
          id: 'research',
          name: 'Research Agent',
          description: 'Gathering comprehensive company and market data',
          status: 'pending',
          output: null,
          startTime: null,
          endTime: null
        },
        {
          id: 'analysis',
          name: 'Analysis Agent', 
          description: 'Performing detailed financial analysis and calculations',
          status: 'pending',
          output: null,
          startTime: null,
          endTime: null
        },
        {
          id: 'recommendation',
          name: 'Recommendation Agent',
          description: 'Generating investment recommendations and strategies',
          status: 'pending', 
          output: null,
          startTime: null,
          endTime: null
        }
      ];

      setAnalysisState(prev => ({ ...prev, steps: initialSteps }));

      // Simulate step-by-step progress while running the full analysis
      await runFullAnalysisWithProgress(query);

    } catch (error) {
      setAnalysisState(prev => ({ 
        ...prev, 
        isRunning: false, 
        error: error.message 
      }));
    }
  };

  const runFullAnalysisWithProgress = async (query) => {
    // Start the full analysis
    const analysisPromise = fetch('/api/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    // Simulate progress through the steps
    const steps = ['research', 'analysis', 'recommendation'];
    const stepDurations = [3000, 4000, 3000]; // Simulated durations in ms

    for (let i = 0; i < steps.length; i++) {
      // Update step to running
      setAnalysisState(prev => ({
        ...prev,
        currentStep: i,
        steps: prev.steps.map((step, idx) => 
          idx === i 
            ? { ...step, status: 'running', startTime: new Date() }
            : step
        )
      }));

      // Wait for simulated duration
      await new Promise(resolve => setTimeout(resolve, stepDurations[i]));

      // Update step to completed
      setAnalysisState(prev => ({
        ...prev,
        steps: prev.steps.map((step, idx) => 
          idx === i 
            ? { 
                ...step, 
                status: 'completed', 
                output: `${step.name} completed successfully. Detailed output will be available in the final report.`,
                endTime: new Date()
              }
            : step
        )
      }));
    }

    // Show final report generation
    setAnalysisState(prev => ({
      ...prev,
      currentStep: steps.length
    }));

    try {
      const response = await analysisPromise;
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();

      if (result.success) {
        setAnalysisState(prev => ({
          ...prev,
          isRunning: false,
          finalReport: result.result
        }));
      } else {
        throw new Error(result.error || 'Analysis failed');
      }
    } catch (error) {
      throw error;
    }
  };

  const handleStepClick = (step) => {
    setSelectedStep(step);
  };

  const handleCloseModal = () => {
    setSelectedStep(null);
  };

  const resetAnalysis = () => {
    setAnalysisState({
      isRunning: false,
      currentStep: 0,
      query: '',
      steps: [],
      finalReport: null,
      error: null
    });
    setSelectedStep(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>Financial Analysis Research Platform</h1>
          <p>Multi-Agent Financial Intelligence System</p>
        </div>
      </header>

      <main className="app-main">
        {!analysisState.isRunning && !analysisState.finalReport && (
          <QueryForm onSubmit={handleQuerySubmit} />
        )}

        {(analysisState.isRunning || analysisState.steps.length > 0) && (
          <AgentFlowChart 
            steps={analysisState.steps}
            currentStep={analysisState.currentStep}
            isRunning={analysisState.isRunning}
            onStepClick={handleStepClick}
            query={analysisState.query}
          />
        )}

        {analysisState.isRunning && (
          <LoadingSpinner 
            message={
              analysisState.currentStep < analysisState.steps.length
                ? `${analysisState.steps[analysisState.currentStep]?.name} is processing...`
                : 'Compiling final financial report...'
            }
          />
        )}

        {analysisState.error && (
          <div className="error-container">
            <h3>Analysis Error</h3>
            <p>{analysisState.error}</p>
            <button onClick={resetAnalysis} className="btn btn-primary">
              Start New Analysis
            </button>
          </div>
        )}

        {analysisState.finalReport && (
          <FinancialReport 
            report={analysisState.finalReport}
            query={analysisState.query}
            steps={analysisState.steps}
            onNewAnalysis={resetAnalysis}
          />
        )}
      </main>

      {selectedStep && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{selectedStep.name}</h3>
              <button className="modal-close" onClick={handleCloseModal}>×</button>
            </div>
            <div className="modal-body">
              <div className="step-info">
                <p><strong>Description:</strong> {selectedStep.description}</p>
                <p><strong>Status:</strong> <span className={`status ${selectedStep.status}`}>{selectedStep.status}</span></p>
                {selectedStep.startTime && (
                  <p><strong>Started:</strong> {selectedStep.startTime.toLocaleTimeString()}</p>
                )}
                {selectedStep.endTime && (
                  <p><strong>Completed:</strong> {selectedStep.endTime.toLocaleTimeString()}</p>
                )}
              </div>
              {selectedStep.output && (
                <div className="step-output">
                  <h4>Agent Output:</h4>
                  <pre>{selectedStep.output}</pre>
                </div>
              )}
              {selectedStep.error && (
                <div className="step-error">
                  <h4>Error:</h4>
                  <p>{selectedStep.error}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
