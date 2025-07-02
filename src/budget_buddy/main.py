# 📁 main.py

from langchain_core.messages import HumanMessage

from src.budget_buddy.core.config import settings, validate_settings
from src.budget_buddy.service import process_message, load_conversation, save_conversation, print_memory_status
from src.budget_buddy.database import engine
from src.budget_buddy.models import Transaction

def init_database():
    """Initialize database and create tables."""
    try:
        # Import Base here to avoid circular imports
        from src.budget_buddy.database import Base
        Base.metadata.create_all(bind=engine)
        print("🗄️ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        if settings["DEBUG"]:
            import traceback
            traceback.print_exc()

def main():
    """Main entry point for the Budget Buddy application."""
    
    # Validate configuration
    validate_settings()
    
    # Initialize database
    init_database()
    
    print("🤖 Budget Buddy Ready! (Type 'exit' to quit)")
    print(f"📱 {settings['APP_NAME']} v{settings['APP_VERSION']}")
    print(f"🌍 Environment: {settings['ENVIRONMENT']}")
    
    # Check memory status
    print_memory_status()
    print("-" * 50)

    # Load existing conversation history
    message_history = load_conversation()

    # Chat loop
    try:
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    break

                message_history.append(HumanMessage(content=user_input))

                # Process the message through the agent
                response = process_message(message_history)

                # Update full history
                message_history = response["messages"]

                # Show assistant's last reply
                print("Assistant:", message_history[-1].content)
                print("-" * 50)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                if settings["DEBUG"]:
                    import traceback
                    traceback.print_exc()
    
    finally:
        # Save conversation before exiting
        if message_history:
            save_conversation(message_history)
        
        print("👋 Goodbye! Thanks for using Budget Buddy!")

if __name__ == "__main__":
    main() 