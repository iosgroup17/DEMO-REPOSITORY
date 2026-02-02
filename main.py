from fastapi import FastAPI, HTTPException
from app.database.supabase_client import SupabaseContextManager
from app.engine.generator import StrategicGenerator
from app.engine.trend_service import TrendService
import uvicorn

app = FastAPI(title="Prosper Content Engine")

# Initialize core components once
db = SupabaseContextManager()
ai = StrategicGenerator()

trends_api  = TrendService()

@app.get("/generate/{user_id}")
async def generate_content(user_id: str):
    # 1. Fetch cached trends for Row 1 (Fast)
    trending_row = db.supabase.table("trending_topics").select("*").limit(5).execute().data
    
    # 2. Fetch User Context for Row 2
    context = db.fetch_user_context(user_id)
    
    # 3. Generate 5-6 Recommended Posts (Real-time)
    # This is NOT saved to the DB yet.
    recommended_row = ai.generate_home_screen_posts(context)
    
    return {
        "trending_topics": trending_row,
        "recommended_posts": recommended_row
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)