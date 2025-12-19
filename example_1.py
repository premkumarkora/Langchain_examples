import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="Specialized AI Stock Worker",
    page_icon="📈",
    layout="wide"
)

def main():
    # 2. Header & Title
    st.title("🤖 Specialized AI Worker: Market Analyst")
    st.markdown("""
    This demo showcases a specialized AI worker logic: 
    **User Input** --> **Function Call (yfinance)** --> **Live Data Output**.
    """)
    st.divider()

    # 3. Sidebar Input
    st.sidebar.header("Agent Configuration")
    ticker_symbol = st.sidebar.text_input("Enter Company Ticker", value="", help="Example: NVDA, AAPL, MSFT, TSLA").upper()
    
    fetch_button = st.sidebar.button("Fetch Stock price & News")

    if fetch_button and ticker_symbol:
        try:
            # 4. Data Extraction Logic (AI Worker Function)
            with st.spinner(f"Agent is fetching live data for {ticker_symbol}..."):
                ticker = yf.Ticker(ticker_symbol)
                
                # Fetching price data
                # Using fast_info for better performance
                try:
                    f_info = ticker.fast_info
                    current_price = f_info.get('lastPrice') or f_info.get('regularMarketPrice') or 0.0
                    previous_close = f_info.get('previousClose') or f_info.get('regularMarketPreviousClose') or current_price
                    
                    price_change = current_price - previous_close
                    pct_change = (price_change / previous_close) * 100 if previous_close else 0.0
                    
                    day_high = f_info.get('dayHigh', 0.0)
                    day_low = f_info.get('dayLow', 0.0)
                    currency = f_info.get('currency', 'USD')
                except Exception as fe:
                    st.warning("Some market metrics were unavailable.")
                    current_price = 0.0
                    price_change = 0.0
                    pct_change = 0.0
                    day_high = 0.0
                    day_low = 0.0
                    currency = "Unknown"
                
                # Fetching News
                news_feed = ticker.news[:3] # Get top 3

            # 5. Displaying Results
            col1, col2 = st.columns([1, 2])

            with col1:
                st.subheader("Current Performance")
                st.metric(
                    label=f"{ticker_symbol} Price",
                    value=f"${current_price:.2f}",
                    delta=f"{price_change:.2f} ({pct_change:.2f}%)"
                )
                
                # Extra stats
                st.write(f"**Day High:** ${day_high:.2f}")
                st.write(f"**Day Low:** ${day_low:.2f}")
                st.write(f"**Currency:** {currency}")

            with col2:
                st.subheader("Latest Intelligence Feed")
                if news_feed:
                    for article in news_feed:
                        # yfinance structure has changed in recent versions
                        # Old: {title: ..., link: ..., providerPublishTime: ...}
                        # New: {content: {title: ..., canonicalUrl: {url: ...}, pubDate: ...}}
                        
                        content = article.get('content', article) # Fallback to article itself
                        title = content.get('title', article.get('title', 'Unknown Title'))
                        
                        # Handle link extraction
                        link = article.get('link')
                        if not link:
                            canon_url = content.get('canonicalUrl', {})
                            if isinstance(canon_url, dict):
                                link = canon_url.get('url')
                        
                        # Handle date extraction
                        pub_time_str = "Unknown Date"
                        try:
                            if 'pubDate' in content:
                                # New format: "2025-12-18T18:14:12Z"
                                dt = datetime.fromisoformat(content['pubDate'].replace('Z', '+00:00'))
                                pub_time_str = dt.strftime('%Y-%m-%d %H:%M')
                            elif 'providerPublishTime' in article:
                                # Old format: timestamp
                                dt = datetime.fromtimestamp(article['providerPublishTime'])
                                pub_time_str = dt.strftime('%Y-%m-%d %H:%M')
                        except:
                            pass

                        provider = article.get('provider', {}).get('displayName', article.get('publisher', 'Unknown'))

                        with st.container(border=True):
                            if link:
                                st.markdown(f"**[{title}]({link})**")
                            else:
                                st.markdown(f"**{title}**")
                            st.caption(f"Published by {provider} at {pub_time_str}")
                else:
                    st.info("No recent news found for this ticker.")

        except Exception as e:
            # 6. Error Handling
            st.error(f"⚠️ Error: The ticker '{ticker_symbol}' could not be found or the market service is busy.")
            st.caption(f"Technical details: {str(e)}")

    else:
        st.info("Enter a ticker symbol in the sidebar to start the AI Market Analyst.")

if __name__ == "__main__":
    main()
