# main.py
import os
from dotenv import load_dotenv
from app.services import TrendService

load_dotenv()

def run_sync():
    apify_token = os.getenv("APIFY_API_KEY")
    
    if not apify_token:
        print("Error: APIFY_API_TOKEN not found in environment.")
        return

    service = TrendService(api_token=apify_token)

    print("Starting Global Sync for all industries...")
    
    try:
        service.sync_all_industries()
        print("Sync completed successfully for all categories.")
    except Exception as e:
        print(f"Critical failure during sync: {e}")

if __name__ == "__main__":
    run_sync()