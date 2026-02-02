import os
from dotenv import load_dotenv
from app.database.supabase_client import SupabaseContextManager
from app.engine.generator import StrategicGenerator

load_dotenv()

db = SupabaseContextManager()
ai = StrategicGenerator()

USER_ID = "801e5aff-c41e-45bf-904f-bd1bc6bbcd17"

def run_test():
    print(f"--- Starting Pulse Check for User: {USER_ID} ---")
    
    # Test Step 1: Fetching
    context = db.fetch_user_context(USER_ID)
    
    # Add this IF check to stop the crash
    if context is None:
        print("❌ Pulse Check stopped: User context could not be loaded.")
        return

    print(f"✅ Context Fetched: {context['role']} in {context['industry']}")

    try:
        context = db.fetch_user_context(USER_ID)
        print(f"Context Fetch: {context['role']} in {context['industry']}")
        print(f"Current Focus: {context['current_focus']}")
    except Exception as e:
        print(f"Database Fetch Failed: {e}")

    
    try:
        print("Asking Gemini to strategize...")
        raw_response = ai.generate_publish_ready_posts(context)
        print("Gemini Response Received!")
        print("\n--- GENERATED CONTENT ---")
        print(raw_response)
    except Exception as e:
        print(f"Gemini Generation Failed: {e}")

if __name__ == "__main__":
    run_test()
