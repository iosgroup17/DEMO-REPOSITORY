import os
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, HTTPException
from app.database import SupabaseContextManager
from app.engine import StrategicGenerator
from app.services import TrendService

app = FastAPI(title="Prosper Content Engine")
db = SupabaseContextManager()
ai = StrategicGenerator()
trend_sync = TrendService(api_token=os.getenv("APIFY_API_KEY"))

@app.get("/discover/{user_id}")
async def get_unified_discover_feed(user_id: str):
    user_context = db.fetch_user_context(user_id)
    if not user_context:
        raise HTTPException(status_code=404, detail="User profile not found")

    trends = db.fetch_top_trends(limit=5)
    
    # Logic to determine if Apify sync is needed
    should_sync = False
    if not trends:
        should_sync = True
    else:
        # Parse Supabase timestamp and compare to current UTC time
        last_sync = datetime.fromisoformat(trends[0]['created_at'].replace('Z', '+00:00'))
        if datetime.now(timezone.utc) - last_sync > timedelta(hours=6):
            should_sync = True

    if should_sync:
        print("Trends stale or missing. Triggering Apify sync...")
        query = f"{user_context['industry']} trends 2026"
        trend_sync.sync_to_dummy(query=query)
        trends = db.fetch_top_trends(limit=5)

    personalized_posts = ai.generate_personalized_feed(user_context, trends)

    return {
        "user_identity": user_context,
        "trending_row": trends,
        "recommended_row": personalized_posts
    }

@app.post("/save-post/{user_id}")
async def save_selected_post(user_id: str, post_data: dict):
    try:
        payload = {
            "user_id": user_id,
            "post_heading": post_data.get("post_heading"),
            "platform_icon": post_data.get("platform_icon"),
            "caption": post_data.get("caption"),
            "hashtags": post_data.get("hashtags"),
            "prediction_text": post_data.get("prediction_text")
        }
        result = db.supabase.table("publish_ready_posts").insert(payload).execute()
        return {"status": "success", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))