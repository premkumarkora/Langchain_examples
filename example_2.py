import streamlit as st
import yfinance as yf
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# 1. Page Configuration
st.set_page_config(page_title="Agentic Stock Analyst", page_icon="🤖", layout="wide")

st.title("AI Agent - Stock Price & News")
st.caption("powered by LangChain Agents & GPT-4o-mini")

# --- TOOL DEFINITIONS ---

@tool
def get_stock_price(ticker: str) -> str:
    """
    Fetches the real-time current price of a stock ticker.
    Use this when the user asks for the price or current value of a stock.
    """
    try:
        t = yf.Ticker(ticker)
        f_info = t.fast_info
        price = f_info.get('lastPrice') or f_info.get('regularMarketPrice')
        currency = f_info.get('currency', 'USD')
        if price:
            return f"The current price of {ticker.upper()} is {price:.2f} {currency}."
        return f"Could not find price data for {ticker}."
    except Exception as e:
        return f"Error fetching price for {ticker}: {str(e)}"

@tool
def get_stock_news(ticker: str) -> str:
    """
    Fetches the 3 most recent news articles for a stock ticker.
    Use this when the user asks for news, updates, or recent events for a company.
    """
    try:
        t = yf.Ticker(ticker)
        news_feed = t.news[:3]
        if not news_feed:
            return f"No recent news found for {ticker}."
        
        results = []
        for article in news_feed:
            content = article.get('content', article)
            title = content.get('title', article.get('title', 'Unknown Title'))
            link = article.get('link') or content.get('canonicalUrl', {}).get('url', '#')
            results.append(f"- {title} (Link: {link})")
            
        return f"Recent news for {ticker.upper()}:\n" + "\n".join(results)
    except Exception as e:
        return f"Error fetching news for {ticker}: {str(e)}"

tools = [get_stock_price, get_stock_news]

# --- AGENT INITIALIZATION ---

def get_agent_executor():
    # Model: Using gpt-4o-mini as requested (referred to as gpt-4.1-mini in request)
    llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
    
    # Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional stock analyst worker. Be concise and provide links where available."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    # Create the executor
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- STREAMLIT UI & PERSISTENCE ---

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt_input := st.chat_input("Ask me about a stock (e.g., 'What is the price of NVDA and show me news')"):
    # Add user message to UI and state
    with st.chat_message("user"):
        st.markdown(prompt_input)
    st.session_state.messages.append({"role": "user", "content": prompt_input})

    # Run the Agent
    with st.chat_message("assistant"):
        with st.spinner("Analyzing market data..."):
            try:
                executor = get_agent_executor()
                
                # Convert session history to LangChain format
                chat_history = []
                for m in st.session_state.messages[:-1]: # exclude latest
                    if m["role"] == "user":
                        chat_history.append(HumanMessage(content=m["content"]))
                    else:
                        chat_history.append(AIMessage(content=m["content"]))
                
                response = executor.invoke({
                    "input": prompt_input,
                    "chat_history": chat_history
                })
                
                full_response = response["output"]
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Agent Error: {str(e)}")
