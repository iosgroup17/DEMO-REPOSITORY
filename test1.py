import os
from dotenv import load_dotenv, find_dotenv

# Sanity Check
load_dotenv(find_dotenv())
token = os.getenv("APIFY_API_TOKEN")
print(f"🔍 Environment Check: Token found? {bool(token)}")

from app.services.trend_sync import TestTrendSync

try:
    sync_engine = TestTrendSync()
    print("🚀 Starting Phase 1 Dummy Test...")
    result = sync_engine.sync_to_dummy(test_label="initial-validation")
    
    if result and result.data:
        print(f"✅ Sync Complete. Inserted {len(result.data)} rows.")
    else:
        print("❌ Sync failed to insert data.")
except Exception as e:
    print(f"💥 Test Failed: {e}")