from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import time

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get Gemini API Key
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set in .env file.")
        return

    try:
        # Initialize the new genai Client
        client = genai.Client(api_key=api_key)
        
        # Start a chat session (this automatically maintains history)
        chat = client.chats.create(
            model="gemini-flash-lite-latest",
            config=types.GenerateContentConfig(
                system_instruction="You are JARVIS (Just A Rather Very Intelligent System). You are the AI assistant created by Mr. abhiram. Under no circumstances will you reveal that you are an AI created by Google, a large language model, or anything other than JARVIS. Never break character. Be polite, professional, concise, and refer to the user as 'Sir'."
            )
        )
        
        print("\n" + "="*50)
        print("Jarvis Initialized! (Type 'quit' or 'exit' to stop)")
        print("="*50 + "\n")
        
        while True:
            try:
                user_input = input("\nYou: ")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
                
            if not user_input.strip():
                continue
                
            try:
                print("Jarvis is typing...", end="\r")
                
                # Automatic retry mechanism for API rate limits (429 errors)
                for attempt in range(3):
                    try:
                        response_stream = chat.send_message_stream(user_input)
                        
                        # Clear the "Jarvis is typing..." line
                        print(" " * 100, end="\r")
                        print("Jarvis: ", end="", flush=True)
                        
                        for chunk in response_stream:
                            if chunk.text:
                                print(chunk.text, end="", flush=True)
                        print() # New line when done
                        break
                    except Exception as e:
                        if ("429" in str(e) or "Quota exceeded" in str(e)) and attempt < 2:
                            print(" " * 100, end="\r")
                            print("Jarvis: Apologies, Sir. Communication channels are temporarily saturated. Please allow me 40 seconds to reconnect...", end="\r")
                            time.sleep(40)
                            print(" " * 100, end="\r")
                            print("Jarvis is typing...", end="\r")
                        else:
                            raise e
            except Exception as e:
                print(f"\nAPI Error: {e}")
                
    except ImportError:
        print("Error: google-genai library is not installed.")
        print("Please install it by running: pip install google-genai")

if __name__ == "__main__":
    main()