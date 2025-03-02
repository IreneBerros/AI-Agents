import os 
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

class AnalyzeEmailToolSchema(BaseModel):
    email_text: str = Field(default="", description="The input email text to be processed.")

llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            azure_deployment="gpt-4o"
        )
    
def analyze_email(email_text):
    """Single GPT call to analyze sentiment, category, and urgency at once."""

    prompt = f"""
    Analyze the following email and provide structured output:

    Email:
    {email_text}

    Return a JSON response with:
    - Sentiment: (Positive, Neutral, Negative)
    - Category: (e.g., Billing Issue, Sales Inquiry, Support Request)
    - Urgency: (Low, Medium, High)
    """

    analysis_result = llm.invoke(prompt)

    return analysis_result.content





