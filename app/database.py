import os
from supabase import create_client, Client
from dotenv import load_dotenv

class SupabaseContextManager:
    def __init__(self):
        load_dotenv()
        url = os.getenv("SUPABASE_URL", "").strip()
        key = os.getenv("SUPABASE_KEY", "").strip()
        if not url or not key:
            raise ValueError("Supabase credentials missing in .env")
        self.supabase: Client = create_client(url, key)

    def fetch_top_trends(self, limit: int = 10):
        try:
            response = self.supabase.table("trending_topics") \
                .select("*") \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            return response.data
        except Exception as e:
            print(f"Fetch Error: {e}")
            return []

    def push_new_trends(self, trends: list):
        """Saves cleaned trends from Gemini/Apify into Supabase."""
        try:
            if not trends: return
            return self.supabase.table("trending_topics").insert(trends).execute()
        except Exception as e:
            print(f"Database Insert Error: {e}")

    def push_user_suggestions(self, suggestions: list):
        """Inserts exactly 2 suggestions per day into Supabase."""
        try:
            return self.supabase.table("user_suggestions").insert(suggestions).execute()
        except Exception as e:
            print(f"Error inserting suggestions: {e}")