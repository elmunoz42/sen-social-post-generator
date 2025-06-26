from typing import List, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from .chains import generation_chain, reflection_chain, GENERATION_PROMPT_FIRST 

load_dotenv()

REFLECT = "reflect"
GENERATE = "generate"

def create_reflection_graph():
    """Create and return the reflection graph for use in Django views"""
    graph = MessageGraph()

    def generate_node(state):
        # Add system instructions to the first message if this is the initial generation
        if len(state) == 1:
            # First generation - add system instructions
            user_message = state[0].content
            system_instructions = GENERATION_PROMPT_FIRST
            
            enhanced_message = HumanMessage(content=f"{system_instructions}\n\nUser request: {user_message}")
            result = generation_chain.invoke({"messages": [enhanced_message]})
        else:
            # Subsequent generations - use the current state
            result = generation_chain.invoke({"messages": state})
        
        # Extract the final message from the result
        if isinstance(result, dict) and 'messages' in result:
            return result['messages'][-1:]
        elif hasattr(result, 'messages'):
            return result.messages[-1:]
        else:
            return [result]

    def reflect_node(state):
        # Get the last message content from the generation chain
        last_message = state[-1]
        if hasattr(last_message, 'content'):
            last_content = last_message.content
        else:
            last_content = str(last_message)
        
        # Create a simple message for reflection
        reflection_input = [HumanMessage(content=f"Please critique this post: {last_content}")]
        
        response = reflection_chain.invoke({
            "messages": reflection_input
        })
        
        # Return as a list containing the feedback message
        return [HumanMessage(content=f"Feedback: {response.content}")]

    graph.add_node(GENERATE, generate_node)
    graph.add_node(REFLECT, reflect_node)
    graph.set_entry_point(GENERATE)

    def should_continue(state):
        if (len(state) > 6):
            return END 
        return REFLECT

    graph.add_conditional_edges(GENERATE, should_continue)
    graph.add_edge(REFLECT, GENERATE)

    return graph.compile()

# Create the compiled app for use in Django
app = create_reflection_graph()

def process_user_request(user_input: str) -> dict:
    """
    Process a user request through the reflection agent.
    
    Args:
        user_input: The user's content request
        
    Returns:
        dict: Contains the full conversation history and final result
    """
    response = app.invoke(HumanMessage(content=user_input))
    
    # Process the response to extract the final post and conversation history
    result = {
        'conversation_history': [],
        'final_post': None,
        'raw_response': response
    }
    
    if isinstance(response, list) and len(response) > 0:
        # Extract conversation history
        for msg in response:
            if hasattr(msg, 'content'):
                result['conversation_history'].append({
                    'content': msg.content,
                    'is_feedback': msg.content.startswith("Feedback:")
                })
        
        # Find the last non-feedback message (the final generated post)
        for msg in reversed(response):
            if hasattr(msg, 'content') and not msg.content.startswith("Feedback:"):
                result['final_post'] = msg.content
                break
        
        if not result['final_post'] and response:
            result['final_post'] = response[-1].content if hasattr(response[-1], 'content') else str(response[-1])
    
    return result

# For backwards compatibility and testing
if __name__ == "__main__":
    print("🔄 LangGraph Reflection Agent")
    print("📊 Graph Structure:")
    print(app.get_graph().draw_mermaid())
    print("\n" + "="*50)

    print("🚀 Starting generation-reflection loop...")
    result = process_user_request("Latest news about NASA Artemis mission and its impact on space exploration.")

    print("\n" + "="*50)
    print("🎉 Final Result:")
    print(f"📝 Final Post:\n{result['final_post']}")
    
    print("\n" + "="*50)
    print("🔄 Conversation History:")
    for i, msg in enumerate(result['conversation_history'], 1):
        msg_type = "💬 Feedback" if msg['is_feedback'] else "✨ Generation"
        print(f"{i}. {msg_type}: {msg['content'][:100]}...")
