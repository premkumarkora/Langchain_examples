# Requirements - Example 1: Specialized AI Worker

## Goal
To provide a simple, reliable interface for fetching real-time market data without complex reasoning overhead.

## Functional Requirements
- **Sidebar Input**: Must provide a text input field for the company ticker symbol (e.g., NVDA, MSFT).
- **Manual Trigger**: Data fetching must only occur when the user clicks the "Fetch Stock price & News" button.
- **Price Retrieval**: Fetch the most recent trading price, day high, day low, and currency from `yfinance`.
- **News Retrieval**: Fetch the top 3 most recent news articles for the specified ticker.
- **Dynamic Metrics**: Display the current price and its daily change (delta) using Streamlit metrics.
- **Error Handling**: Gracefully handle invalid ticker symbols or API failures with a user-friendly error message.
- **Empty Initial State**: The application must not auto-load data on startup.

## Non-Functional Requirements
- **Speed**: Use the `fast_info` attribute of `yfinance` for low-latency metric retrieval.
- **Robustness**: Implement fallback logic for missing data fields (e.g., fallback from `lastPrice` to `regularMarketPrice`).
- **UI Consistency**: Maintain a modern, wide-layout design with professional typography.
