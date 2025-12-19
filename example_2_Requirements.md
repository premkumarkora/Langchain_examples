# Requirements - Example 2: Agentic Stock Analyst

## Goal
To demonstrate advanced AI reasoning where the system autonomously decides which tools to call based on natural language intent.

## Functional Requirements
- **Chat Interface**: Use a modern, persistent chat input (`st.chat_input`) instead of static sidebar forms.
- **Tool-Based Execution**: Rewrite core logic into reusable "tools" (`get_stock_price`, `get_stock_news`).
- **Reasoning Loop**: Integrate a LangChain agent using a high-performance LLM (`gpt-4.1-nano`) to orchestrate tool calls.
- **Multi-Intent Handling**: Successfully parse and execute compound queries (e.g., "Tell me the price of TSLA and the latest news").
- **Conversation Memory**: Persist chat history within the session (`st.session_state`) allowing the agent to remember context.
- **Transparent Logic**: Enable verbose logging to the terminal so the "thought process" can be demonstrated.

## Non-Functional Requirements
- **Scalability**: Decouple the data retrieval (Tools) from the reasoning (Agent) for easy future tool expansion.
- **Context Management**: Limit tool outputs (e.g., truncate news descriptions) to stay within LLM token constraints.
- **Persistence**: Ensure the UI does not clear previous messages when new inputs are processed.
