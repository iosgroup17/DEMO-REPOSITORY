import os
from dotenv import load_dotenv, find_dotenv
from apify_client import ApifyClient
from app.database.supabase_client import SupabaseContextManager

class TestTrendSync:
    def __init__(self):
        # Explicitly find and load the .env file
        env_path = find_dotenv()
        load_dotenv(env_path)
        
        token = os.getenv("APIFY_API_TOKEN")
        
        # Rigorous validation to prevent empty/malformed tokens
        if not token or not token.startswith("apify_api_"):
            print(f"❌ DEBUG: Invalid Token Found at {env_path}")
            raise ValueError("APIFY_API_TOKEN is missing or malformed in .env")
            
        self.client = ApifyClient(token)
        self.db = SupabaseContextManager()

    def sync_to_dummy(self, test_label: str = "v1-alpha"):
        """Fetches trends and populates the dummy_trending_topics table."""
        run_input = {
            "search": "AI SaaS, startup tech trends 2026",
            "maxItems": 5
        }
        
        print(f"📡 Calling Apify Actor (Jv27ie6FT7KAkRWes)...")
        # Ensure the actor ID matches the 'Social Media Trend Scraper'
        run = self.client.actor("Jv27ie6FT7KAkRWes").call(run_input=run_input)
        
        test_data = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            test_data.append({
                "topic_name": item.get("title") or item.get("trend_name") or "Global Trend",
                "short_description": item.get("description") or item.get("snippet") or "",
                "platform_icon": "bolt.horizontal.circle.fill",
                "hashtags": item.get("hashtags") or [],
                "sector": "Technology"
            })
        
        if not test_data:
            print("⚠️ No trends found in the dataset.")
            return None

        print(f"💾 Inserting {len(test_data)} items into dummy_trending_topics...")
        return self.db.supabase.table("dummy_trending_topics").insert(test_data).execute()