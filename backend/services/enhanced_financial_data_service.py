import yfinance as yf
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Optional, Any
import warnings
warnings.filterwarnings('ignore')

class EnhancedFinancialDataService:
    """
    Enhanced financial data service using only free data sources:
    - Yahoo Finance (via yfinance)
    - Web scraping for additional data
    - SEC EDGAR for filings
    - FRED for economic indicators
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Cache for data to avoid repeated API calls
        self.cache = {}
        self.cache_expiry = 300  # 5 minutes
        
        # Web scraping configurations
        self.scraping_delay = 1  # Delay between requests to be respectful
        self.max_retries = 3
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _get_cached_data(self, key: str) -> Optional[Dict]:
        """Get cached data if still valid"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_expiry:
                return data
        return None
    
    def _cache_data(self, key: str, data: Dict):
        """Cache data with timestamp"""
        self.cache[key] = (data, time.time())
    
    def get_comprehensive_stock_data(self, symbol: str) -> Dict[str, Any]:
        """
        Get comprehensive stock data from multiple free sources
        """
        try:
            # Check cache first
            cache_key = f"comprehensive_{symbol}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
            symbol = symbol.upper()
            self.logger.info(f"Fetching comprehensive data for {symbol}")
            
            # Get Yahoo Finance data
            ticker = yf.Ticker(symbol)
            
            # Validate that the ticker exists by checking basic info
            try:
                info = ticker.info
                if not info or not any(key in info for key in ['symbol', 'shortName', 'longName', 'regularMarketPrice']):
                    return {"error": f"Invalid or non-existent stock symbol: {symbol}. Please verify the ticker symbol."}
            except Exception as e:
                return {"error": f"Unable to retrieve data for {symbol}. Symbol may be invalid or delisted."}
            
            # Gather all data including web scraping
            result = {
                'symbol': symbol,
                'data_timestamp': datetime.now().isoformat(),
                'basic_info': self._get_basic_info(ticker),
                'price_data': self._get_price_data(ticker),
                'financial_statements': self._get_financial_statements(ticker),
                'valuation_metrics': self._get_valuation_metrics(ticker),
                'risk_metrics': self._get_risk_metrics(ticker),
                'analyst_data': self._get_analyst_data(ticker),
                'news_data': self._get_news_data(ticker),
                'peer_comparison': self._get_peer_comparison(ticker),
                'market_data': self._get_market_context(),
                'web_scraped_data': self.get_enhanced_web_data(symbol),
                'technical_indicators': self.get_technical_indicators(symbol)
            }
            
            # Validate that we got meaningful data
            if not any([
                result['basic_info'].get('company_name', '') != 'N/A',
                result['price_data'].get('current_price', 0) > 0,
                result['valuation_metrics'].get('market_cap', 0) > 0
            ]):
                return {"error": f"No meaningful financial data available for {symbol}. Symbol may be inactive or delisted."}
            
            # Cache the result
            self._cache_data(cache_key, result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return {"error": f"Failed to fetch data for {symbol}: {str(e)}. Please verify the symbol is correct and active."}
    
    def _get_basic_info(self, ticker) -> Dict[str, Any]:
        """Get basic company information"""
        try:
            info = ticker.info
            return {
                'company_name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'country': info.get('country', 'N/A'),
                'website': info.get('website', 'N/A'),
                'business_summary': info.get('longBusinessSummary', 'N/A')[:500] + '...' if info.get('longBusinessSummary') else 'N/A',
                'employees': info.get('fullTimeEmployees', 0),
                'market_cap': info.get('marketCap', 0),
                'enterprise_value': info.get('enterpriseValue', 0),
                'founded': info.get('foundingDate', 'N/A')
            }
        except Exception as e:
            self.logger.error(f"Error getting basic info: {str(e)}")
            return {}
    
    def _get_price_data(self, ticker) -> Dict[str, Any]:
        """Get comprehensive price and performance data"""
        try:
            info = ticker.info
            hist = ticker.history(period="2y")
            
            if hist.empty:
                return {}
            
            current_price = hist['Close'].iloc[-1]
            
            # Calculate returns
            returns = {}
            periods = {
                '1_day': 1,
                '5_day': 5,
                '1_month': 22,
                '3_month': 66,
                '6_month': 132,
                '1_year': 252,
                '2_year': 504
            }
            
            for period_name, days in periods.items():
                if len(hist) > days:
                    start_price = hist['Close'].iloc[-days-1]
                    returns[period_name] = ((current_price - start_price) / start_price * 100)
            
            # Volatility calculation
            daily_returns = hist['Close'].pct_change().dropna()
            volatility_daily = daily_returns.std()
            volatility_annual = volatility_daily * np.sqrt(252) * 100
            
            # Trading metrics
            volume_avg = hist['Volume'].tail(30).mean()
            
            return {
                'current_price': float(current_price),
                '52_week_high': info.get('fiftyTwoWeekHigh', float(hist['High'].max())),
                '52_week_low': info.get('fiftyTwoWeekLow', float(hist['Low'].min())),
                'price_from_52w_high': ((current_price - info.get('fiftyTwoWeekHigh', hist['High'].max())) / info.get('fiftyTwoWeekHigh', hist['High'].max()) * 100),
                'returns': returns,
                'volatility_1y': float(volatility_annual),
                'trading_volume_avg': int(volume_avg),
                'day_range_low': info.get('dayLow', 0),
                'day_range_high': info.get('dayHigh', 0),
                'previous_close': info.get('previousClose', 0),
                'opening_price': info.get('open', 0)
            }
        except Exception as e:
            self.logger.error(f"Error getting price data: {str(e)}")
            return {}
    
    def _get_financial_statements(self, ticker) -> Dict[str, Any]:
        """Get financial statement data"""
        try:
            # Get financial data
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cash_flow = ticker.cashflow
            
            result = {}
            
            # Income Statement metrics
            if not financials.empty:
                latest_year = financials.columns[0]
                result['income_statement'] = {
                    'total_revenue': self._safe_get_financial_value(financials, 'Total Revenue', latest_year),
                    'gross_profit': self._safe_get_financial_value(financials, 'Gross Profit', latest_year),
                    'operating_income': self._safe_get_financial_value(financials, 'Operating Income', latest_year),
                    'net_income': self._safe_get_financial_value(financials, 'Net Income', latest_year),
                    'ebitda': self._safe_get_financial_value(financials, 'EBITDA', latest_year)
                }
                
                # Calculate margins
                revenue = result['income_statement']['total_revenue']
                if revenue and revenue != 0:
                    result['margins'] = {
                        'gross_margin': (result['income_statement']['gross_profit'] / revenue * 100) if result['income_statement']['gross_profit'] else 0,
                        'operating_margin': (result['income_statement']['operating_income'] / revenue * 100) if result['income_statement']['operating_income'] else 0,
                        'net_margin': (result['income_statement']['net_income'] / revenue * 100) if result['income_statement']['net_income'] else 0
                    }
            
            # Balance Sheet metrics
            if not balance_sheet.empty:
                latest_year = balance_sheet.columns[0]
                result['balance_sheet'] = {
                    'total_assets': self._safe_get_financial_value(balance_sheet, 'Total Assets', latest_year),
                    'total_debt': self._safe_get_financial_value(balance_sheet, 'Total Debt', latest_year),
                    'cash_and_equivalents': self._safe_get_financial_value(balance_sheet, 'Cash And Cash Equivalents', latest_year),
                    'total_equity': self._safe_get_financial_value(balance_sheet, 'Total Equity Gross Minority Interest', latest_year),
                    'working_capital': self._safe_get_financial_value(balance_sheet, 'Working Capital', latest_year)
                }
            
            # Cash Flow metrics
            if not cash_flow.empty:
                latest_year = cash_flow.columns[0]
                result['cash_flow'] = {
                    'operating_cash_flow': self._safe_get_financial_value(cash_flow, 'Operating Cash Flow', latest_year),
                    'free_cash_flow': self._safe_get_financial_value(cash_flow, 'Free Cash Flow', latest_year),
                    'capital_expenditure': self._safe_get_financial_value(cash_flow, 'Capital Expenditure', latest_year)
                }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting financial statements: {str(e)}")
            return {}
    
    def _safe_get_financial_value(self, df, metric_name, period):
        """Safely extract financial values"""
        try:
            # Try exact match first
            if metric_name in df.index:
                value = df.loc[metric_name, period]
                return float(value) if pd.notna(value) else 0
            
            # Try case-insensitive partial match
            for index in df.index:
                if metric_name.lower() in str(index).lower():
                    value = df.loc[index, period]
                    return float(value) if pd.notna(value) else 0
            
            return 0
        except:
            return 0
    
    def _get_valuation_metrics(self, ticker) -> Dict[str, Any]:
        """Get valuation metrics"""
        try:
            info = ticker.info
            return {
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'peg_ratio': info.get('pegRatio', 0),
                'price_to_book': info.get('priceToBook', 0),
                'price_to_sales': info.get('priceToSalesTrailing12Months', 0),
                'ev_to_ebitda': info.get('enterpriseToEbitda', 0),
                'enterprise_value': info.get('enterpriseValue', 0),
                'market_cap': info.get('marketCap', 0),
                'book_value': info.get('bookValue', 0),
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'dividend_rate': info.get('dividendRate', 0),
                'payout_ratio': info.get('payoutRatio', 0) * 100 if info.get('payoutRatio') else 0
            }
        except Exception as e:
            self.logger.error(f"Error getting valuation metrics: {str(e)}")
            return {}
    
    def _get_risk_metrics(self, ticker) -> Dict[str, Any]:
        """Calculate risk metrics"""
        try:
            info = ticker.info
            hist = ticker.history(period="2y")
            
            if hist.empty:
                return {}
            
            # Calculate daily returns
            daily_returns = hist['Close'].pct_change().dropna()
            
            # Beta calculation (vs S&P 500)
            spy_data = yf.download("^GSPC", period="2y", progress=False)
            if not spy_data.empty:
                spy_returns = spy_data['Close'].pct_change().dropna()
                
                # Align dates
                common_dates = daily_returns.index.intersection(spy_returns.index)
                if len(common_dates) > 50:
                    stock_aligned = daily_returns.loc[common_dates]
                    spy_aligned = spy_returns.loc[common_dates]
                    
                    covariance = np.cov(stock_aligned, spy_aligned)[0][1]
                    spy_variance = np.var(spy_aligned)
                    beta = covariance / spy_variance if spy_variance != 0 else 1.0
                else:
                    beta = info.get('beta', 1.0)
            else:
                beta = info.get('beta', 1.0)
            
            # Volatility
            volatility = daily_returns.std() * np.sqrt(252) * 100
            
            # Maximum drawdown
            cumulative = (1 + daily_returns).cumprod()
            rolling_max = cumulative.expanding().max()
            drawdown = (cumulative - rolling_max) / rolling_max
            max_drawdown = drawdown.min() * 100
            
            # Sharpe ratio (assuming 2% risk-free rate)
            risk_free_rate = 0.02
            excess_returns = daily_returns.mean() * 252 - risk_free_rate
            sharpe_ratio = excess_returns / (daily_returns.std() * np.sqrt(252)) if daily_returns.std() != 0 else 0
            
            return {
                'beta': float(beta),
                'volatility': float(volatility),
                'max_drawdown': float(max_drawdown),
                'sharpe_ratio': float(sharpe_ratio),
                'var_95': float(np.percentile(daily_returns, 5) * 100),  # Value at Risk
                'current_ratio': info.get('currentRatio', 0),
                'debt_to_equity': info.get('debtToEquity', 0)
            }
        except Exception as e:
            self.logger.error(f"Error calculating risk metrics: {str(e)}")
            return {}
    
    def _get_analyst_data(self, ticker) -> Dict[str, Any]:
        """Get analyst recommendations and estimates"""
        try:
            recommendations = ticker.recommendations
            if recommendations is not None and not recommendations.empty:
                latest_recs = recommendations.tail(10)  # Last 10 recommendations
                
                # Count recommendation types
                rec_counts = latest_recs['To Grade'].value_counts().to_dict()
                
                return {
                    'recommendations': rec_counts,
                    'latest_recommendation': latest_recs.iloc[-1]['To Grade'] if not latest_recs.empty else 'N/A',
                    'recommendation_count': len(latest_recs)
                }
            
            return {'recommendations': {}, 'latest_recommendation': 'N/A'}
            
        except Exception as e:
            self.logger.error(f"Error getting analyst data: {str(e)}")
            return {}
    
    def _get_news_data(self, ticker) -> Dict[str, Any]:
        """Get recent news data"""
        try:
            news = ticker.news
            if news:
                recent_news = []
                for article in news[:5]:  # Top 5 news items
                    recent_news.append({
                        'title': article.get('title', ''),
                        'publisher': article.get('publisher', ''),
                        'publish_time': datetime.fromtimestamp(article.get('providerPublishTime', 0)).strftime('%Y-%m-%d') if article.get('providerPublishTime') else 'N/A'
                    })
                
                return {
                    'recent_news': recent_news,
                    'news_count': len(news)
                }
            
            return {'recent_news': [], 'news_count': 0}
            
        except Exception as e:
            self.logger.error(f"Error getting news data: {str(e)}")
            return {}
    
    def _get_peer_comparison(self, ticker) -> Dict[str, Any]:
        """Get peer comparison data"""
        try:
            info = ticker.info
            sector = info.get('sector', '')
            
            # Common peers by sector (simplified)
            sector_peers = {
                'Technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA'],
                'Healthcare': ['JNJ', 'PFE', 'UNH', 'ABBV', 'TMO'],
                'Financial Services': ['JPM', 'BAC', 'WFC', 'GS', 'MS'],
                'Consumer Cyclical': ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE'],
                'Communication Services': ['META', 'GOOGL', 'NFLX', 'DIS', 'T'],
                'Industrial': ['BA', 'CAT', 'GE', 'LMT', 'UPS'],
                'Consumer Defensive': ['PG', 'KO', 'PEP', 'WMT', 'COST'],
                'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB'],
                'Utilities': ['NEE', 'SO', 'DUK', 'AEP', 'EXC'],
                'Real Estate': ['AMT', 'PLD', 'CCI', 'EQIX', 'PSA'],
                'Materials': ['LIN', 'APD', 'ECL', 'SHW', 'FCX']
            }
            
            peers = sector_peers.get(sector, [])
            symbol = ticker.ticker
            
            # Remove current symbol from peers
            if symbol in peers:
                peers.remove(symbol)
            
            return {
                'peers': peers[:5],  # Top 5 peers
                'sector': sector
            }
            
        except Exception as e:
            self.logger.error(f"Error getting peer comparison: {str(e)}")
            return {}
    
    def _get_market_context(self) -> Dict[str, Any]:
        """Get broader market context"""
        try:
            # Get major indices
            indices = {
                '^GSPC': 'S&P 500',
                '^IXIC': 'NASDAQ',
                '^DJI': 'Dow Jones',
                '^VIX': 'VIX'
            }
            
            market_data = {}
            
            for symbol, name in indices.items():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="1y")
                    
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        year_start_price = hist['Close'].iloc[0]
                        year_return = ((current_price - year_start_price) / year_start_price * 100)
                        
                        if symbol == '^VIX':
                            market_data['vix_current'] = float(current_price)
                        elif symbol == '^GSPC':
                            market_data['sp500_1y_return'] = float(year_return)
                        elif symbol == '^IXIC':
                            market_data['nasdaq_1y_return'] = float(year_return)
                        elif symbol == '^DJI':
                            market_data['dow_1y_return'] = float(year_return)
                            
                except Exception as idx_error:
                    self.logger.error(f"Error getting data for {symbol}: {str(idx_error)}")
                    continue
            
            return market_data
            
        except Exception as e:
            self.logger.error(f"Error getting market context: {str(e)}")
            return {}
    
    def get_stock_fundamentals(self, symbol: str) -> Dict[str, Any]:
        """Get focused fundamental analysis data"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'price_to_book': info.get('priceToBook', 0),
                'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
                'debt_to_equity': info.get('debtToEquity', 0),
                'current_ratio': info.get('currentRatio', 0),
                'revenue_growth': info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0,
                'profit_margin': info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0,
                'operating_margin': info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0
            }
            
        except Exception as e:
            return {"error": f"Error getting fundamentals for {symbol}: {str(e)}"}
    
    def get_technical_indicators(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Calculate basic technical indicators"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return {"error": "No historical data available"}
            
            close_prices = hist['Close']
            
            # Simple Moving Averages
            sma_20 = close_prices.rolling(window=20).mean().iloc[-1]
            sma_50 = close_prices.rolling(window=50).mean().iloc[-1]
            sma_200 = close_prices.rolling(window=200).mean().iloc[-1]
            
            current_price = close_prices.iloc[-1]
            
            # RSI calculation
            delta = close_prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            return {
                'current_price': float(current_price),
                'sma_20': float(sma_20) if pd.notna(sma_20) else 0,
                'sma_50': float(sma_50) if pd.notna(sma_50) else 0,
                'sma_200': float(sma_200) if pd.notna(sma_200) else 0,
                'rsi': float(rsi) if pd.notna(rsi) else 50,
                'price_vs_sma20': ((current_price - sma_20) / sma_20 * 100) if pd.notna(sma_20) else 0,
                'price_vs_sma50': ((current_price - sma_50) / sma_50 * 100) if pd.notna(sma_50) else 0,
                'price_vs_sma200': ((current_price - sma_200) / sma_200 * 100) if pd.notna(sma_200) else 0
            }
        except Exception as e:
            self.logger.error(f"Error calculating technical indicators for {symbol}: {str(e)}")
            return {"error": f"Error calculating technical indicators for {symbol}: {str(e)}"}
    
    # =============================================================================
    # WEB SCRAPING METHODS
    # =============================================================================
    
    def _safe_request(self, url: str, retries: int = None) -> Optional[requests.Response]:
        """Make a safe HTTP request with retries and proper error handling"""
        if retries is None:
            retries = self.max_retries
            
        for attempt in range(retries):
            try:
                time.sleep(self.scraping_delay)  # Be respectful with delays
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}/{retries}): {str(e)}")
                if attempt == retries - 1:
                    self.logger.error(f"All {retries} attempts failed for URL: {url}")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
        return None
    
    def scrape_finviz_data(self, symbol: str) -> Dict[str, Any]:
        """Scrape additional financial metrics from Finviz"""
        try:
            url = f"https://finviz.com/quote.ashx?t={symbol.upper()}"
            response = self._safe_request(url)
            
            if not response:
                return {"error": "Failed to fetch Finviz data"}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the fundamental data table
            table = soup.find('table', {'class': 'snapshot-table2'})
            if not table:
                return {"error": "Could not find fundamental data table"}
            
            data = {}
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all('td')
                for i in range(0, len(cells), 2):
                    if i + 1 < len(cells):
                        key = cells[i].get_text(strip=True)
                        value = cells[i + 1].get_text(strip=True)
                        data[key] = value
            
            # Parse relevant metrics
            parsed_data = {
                'finviz_pe': self._parse_numeric(data.get('P/E', '')),
                'finviz_forward_pe': self._parse_numeric(data.get('Forward P/E', '')),
                'finviz_peg': self._parse_numeric(data.get('PEG', '')),
                'finviz_price_book': self._parse_numeric(data.get('P/B', '')),
                'finviz_price_sales': self._parse_numeric(data.get('P/S', '')),
                'finviz_roe': self._parse_percentage(data.get('ROE', '')),
                'finviz_roa': self._parse_percentage(data.get('ROA', '')),
                'finviz_debt_equity': self._parse_numeric(data.get('Debt/Eq', '')),
                'finviz_current_ratio': self._parse_numeric(data.get('Current Ratio', '')),
                'finviz_gross_margin': self._parse_percentage(data.get('Gross Margin', '')),
                'finviz_profit_margin': self._parse_percentage(data.get('Profit Margin', '')),
                'finviz_insider_own': self._parse_percentage(data.get('Insider Own', '')),
                'finviz_inst_own': self._parse_percentage(data.get('Inst Own', '')),
                'finviz_short_float': self._parse_percentage(data.get('Short Float', '')),
                'finviz_analyst_recom': data.get('Recom', 'N/A'),
                'finviz_target_price': self._parse_numeric(data.get('Target Price', ''))
            }
            
            return parsed_data
            
        except Exception as e:
            self.logger.error(f"Error scraping Finviz data for {symbol}: {str(e)}")
            return {"error": f"Finviz scraping failed: {str(e)}"}
    
    def scrape_marketwatch_news(self, symbol: str) -> Dict[str, Any]:
        """Scrape recent news from MarketWatch"""
        try:
            url = f"https://www.marketwatch.com/investing/stock/{symbol.lower()}"
            response = self._safe_request(url)
            
            if not response:
                return {"error": "Failed to fetch MarketWatch data"}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find news articles
            news_articles = []
            
            # Look for different news section patterns
            news_selectors = [
                'div.element--article',
                'div.article__content',
                'div.latest-news__item',
                'article.article'
            ]
            
            for selector in news_selectors:
                articles = soup.select(selector)
                if articles:
                    break
            
            for article in articles[:10]:  # Limit to 10 articles
                try:
                    title_elem = article.find(['h3', 'h4', 'h5', 'a'])
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                        
                        # Find timestamp
                        time_elem = article.find('time') or article.find(class_='timestamp')
                        timestamp = time_elem.get_text(strip=True) if time_elem else 'Recent'
                        
                        news_articles.append({
                            'title': title,
                            'link': f"https://www.marketwatch.com{link}" if link.startswith('/') else link,
                            'timestamp': timestamp,
                            'source': 'MarketWatch'
                        })
                except Exception as e:
                    continue
            
            return {
                'articles': news_articles,
                'article_count': len(news_articles),
                'source': 'MarketWatch'
            }
            
        except Exception as e:
            self.logger.error(f"Error scraping MarketWatch news for {symbol}: {str(e)}")
            return {"error": f"MarketWatch news scraping failed: {str(e)}"}
    
    def scrape_seeking_alpha_analysis(self, symbol: str) -> Dict[str, Any]:
        """Scrape analysis and sentiment from Seeking Alpha"""
        try:
            url = f"https://seekingalpha.com/symbol/{symbol.upper()}"
            response = self._safe_request(url)
            
            if not response:
                return {"error": "Failed to fetch Seeking Alpha data"}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract analyst ratings and sentiment
            data = {
                'articles': [],
                'analyst_sentiment': 'N/A',
                'price_target': 'N/A',
                'rating_summary': 'N/A'
            }
            
            # Look for recent articles
            article_links = soup.find_all('a', {'data-test-id': 'post-list-item-title'})
            
            for link in article_links[:5]:  # Limit to 5 articles
                try:
                    title = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    data['articles'].append({
                        'title': title,
                        'link': f"https://seekingalpha.com{href}" if href.startswith('/') else href,
                        'source': 'Seeking Alpha'
                    })
                except Exception:
                    continue
            
            # Look for analyst consensus data
            rating_elem = soup.find(string=lambda text: text and 'Strong Buy' in text or 'Buy' in text or 'Hold' in text)
            if rating_elem:
                data['analyst_sentiment'] = rating_elem.strip()
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error scraping Seeking Alpha for {symbol}: {str(e)}")
            return {"error": f"Seeking Alpha scraping failed: {str(e)}"}
    
    def scrape_yahoo_finance_news(self, symbol: str) -> Dict[str, Any]:
        """Scrape additional news from Yahoo Finance"""
        try:
            url = f"https://finance.yahoo.com/quote/{symbol.upper()}/news"
            response = self._safe_request(url)
            
            if not response:
                return {"error": "Failed to fetch Yahoo Finance news"}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            news_articles = []
            
            # Find news articles using various selectors
            article_selectors = [
                'div[data-test-locator="mega"] h3',
                'h3[data-test-locator="headline"]',
                'div.caas-body h3',
                'li.js-stream-content h3'
            ]
            
            for selector in article_selectors:
                headlines = soup.select(selector)
                if headlines:
                    break
            
            for headline in headlines[:10]:
                try:
                    title = headline.get_text(strip=True)
                    link_elem = headline.find('a') or headline.find_parent('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    
                    if title and len(title) > 10:  # Filter out very short titles
                        news_articles.append({
                            'title': title,
                            'link': f"https://finance.yahoo.com{link}" if link.startswith('/') else link,
                            'source': 'Yahoo Finance'
                        })
                except Exception:
                    continue
            
            return {
                'articles': news_articles,
                'article_count': len(news_articles),
                'source': 'Yahoo Finance'
            }
            
        except Exception as e:
            self.logger.error(f"Error scraping Yahoo Finance news for {symbol}: {str(e)}")
            return {"error": f"Yahoo Finance news scraping failed: {str(e)}"}
    
    def scrape_sec_filings(self, symbol: str) -> Dict[str, Any]:
        """Scrape recent SEC filings for the company"""
        try:
            # Use SEC EDGAR RSS feed
            url = f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={symbol}&owner=exclude&action=getcompany&output=atom"
            response = self._safe_request(url)
            
            if not response:
                return {"error": "Failed to fetch SEC data"}
            
            soup = BeautifulSoup(response.content, 'xml')
            
            filings = []
            entries = soup.find_all('entry')[:10]  # Get last 10 filings
            
            for entry in entries:
                try:
                    title = entry.find('title').get_text(strip=True) if entry.find('title') else 'N/A'
                    link = entry.find('link')['href'] if entry.find('link') else ''
                    updated = entry.find('updated').get_text(strip=True) if entry.find('updated') else 'N/A'
                    
                    filings.append({
                        'title': title,
                        'link': link,
                        'date': updated,
                        'source': 'SEC EDGAR'
                    })
                except Exception:
                    continue
            
            return {
                'recent_filings': filings,
                'filing_count': len(filings),
                'source': 'SEC EDGAR'
            }
            
        except Exception as e:
            self.logger.error(f"Error scraping SEC filings for {symbol}: {str(e)}")
            return {"error": f"SEC filing scraping failed: {str(e)}"}
    
    def scrape_insider_trading(self, symbol: str) -> Dict[str, Any]:
        """Scrape insider trading information"""
        try:
            # This is a placeholder for insider trading data
            # In practice, you might scrape from multiple sources
            url = f"https://www.secform4.com/insider-trading/{symbol.lower()}.htm"
            response = self._safe_request(url)
            
            if not response:
                return {"error": "Failed to fetch insider trading data"}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for insider trading table
            trading_data = []
            table = soup.find('table', {'class': 'tinytable'})
            
            if table:
                rows = table.find_all('tr')[1:]  # Skip header
                for row in rows[:10]:  # Limit to 10 transactions
                    cells = row.find_all('td')
                    if len(cells) >= 4:
                        trading_data.append({
                            'insider': cells[0].get_text(strip=True),
                            'transaction_type': cells[1].get_text(strip=True),
                            'shares': cells[2].get_text(strip=True),
                            'date': cells[3].get_text(strip=True)
                        })
            
            return {
                'insider_transactions': trading_data,
                'transaction_count': len(trading_data),
                'source': 'SEC Form 4'
            }
            
        except Exception as e:
            self.logger.error(f"Error scraping insider trading for {symbol}: {str(e)}")
            return {"error": f"Insider trading scraping failed: {str(e)}"}
    
    def get_enhanced_web_data(self, symbol: str) -> Dict[str, Any]:
        """Get enhanced data from web scraping sources"""
        try:
            cache_key = f"web_data_{symbol}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
            # Scrape from multiple sources
            web_data = {
                'symbol': symbol.upper(),
                'scraping_timestamp': datetime.now().isoformat(),
                'finviz_metrics': self.scrape_finviz_data(symbol),
                'marketwatch_news': self.scrape_marketwatch_news(symbol),
                'seeking_alpha_analysis': self.scrape_seeking_alpha_analysis(symbol),
                'yahoo_news': self.scrape_yahoo_finance_news(symbol),
                'sec_filings': self.scrape_sec_filings(symbol),
                'insider_trading': self.scrape_insider_trading(symbol)
            }
            
            # Cache the result
            self._cache_data(cache_key, web_data)
            
            return web_data
            
        except Exception as e:
            self.logger.error(f"Error getting enhanced web data for {symbol}: {str(e)}")
            return {"error": f"Web scraping failed: {str(e)}"}
    
    # =============================================================================
    # UTILITY METHODS FOR PARSING
    # =============================================================================
    
    def _parse_numeric(self, value: str) -> float:
        """Parse numeric values from scraped text"""
        try:
            # Remove common non-numeric characters
            clean_value = value.replace(',', '').replace('$', '').replace('%', '').replace('B', '').replace('M', '').replace('K', '')
            
            # Handle special cases
            if value == '-' or value == 'N/A' or not value:
                return 0.0
            
            # Convert percentage values
            if '%' in value:
                return float(clean_value) / 100
            
            # Convert abbreviated numbers
            multiplier = 1
            if 'B' in value:
                multiplier = 1e9
            elif 'M' in value:
                multiplier = 1e6
            elif 'K' in value:
                multiplier = 1e3
            
            return float(clean_value) * multiplier
            
        except (ValueError, TypeError):
            return 0.0
    
    def _parse_percentage(self, value: str) -> float:
        """Parse percentage values from scraped text"""
        try:
            if '%' in value:
                return float(value.replace('%', '').replace(',', ''))
            return float(value.replace(',', ''))
        except (ValueError, TypeError):
            return 0.0
