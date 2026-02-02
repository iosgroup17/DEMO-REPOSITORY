import os
from dotenv import load_dotenv
from app.services import TrendService

load_dotenv()
token = os.getenv("APIFY_API_KEY")

print(f"🔍 Token loaded in test1.py: {bool(token)}")

if token:
    service = TrendService(api_token=token)
    print("🚀 Running Phase 1 Sync...")
    service.sync_to_dummy()
    print("✅ Check your Supabase 'dummy_trending_topics' table!")