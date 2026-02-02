# app/services/test_sync.py
from apify_client import ApifyClient
from app.database.supabase_client import SupabaseContextManager
import os

class TestTrendSync:
    def __init__(self):
        self.client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
        self.db = SupabaseContextManager()

    def sync_to_dummy(self, test_label: str = "v1-alpha"):
        # Scrape data using the 6-in-1 Actor
        run_input = {
            "platforms": [
                "instagram",
                "twitter",
                "linkedIn"
            ],
            "region": "india",
            "timeRange": "4h",
            "maxTrends": 10
        }
        run = self.client.actor("Jv27ie6FT7KAkRWes").call(run_input=run_input)
        
        test_data = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            test_data.append({
                "topic_name": item.get("title", "Test Topic"),
                "short_description": item.get("description", "No description provided"),
                "platform_icon": "testtube.2.fill", # Distinct SF Symbol for testing
                "hashtags": item.get("hashtags", []),
                "sector": "Testing",
                "test_run_id": test_label
            })
        
        # Insert into the DUMMY table
        return self.db.supabase.table("dummy_trending_topics").insert(test_data).execute()