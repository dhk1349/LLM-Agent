from llm_executor import LLMExecutor
import os

def main():
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Please set your OPENAI_API_KEY environment variable")
        return
    
    # Initialize the LLM Executor
    executor = LLMExecutor(api_key)
    
    print("👋 Hi! I'm your AI assistant. I can help you with calculations, visualizations, text analysis, and more.")
    print("What would you like to explore today? (Type 'quit' to exit)")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == 'quit':
                print("\nGoodbye! Have a great day! 👋")
                break
            if not user_input:
                continue
                
            response = executor.process_user_input(user_input)
            print("\nAssistant:", response)
            
        except Exception as e:
            print(f"\nOops! Something went wrong: {str(e)}")
            print("Let's try something else!")

if __name__ == "__main__":
    main() 