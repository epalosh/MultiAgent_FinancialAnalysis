#!/usr/bin/env python3
"""
Demo script showcasing Enhanced Financial Analysis with Real Data
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.agents.financial_orchestrator import FinancialOrchestrator

def demo_enhanced_financial_analysis():
    """Demonstrate enhanced financial analysis capabilities"""
    
    print("🚀 Enhanced Financial Analysis System Demo")
    print("=" * 70)
    print("📊 Now using REAL market data from multiple sources:")
    print("   • Yahoo Finance APIs")
    print("   • Live stock prices & financial statements")
    print("   • Real-time risk calculations")
    print("   • Actual valuation metrics")
    print("=" * 70)
    
    # Initialize orchestrator
    orchestrator = FinancialOrchestrator()
    
    # Demo 1: Enhanced Research with Real Data
    print("\n🔍 DEMO 1: Enhanced Research with Real Market Data")
    print("-" * 50)
    
    try:
        print("Analyzing Apple Inc. (AAPL) with live data...")
        research_result = orchestrator.enhanced_research_agent.research_company("Apple (AAPL)")
        
        print("✅ Real data research completed!")
        print(f"📊 Generated {len(research_result)} characters of analysis")
        print("\n📋 Sample research output:")
        print(research_result[:800] + "...\n" if len(research_result) > 800 else research_result)
        
    except Exception as e:
        print(f"❌ Demo 1 failed: {str(e)}")
    
    # Demo 2: Quick Analysis
    print("\n🔍 DEMO 2: Quick Stock Analysis")
    print("-" * 50)
    
    try:
        print("Getting quick analysis for Microsoft (MSFT)...")
        quick_result = orchestrator.enhanced_research_agent.get_quick_analysis("MSFT")
        
        print("✅ Quick analysis completed!")
        print("\n📊 Quick Analysis Result:")
        print(quick_result)
        
    except Exception as e:
        print(f"❌ Demo 2 failed: {str(e)}")
    
    # Demo 3: Stock Comparison
    print("\n🔍 DEMO 3: Multi-Stock Comparison")
    print("-" * 50)
    
    try:
        print("Comparing AAPL vs MSFT vs GOOGL using real data...")
        comparison_result = orchestrator.enhanced_analysis_agent.compare_stocks(["AAPL", "MSFT", "GOOGL"])
        
        print("✅ Stock comparison completed!")
        print(f"📊 Generated {len(comparison_result)} characters of comparison")
        print("\n📋 Sample comparison output:")
        print(comparison_result[:600] + "...\n" if len(comparison_result) > 600 else comparison_result)
        
    except Exception as e:
        print(f"❌ Demo 3 failed: {str(e)}")
    
    # Demo 4: Full Enhanced Analysis
    print("\n🔍 DEMO 4: Complete Enhanced Financial Analysis")
    print("-" * 50)
    
    try:
        print("Running complete enhanced analysis for Tesla (TSLA)...")
        print("This includes:")
        print("  • Real-time data collection")
        print("  • Quantitative analysis with live metrics")
        print("  • Risk assessment using actual volatility")
        print("  • Investment scoring based on real fundamentals")
        
        enhanced_result = orchestrator.orchestrate_enhanced_analysis("Tesla (TSLA)")
        
        if enhanced_result.get('success'):
            print("✅ Enhanced analysis completed successfully!")
            print(f"📊 Total analysis: {enhanced_result.get('total_length', 0)} characters")
            print(f"🤖 Agents used: {', '.join(enhanced_result.get('agents_used', []))}")
            print(f"📈 Data sources: {', '.join(enhanced_result.get('data_sources', []))}")
            
            analysis = enhanced_result.get('analysis', '')
            print("\n📋 Enhanced Analysis Executive Summary:")
            # Extract just the executive summary
            lines = analysis.split('\n')
            summary_lines = []
            in_summary = False
            for line in lines:
                if 'EXECUTIVE SUMMARY' in line.upper():
                    in_summary = True
                elif in_summary and line.startswith('##') and 'EXECUTIVE' not in line.upper():
                    break
                elif in_summary:
                    summary_lines.append(line)
            
            summary = '\n'.join(summary_lines[:15])  # First 15 lines of summary
            print(summary if summary else analysis[:800] + "...")
            
        else:
            print(f"❌ Enhanced analysis failed: {enhanced_result.get('error')}")
        
    except Exception as e:
        print(f"❌ Demo 4 failed: {str(e)}")
    
    print("\n" + "=" * 70)
    print("🎉 Enhanced Financial Analysis Demo Complete!")
    print("✨ Key Improvements:")
    print("   • Uses REAL market data instead of placeholder values")
    print("   • Calculates actual financial ratios and risk metrics")
    print("   • Provides quantitative investment scores")
    print("   • Includes live price data and performance metrics")
    print("   • Performs real technical and fundamental analysis")
    print("=" * 70)

if __name__ == "__main__":
    demo_enhanced_financial_analysis()
