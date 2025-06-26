from typing import List, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains import generation_chain, reflection_chain, GENERATION_PROMPT_FIRST

load_dotenv()

REFLECT = "reflect"
GENERATE = "generate"
graph = MessageGraph()


def generate_node(state):
    # Add system instructions to the first message if this is the initial generation
    if len(state) == 1:
        # First generation - add system instructions
        user_message = state[0].content
        system_instructions = GENERATION_PROMPT_FIRST

        enhanced_message = HumanMessage(
            content=f"{system_instructions}\n\nUser request: {user_message}"
        )
        result = generation_chain.invoke({"messages": [enhanced_message]})
    else:
        # Subsequent generations - use the current state
        result = generation_chain.invoke({"messages": state})

    # Extract the final message from the result
    if isinstance(result, dict) and "messages" in result:
        return result["messages"][-1:]
    elif hasattr(result, "messages"):
        return result.messages[-1:]
    else:
        return [result]


def reflect_node(state):
    # Get the last message content from the generation chain
    last_message = state[-1]
    if hasattr(last_message, "content"):
        last_content = last_message.content
    else:
        last_content = str(last_message)

    # Create a simple message for reflection
    reflection_input = [
        HumanMessage(content=f"Please critique this post: {last_content}")
    ]

    response = reflection_chain.invoke({"messages": reflection_input})

    # Return as a list containing the feedback message
    return [HumanMessage(content=f"Feedback: {response.content}")]


graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)
graph.set_entry_point(GENERATE)


def should_continue(state):
    if len(state) > 6:
        return END
    return REFLECT


graph.add_conditional_edges(GENERATE, should_continue)
graph.add_edge(REFLECT, GENERATE)

app = graph.compile()

print("🔄 LangGraph Reflection Agent")
print("📊 Graph Structure:")
print(app.get_graph().draw_mermaid())
print("\n" + "=" * 50)

print("🚀 Starting generation-reflection loop...")
response = app.invoke(
    HumanMessage(
        content="Latest news about NASA Artemis mission and its impact on space exploration."
    )
)

print("\n" + "=" * 50)
print("🎉 Final Result:")
if isinstance(response, list) and len(response) > 0:
    # Find the last non-feedback message (the final generated post)
    final_post = None
    for msg in reversed(response):
        if hasattr(msg, "content") and not msg.content.startswith("Feedback:"):
            final_post = msg.content
            break

    if final_post:
        print(f"📝 Final Post:\n{final_post}")
    else:
        print(f"📝 Last Message:\n{response[-1].content}")
else:
    print(f"📝 Response:\n{response}")
