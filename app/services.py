# app/services.py
import os
from apify_client import ApifyClient
from app.database import SupabaseContextManager

class TrendService:
    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError("❌ No Apify Token provided.")
        self.client = ApifyClient(api_token)
        self.db = SupabaseContextManager()

    def sync_to_dummy(self, search_query: str = "AI SaaS trends 2026"):
        run_input = { "search": search_query, "maxItems": 5 }
        print(f"📡 Requesting real-time trends for: {search_query}")
        
        run = self.client.actor("manju4k/social-media-trend-scraper-6-in-1-ai-analysis").call(run_input=run_input)
        
        test_data = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            # 🔍 PROBE: Try every key the Actor might use
            topic_name = (
                item.get("trend_name") or 
                item.get("name") or 
                item.get("hashtag") or 
                item.get("title") or 
                item.get("topic")
            )
            
            if topic_name:
                test_data.append({
                    "topic_name": topic_name,
                    "short_description": item.get("description") or item.get("snippet") or f"Hot topic on {item.get('platform', 'social media')}",
                    "platform_icon": "bolt.horizontal.circle.fill",
                    "hashtags": item.get("hashtags") or [],
                    "sector": "Technology"
                })
            else:
                # DEBUG: If it still fails, print the item keys to see what's inside
                print(f"⚠️ Item skipped. Available keys were: {list(item.keys())}")
        
        if test_data:
            print(f"💾 Found {len(test_data)} valid trends. Syncing to dummy table...")
            return self.db.supabase.table("dummy_trending_topics").insert(test_data).execute()
        else:
            print("❌ No valid trend data found. Check the 'Item skipped' debug prints above.")
            return None