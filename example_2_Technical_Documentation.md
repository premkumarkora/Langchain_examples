# Technical Documentation - Example 2: Agentic Stock Analyst

## Architecture Overview
Follows an **Iterative Reasoning Loop**:
`Input` $\rightarrow$ `LLM Reasoning (Agent)` $\rightarrow$ `Dynamic Tool Selection` $\rightarrow$ `Recursive Execution` $\rightarrow$ `Natural Language Summary`.

## Tool-Centric Design
Individual capabilities are encapsulated using the `@tool` decorator. This allows the LLM to "see" the functions as documentation:
- **`get_stock_price`**: Targeted tool for real-time valuation.
- **`get_stock_news`**: Targeted tool for qualitative intelligence.

## Agent Logic & Prompting
The agent is initialized using the `langchain_classic` framework to ensure compatibility with existing environment constraints. The system prompt enforces a "Professional Stock Analyst" persona:
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional stock analyst worker."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
```

## UI & Session Management
Session state is maintained using a list of dictionaries:
```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```
On every rerun, the app iterates through this list to rebuild the chat history, which is also passed to the LLM to provide it with "short-term memory."

## Maintenance & Troubleshooting
- **API Changes**: `yfinance` internal structures frequently change. The code uses `.get()` method heavily to remain resilient.
- **Model Names**: The agent relies on `gpt-4.1-nano`. If model name errors occur, verify valid OpenAI model identifiers.
