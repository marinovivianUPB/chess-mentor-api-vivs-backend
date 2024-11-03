import gradio as gr
from src.agent import MagnusAgent

agent = MagnusAgent().get_agent()

def agent_response(message, history):
    return agent.chat(message).response


if __name__ == "__main__":
    demo = gr.ChatInterface(agent_response, type="messages")
    demo.launch()
