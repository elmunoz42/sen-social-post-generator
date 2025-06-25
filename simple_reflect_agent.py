from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from chains import generation_chain, reflection_chain

load_dotenv()

def simple_generation_reflection_loop(user_input: str, max_iterations: int = 3):
    """
    Simple generation-reflection loop without complex graph setup
    """
    current_post = None
    
    for i in range(max_iterations):
        print(f"\n--- Iteration {i+1} ---")
        
        if i == 0:
            # First generation with system instructions
            print("🤖 Generating initial post...")
            system_message = ("You are a space exploration news reporter and X influencer writing an excellent post about the latest space exploration news. "
                            "Use the search tool to find the latest space exploration news and the time tool to get current date/time for context. "
                            "Generate a post that is engaging, informative, and suitable for a wide audience. "
                            "Always search for current information before generating your post.")
            
            result = generation_chain.invoke({"messages": [
                HumanMessage(content=f"{system_message}\n\nUser request: {user_input}")
            ]})
        else:
            # Subsequent generations with feedback
            print("🤖 Generating improved post based on feedback...")
            system_message = ("You are a space exploration news reporter and X influencer. "
                            "Use the search tool if you need updated information and the time tool for current date/time. "
                            "Generate an improved post based on the feedback provided.")
            
            feedback_message = f"{system_message}\n\nHere's the previous post: {current_post}\n\nHere's the feedback: {reflection_result.content}\n\nPlease generate an improved version."
            result = generation_chain.invoke({"messages": [HumanMessage(content=feedback_message)]})
        
        # Extract the final message content
        if isinstance(result, dict) and 'messages' in result:
            current_post = result['messages'][-1].content
        elif hasattr(result, 'messages') and result.messages:
            current_post = result.messages[-1].content
        elif isinstance(result, list) and len(result) > 0:
            current_post = result[-1].content
        else:
            current_post = str(result)
        
        print(f"📝 Generated Post:\n{current_post}")
        
        # Get reflection
        if i < max_iterations - 1:  # Don't reflect on the last iteration
            print("\n🧠 Getting feedback...")
            reflection_result = reflection_chain.invoke({
                "messages": [HumanMessage(content=f"Please critique this post: {current_post}")]
            })
            print(f"💭 Feedback:\n{reflection_result.content}")
    
    return current_post

if __name__ == "__main__":
    final_post = simple_generation_reflection_loop(
        "Latest news about NASA Artemis mission and its impact on space exploration."
    )
    
    print(f"\n🎉 Final Post:\n{final_post}")
