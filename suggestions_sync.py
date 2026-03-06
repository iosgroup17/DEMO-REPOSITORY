import os
from dotenv import load_dotenv
from app.services import TrendService
from app.database import SupabaseContextManager

load_dotenv()

def run_suggestion_sync():
    service = TrendService(api_token=os.getenv("APIFY_API_KEY"))
    db = SupabaseContextManager()
    
    print("Starting Daily Smart Suggestions Sync...")
    
    try:
        # 1. Fetch all users who need suggestions
        # Note: You'll need to fetch user_id and their industry from your profiles table
        users = db.supabase.table("onboarding_responses").select("user_id, selection_tags").eq("step_index", 2).execute().data
        
        for user in users:
            user_id = user['user_id']
            # Get the first industry tag selected during onboarding
            industry = user['selection_tags'][0] if user['selection_tags'] else "General"
            
            print(f"Generating 2 suggestions for User {user_id} in {industry}...")
            service.generate_daily_suggestions(user_id, industry)
            
        print("Successfully updated all user suggestions.")
    except Exception as e:
        print(f"Suggestion Sync Failure: {e}")

if __name__ == "__main__":
    run_suggestion_sync()