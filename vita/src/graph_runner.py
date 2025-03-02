from src.core.agent import Agent

def run_email_analysis(email_text):
    """Executes the compiled LangGraph pipeline."""
    agent = Agent()
    response = agent.invoke([email_text])  
    return response