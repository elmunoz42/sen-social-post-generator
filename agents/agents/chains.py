from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()
from .tools import search_tool, get_system_time

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Define the LLM model
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
)

# Create tools list
tools = [search_tool, get_system_time]

# Create the generation agent with tools using LangGraph (no custom prompt)
# The agent will use its default prompt and we'll add instructions via system message
generation_chain = create_react_agent(llm, tools)

GENERATION_PROMPT_FIRST = """You are a space exploration news reporter and X influencer writing an excellent post about the latest space exploration news. Use the search tool to find the latest space exploration news and the time tool to get current date/time for context. Generate a post that is engaging, informative, and suitable for a wide audience. Always search for current information before generating your post."""

GENERATION_PROMPT_ADJUSTMENTS = """You are a space exploration news reporter and X influencer. Use the search tool if you need updated information and the time tool for current date/time. Generate an improved post based on the feedback provided."""

# Reflection prompt for critique
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a space exploration news reporter and X influencer."
            " Critique the post provided by the user and suggest improvements."
            " Always provide detailed feedback and actionable suggestions."
            " Brevity, impact and virality are key.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Keep reflection chain simple (no tools needed for critique)
reflection_chain = reflection_prompt | llm
