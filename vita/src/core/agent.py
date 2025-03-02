import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph
from langchain.tools.base import StructuredTool
from langgraph.prebuilt import tools_condition

from src.states.state import State
from src.nodes.tools_node import tool_node
from src.tools.email_analyzer import AnalyzeEmailToolSchema, analyze_email

load_dotenv()

class Agent:
    def __init__(self): 
        """Initialize the agent with LLM and tools."""
        self.llm = self._initialize_llm()
        self.tools = self._initialize_tools()
        self.graph = self._initialize_graph()

    def _initialize_llm(self):
        """Create and return the Azure OpenAI LLM."""
        return AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            azure_deployment="gpt-4o"
        )
    
    def _initialize_tools(self): 
        """Define tools and bind them to the LLM."""
        analyze_email_tool = StructuredTool(
            name="email_analyzer",
            description="Analyze email text to extract sentiment, category and urgency.",
            args_schema=AnalyzeEmailToolSchema,
            func=analyze_email
        )
        return [analyze_email_tool]
    
    def _initialize_graph(self):
        """Create the LangGraph workflow."""
        graph_builder = StateGraph(State)

        # Bind tools to LLM
        self.llm = self.llm.bind_tools(tools=self.tools)

        # Nodes
        graph_builder.add_node("chatbot", self._chatbot)
        graph_builder.add_node("tools", tool_node(tools=self.tools))

        # Edges
        graph_builder.set_entry_point("chatbot")
        graph_builder.add_conditional_edges(
            source="chatbot",
            path=tools_condition
        )
        graph_builder.set_finish_point("chatbot")

        return graph_builder.compile()

    def _chatbot(self, state: State):
        """Node function for the chatbot interaction."""
        return {"messages": [self.llm.invoke(state["messages"])]}
    
    def invoke(self, input_messages:list):
        """Invoke the graph with a given input."""
        response = self.graph.invoke(input={"messages": input_messages})
        return response['messages'][-1].content
    


