import gradio as gr
from smolagents import CodeAgent, InferenceClientModel
from smolagents.mcp_client import MCPClient
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("HF_API_KEY")

try:
    mcp_client = MCPClient(
        {"url": "http://localhost:8050/sse"}
    )
    tools = mcp_client.get_tools()

    model = InferenceClientModel(api_key=api_key)
    agent = CodeAgent(tools=[*tools], model=model)

    demo = gr.ChatInterface(
        fn=lambda message, history: str(agent.run(message)),
        type="messages",
        examples=["greet me my name is wilsen"],
        title="Agent with MCP Tools",
        description="This is a simple agent that uses MCP tools to answer questions.",
    )

    demo.launch()
finally:
    mcp_client.close()
