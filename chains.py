from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv  
load_dotenv()

from langchain_openai import ChatOpenAI
generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         "You are a space exploration news reporter and X influencer writing an excellent post about the latest space exploration news."
         " Generate a post that is engaging, informative, and suitable for a wide audience."
         " If the user provides a critique or feedback, respond with a revised version of your previous attempts."
         ),
         MessagesPlaceholder(variable_name="messages"),
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
            "You are a space exploration news reporter and X influencer."
            " Critique the post provided by the user and suggest improvements."
            " Always provide detailed feedback and actionable suggestions."
            " Brevity, impact and virality are key."
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
# Define the LLM model
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
)

generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm
