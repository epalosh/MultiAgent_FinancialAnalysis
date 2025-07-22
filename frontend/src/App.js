import React, { useState, useEffect } from 'react';
import './App.css';
import QueryForm from './components/QueryForm';
import AgentFlowChart from './components/AgentFlowChart';
import FinancialReport from './components/FinancialReport';
import LoadingSpinner from './components/LoadingSpinner';
import AgentOutputModal from './components/AgentOutputModal';

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
  const [showModal, setShowModal] = useState(false);

  // Format text with markdown-like formatting for modal display
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
    const agentEndpoints = [
      { id: 'research', endpoint: '/api/agents/research', name: 'Research Agent' },
      { id: 'analysis', endpoint: '/api/agents/analysis', name: 'Analysis Agent' },
      { id: 'recommendation', endpoint: '/api/agents/recommendation', name: 'Recommendation Agent' }
    ];

    let cumulativeContext = '';
    const agentOutputs = {};

    for (let i = 0; i < agentEndpoints.length; i++) {
      const agent = agentEndpoints[i];
      
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

      try {
        // Call the specific agent endpoint
        const response = await fetch(agent.endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            query: query,
            context: cumulativeContext 
          }),
        });

        if (!response.ok) {
          throw new Error(`Agent ${agent.name} failed: ${response.status}`);
        }

        const result = await response.json();

        if (result.success) {
          // Store the full agent output
          agentOutputs[agent.id] = result.result;
          cumulativeContext += `\n\n=== ${agent.name} Output ===\n${result.result}`;

          // Update step to completed with full output
          setAnalysisState(prev => ({
            ...prev,
            steps: prev.steps.map((step, idx) => 
              idx === i 
                ? { 
                    ...step, 
                    status: 'completed', 
                    output: result.result,  // Store the FULL agent output
                    endTime: new Date(),
                    outputLength: result.output_length || result.result.length
                  }
                : step
            )
          }));
        } else {
          throw new Error(result.error || `${agent.name} failed`);
        }

      } catch (error) {
        // Update step to failed
        setAnalysisState(prev => ({
          ...prev,
          steps: prev.steps.map((step, idx) => 
            idx === i 
              ? { 
                  ...step, 
                  status: 'failed', 
                  output: `Error: ${error.message}`,
                  endTime: new Date()
                }
              : step
          )
        }));
        throw error;
      }
    }

    // Generate final comprehensive report by calling the orchestrator
    setAnalysisState(prev => ({
      ...prev,
      currentStep: agentEndpoints.length
    }));

    try {
      // Generate comprehensive integrated report
      const reportResponse = await fetch('/api/generate-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query: query,
          research: agentOutputs.research,
          analysis: agentOutputs.analysis,
          recommendations: agentOutputs.recommendation
        }),
      });
      
      if (!reportResponse.ok) {
        throw new Error(`Report generation failed: ${reportResponse.status}`);
      }

      const reportResult = await reportResponse.json();

      if (reportResult.success) {
        setAnalysisState(prev => ({
          ...prev,
          isRunning: false,
          finalReport: reportResult.comprehensive_report,
          agentOutputs: agentOutputs  // Store all individual agent outputs
        }));
      } else {
        // Fallback to simple combination if comprehensive report fails
        const fallbackReport = `
# COMPREHENSIVE FINANCIAL ANALYSIS REPORT

## EXECUTIVE SUMMARY
This report synthesizes outputs from our multi-agent financial analysis system.

---

## RESEARCH FINDINGS
${agentOutputs.research || 'Research data not available'}

---

## FINANCIAL ANALYSIS  
${agentOutputs.analysis || 'Analysis data not available'}

---

## INVESTMENT RECOMMENDATIONS
${agentOutputs.recommendation || 'Recommendations not available'}

---
**Report Generated:** ${new Date().toLocaleString()}
        `;
        
        setAnalysisState(prev => ({
          ...prev,
          isRunning: false,
          finalReport: fallbackReport,
          agentOutputs: agentOutputs
        }));
      }
    } catch (error) {
      console.error('Report generation error:', error);
      // Fallback to simple combination if there's an error
      const fallbackReport = `
# COMPREHENSIVE FINANCIAL ANALYSIS REPORT

## EXECUTIVE SUMMARY
This report synthesizes outputs from our multi-agent financial analysis system.

---

## RESEARCH FINDINGS
${agentOutputs.research || 'Research data not available'}

---

## FINANCIAL ANALYSIS
${agentOutputs.analysis || 'Analysis data not available'}

---

## INVESTMENT RECOMMENDATIONS
${agentOutputs.recommendation || 'Recommendations not available'}

---
**Report Generated:** ${new Date().toLocaleString()}
**Note:** Comprehensive report generation encountered an issue, displaying individual agent outputs.
      `;
      
      setAnalysisState(prev => ({
        ...prev,
        isRunning: false,
        finalReport: fallbackReport,
        agentOutputs: agentOutputs
      }));
    }
  };

  const handleStepClick = (step) => {
    setSelectedStep(step);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
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
    setShowModal(false);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>Multi-Agent Financial Analysis Research Platform</h1>
          <p>Built on LangChain, with yFinance integration for real data.</p>
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

      <AgentOutputModal 
        step={selectedStep}
        isOpen={showModal}
        onClose={handleCloseModal}
      />
    </div>
  );
};

export default App;
