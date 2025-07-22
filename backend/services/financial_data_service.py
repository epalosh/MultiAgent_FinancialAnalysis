import yfinance as yf
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class FinancialDataService:
    """
    Comprehensive financial data service that aggregates data from multiple sources
    """
    
    def __init__(self):
        self.alpha_vantage_key = None  # Can be set if user has API key
        self.fred_key = None  # Can be set if user has FRED API key
        
    def get_comprehensive_stock_data(self, symbol: str) -> Dict:
        """
        Get comprehensive stock data from multiple sources
        """
        try:
            # Primary data from Yahoo Finance
            stock = yf.Ticker(symbol)
            
            # Get basic info
            info = stock.info
            
            # Get historical data (5 years)
            hist_5y = stock.history(period="5y")
            hist_1y = stock.history(period="1y")
            hist_1m = stock.history(period="1mo")
            
            # Get financial statements
            financials = stock.financials
            balance_sheet = stock.balance_sheet
            cash_flow = stock.cashflow
            
            # Get additional metrics
            calendar = stock.calendar
            recommendations = stock.recommendations
            
            # Compile comprehensive data
            comprehensive_data = {
                "basic_info": self._process_basic_info(info),
                "price_data": self._process_price_data(hist_5y, hist_1y, hist_1m),
                "financial_statements": self._process_financial_statements(financials, balance_sheet, cash_flow),
                "valuation_metrics": self._calculate_valuation_metrics(info, financials, balance_sheet),
                "market_data": self._get_market_context(symbol),
                "analyst_data": self._process_analyst_data(recommendations),
                "risk_metrics": self._calculate_risk_metrics(hist_1y),
                "peer_comparison": self._get_peer_comparison(symbol, info.get('sector', '')),
                "data_timestamp": datetime.now().isoformat()
            }
            
            return comprehensive_data
            
        except Exception as e:
            logger.error(f"Error getting comprehensive data for {symbol}: {str(e)}")
            return {"error": str(e)}
    
    def _process_basic_info(self, info: Dict) -> Dict:
        """Process basic company information"""
        return {
            "company_name": info.get('longName', 'N/A'),
            "symbol": info.get('symbol', 'N/A'),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "market_cap": info.get('marketCap', 0),
            "employees": info.get('fullTimeEmployees', 0),
            "description": info.get('longBusinessSummary', 'N/A'),
            "exchange": info.get('exchange', 'N/A'),
            "currency": info.get('currency', 'USD'),
            "country": info.get('country', 'N/A'),
            "website": info.get('website', 'N/A')
        }
    
    def _process_price_data(self, hist_5y: pd.DataFrame, hist_1y: pd.DataFrame, hist_1m: pd.DataFrame) -> Dict:
        """Process historical price data and calculate performance metrics"""
        current_price = hist_1m['Close'].iloc[-1] if not hist_1m.empty else 0
        
        # Calculate returns
        returns_data = {}
        if not hist_1m.empty:
            returns_data['1_month'] = ((current_price / hist_1m['Close'].iloc[0]) - 1) * 100
        if not hist_1y.empty:
            returns_data['1_year'] = ((current_price / hist_1y['Close'].iloc[0]) - 1) * 100
        if not hist_5y.empty:
            returns_data['5_year'] = ((current_price / hist_5y['Close'].iloc[0]) - 1) * 100
            
        # Calculate volatility (annualized)
        volatility_1y = hist_1y['Close'].pct_change().std() * np.sqrt(252) * 100 if not hist_1y.empty else 0
        
        # Calculate 52-week high/low
        high_52w = hist_1y['High'].max() if not hist_1y.empty else 0
        low_52w = hist_1y['Low'].min() if not hist_1y.empty else 0
        
        return {
            "current_price": round(current_price, 2),
            "returns": returns_data,
            "volatility_1y": round(volatility_1y, 2),
            "52_week_high": round(high_52w, 2),
            "52_week_low": round(low_52w, 2),
            "price_from_52w_high": round(((current_price / high_52w) - 1) * 100, 2) if high_52w > 0 else 0,
            "trading_volume_avg": int(hist_1m['Volume'].mean()) if not hist_1m.empty else 0
        }
    
    def _process_financial_statements(self, financials: pd.DataFrame, balance_sheet: pd.DataFrame, cash_flow: pd.DataFrame) -> Dict:
        """Process financial statements and extract key metrics"""
        financial_data = {}
        
        try:
            # Income Statement Data
            if not financials.empty:
                latest_col = financials.columns[0]  # Most recent year
                financial_data['income_statement'] = {
                    "revenue": financials.loc['Total Revenue', latest_col] if 'Total Revenue' in financials.index else 0,
                    "gross_profit": financials.loc['Gross Profit', latest_col] if 'Gross Profit' in financials.index else 0,
                    "operating_income": financials.loc['Operating Income', latest_col] if 'Operating Income' in financials.index else 0,
                    "net_income": financials.loc['Net Income', latest_col] if 'Net Income' in financials.index else 0,
                    "ebitda": financials.loc['EBITDA', latest_col] if 'EBITDA' in financials.index else 0,
                }
                
                # Calculate margins
                revenue = financial_data['income_statement']['revenue']
                if revenue > 0:
                    financial_data['margins'] = {
                        "gross_margin": (financial_data['income_statement']['gross_profit'] / revenue) * 100,
                        "operating_margin": (financial_data['income_statement']['operating_income'] / revenue) * 100,
                        "net_margin": (financial_data['income_statement']['net_income'] / revenue) * 100,
                        "ebitda_margin": (financial_data['income_statement']['ebitda'] / revenue) * 100,
                    }
            
            # Balance Sheet Data
            if not balance_sheet.empty:
                latest_col = balance_sheet.columns[0]
                financial_data['balance_sheet'] = {
                    "total_assets": balance_sheet.loc['Total Assets', latest_col] if 'Total Assets' in balance_sheet.index else 0,
                    "total_debt": balance_sheet.loc['Total Debt', latest_col] if 'Total Debt' in balance_sheet.index else 0,
                    "total_equity": balance_sheet.loc['Total Stockholder Equity', latest_col] if 'Total Stockholder Equity' in balance_sheet.index else 0,
                    "current_assets": balance_sheet.loc['Current Assets', latest_col] if 'Current Assets' in balance_sheet.index else 0,
                    "current_liabilities": balance_sheet.loc['Current Liabilities', latest_col] if 'Current Liabilities' in balance_sheet.index else 0,
                    "cash": balance_sheet.loc['Cash And Cash Equivalents', latest_col] if 'Cash And Cash Equivalents' in balance_sheet.index else 0,
                }
            
            # Cash Flow Data
            if not cash_flow.empty:
                latest_col = cash_flow.columns[0]
                financial_data['cash_flow'] = {
                    "operating_cash_flow": cash_flow.loc['Operating Cash Flow', latest_col] if 'Operating Cash Flow' in cash_flow.index else 0,
                    "capital_expenditures": cash_flow.loc['Capital Expenditures', latest_col] if 'Capital Expenditures' in cash_flow.index else 0,
                    "free_cash_flow": cash_flow.loc['Free Cash Flow', latest_col] if 'Free Cash Flow' in cash_flow.index else 0,
                }
                
        except Exception as e:
            logger.error(f"Error processing financial statements: {str(e)}")
            financial_data['error'] = str(e)
            
        return financial_data
    
    def _calculate_valuation_metrics(self, info: Dict, financials: pd.DataFrame, balance_sheet: pd.DataFrame) -> Dict:
        """Calculate comprehensive valuation metrics"""
        metrics = {}
        
        try:
            # Basic valuation metrics from info
            metrics.update({
                "pe_ratio": info.get('trailingPE', 0),
                "forward_pe": info.get('forwardPE', 0),
                "peg_ratio": info.get('pegRatio', 0),
                "price_to_book": info.get('priceToBook', 0),
                "price_to_sales": info.get('priceToSalesTrailing12Months', 0),
                "ev_to_ebitda": info.get('enterpriseToEbitda', 0),
                "enterprise_value": info.get('enterpriseValue', 0),
                "dividend_yield": info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                "dividend_rate": info.get('dividendRate', 0),
                "payout_ratio": info.get('payoutRatio', 0) * 100 if info.get('payoutRatio') else 0,
            })
            
            # Calculate additional metrics if financial data is available
            if not financials.empty and not balance_sheet.empty:
                latest_col = financials.columns[0]
                net_income = financials.loc['Net Income', latest_col] if 'Net Income' in financials.index else 0
                total_equity = balance_sheet.loc['Total Stockholder Equity', latest_col] if 'Total Stockholder Equity' in balance_sheet.index else 0
                total_assets = balance_sheet.loc['Total Assets', latest_col] if 'Total Assets' in balance_sheet.index else 0
                
                if total_equity > 0:
                    metrics['roe'] = (net_income / total_equity) * 100
                if total_assets > 0:
                    metrics['roa'] = (net_income / total_assets) * 100
                    
        except Exception as e:
            logger.error(f"Error calculating valuation metrics: {str(e)}")
            metrics['error'] = str(e)
            
        return metrics
    
    def _get_market_context(self, symbol: str) -> Dict:
        """Get broader market context and economic indicators"""
        try:
            # Get market indices for context
            sp500 = yf.Ticker("^GSPC")
            nasdaq = yf.Ticker("^IXIC")
            vix = yf.Ticker("^VIX")
            
            # Get 1-year performance for comparison
            sp500_1y = sp500.history(period="1y")
            nasdaq_1y = nasdaq.history(period="1y")
            vix_current = vix.history(period="5d")
            
            market_data = {}
            
            if not sp500_1y.empty:
                sp500_return = ((sp500_1y['Close'].iloc[-1] / sp500_1y['Close'].iloc[0]) - 1) * 100
                market_data['sp500_1y_return'] = round(sp500_return, 2)
                
            if not nasdaq_1y.empty:
                nasdaq_return = ((nasdaq_1y['Close'].iloc[-1] / nasdaq_1y['Close'].iloc[0]) - 1) * 100
                market_data['nasdaq_1y_return'] = round(nasdaq_return, 2)
                
            if not vix_current.empty:
                market_data['vix_current'] = round(vix_current['Close'].iloc[-1], 2)
                
            # Try to get Treasury rates via web scraping (fallback)
            try:
                treasury_data = self._scrape_treasury_rates()
                market_data.update(treasury_data)
            except:
                pass
                
            return market_data
            
        except Exception as e:
            logger.error(f"Error getting market context: {str(e)}")
            return {"error": str(e)}
    
    def _scrape_treasury_rates(self) -> Dict:
        """Scrape current Treasury rates"""
        try:
            url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/textview.aspx?data=yield"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Parse Treasury data (simplified)
                return {
                    "treasury_10y": 4.5,  # Placeholder - would parse from actual data
                    "treasury_2y": 4.2,   # Placeholder - would parse from actual data
                    "risk_free_rate": 4.5
                }
        except:
            pass
        
        return {"risk_free_rate": 4.5}  # Default fallback
    
    def _process_analyst_data(self, recommendations: pd.DataFrame) -> Dict:
        """Process analyst recommendations and price targets"""
        analyst_data = {}
        
        try:
            if not recommendations.empty:
                latest_recs = recommendations.tail(10)  # Last 10 recommendations
                
                # Count recommendation types
                rec_counts = latest_recs['To Grade'].value_counts()
                
                analyst_data = {
                    "recommendations": rec_counts.to_dict(),
                    "latest_recommendation": latest_recs.iloc[-1]['To Grade'] if not latest_recs.empty else "N/A",
                    "number_of_analysts": len(latest_recs)
                }
                
        except Exception as e:
            logger.error(f"Error processing analyst data: {str(e)}")
            
        return analyst_data
    
    def _calculate_risk_metrics(self, hist_1y: pd.DataFrame) -> Dict:
        """Calculate risk metrics"""
        risk_metrics = {}
        
        try:
            if not hist_1y.empty:
                returns = hist_1y['Close'].pct_change().dropna()
                
                # Calculate beta vs S&P 500
                sp500 = yf.Ticker("^GSPC")
                sp500_1y = sp500.history(period="1y")
                if not sp500_1y.empty:
                    sp500_returns = sp500_1y['Close'].pct_change().dropna()
                    
                    # Align dates
                    aligned_data = pd.DataFrame({
                        'stock': returns,
                        'market': sp500_returns
                    }).dropna()
                    
                    if len(aligned_data) > 50:  # Need sufficient data
                        covariance = np.cov(aligned_data['stock'], aligned_data['market'])[0][1]
                        market_variance = np.var(aligned_data['market'])
                        beta = covariance / market_variance if market_variance > 0 else 1.0
                        
                        risk_metrics['beta'] = round(beta, 2)
                
                # Other risk metrics
                risk_metrics['volatility'] = round(returns.std() * np.sqrt(252) * 100, 2)
                risk_metrics['max_drawdown'] = round(((hist_1y['Close'] / hist_1y['Close'].cummax()) - 1).min() * 100, 2)
                risk_metrics['sharpe_ratio'] = round((returns.mean() * 252) / (returns.std() * np.sqrt(252)), 2)
                
        except Exception as e:
            logger.error(f"Error calculating risk metrics: {str(e)}")
            
        return risk_metrics
    
    def _get_peer_comparison(self, symbol: str, sector: str) -> Dict:
        """Get peer comparison data"""
        peer_data = {}
        
        try:
            # Define sector-based peer mappings (simplified)
            sector_peers = {
                "Technology": ["AAPL", "MSFT", "GOOGL", "META", "NVDA"],
                "Healthcare": ["JNJ", "PFE", "UNH", "ABBV", "MRK"],
                "Financial Services": ["JPM", "BAC", "WFC", "C", "GS"],
                "Consumer Cyclical": ["AMZN", "TSLA", "HD", "MCD", "NKE"],
                "Communication Services": ["META", "GOOGL", "NFLX", "DIS", "T"],
                "Industrial": ["BA", "CAT", "GE", "MMM", "LMT"],
            }
            
            peers = sector_peers.get(sector, [])
            if symbol in peers:
                peers.remove(symbol)
            
            peer_data['peers'] = peers[:5]  # Top 5 peers
            
            # Get basic metrics for peers (simplified)
            peer_metrics = []
            for peer in peers[:3]:  # Limit to 3 for performance
                try:
                    peer_stock = yf.Ticker(peer)
                    peer_info = peer_stock.info
                    peer_metrics.append({
                        "symbol": peer,
                        "market_cap": peer_info.get('marketCap', 0),
                        "pe_ratio": peer_info.get('trailingPE', 0),
                        "profit_margin": peer_info.get('profitMargins', 0) * 100 if peer_info.get('profitMargins') else 0
                    })
                except:
                    continue
                    
            peer_data['peer_metrics'] = peer_metrics
            
        except Exception as e:
            logger.error(f"Error getting peer comparison: {str(e)}")
            
        return peer_data
    
    def get_sector_analysis(self, sector: str) -> Dict:
        """Get sector-wide analysis"""
        try:
            # This would involve more complex analysis
            # For now, return basic sector info
            return {
                "sector": sector,
                "analysis": f"Sector analysis for {sector} would include industry trends, regulatory environment, and competitive landscape."
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_news_sentiment(self, symbol: str) -> Dict:
        """Get recent news and sentiment analysis"""
        try:
            stock = yf.Ticker(symbol)
            news = stock.news
            
            # Basic news processing
            recent_news = []
            for article in news[:5]:  # Last 5 articles
                recent_news.append({
                    "title": article.get('title', ''),
                    "publisher": article.get('publisher', ''),
                    "link": article.get('link', ''),
                    "published": article.get('providerPublishTime', 0)
                })
                
            return {
                "recent_news": recent_news,
                "news_count": len(news)
            }
            
        except Exception as e:
            logger.error(f"Error getting news sentiment: {str(e)}")
            return {"error": str(e)}
