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

    def fetch_user_context(self, user_id: str):
        try:
            profile_res = self.supabase.table("profiles").select("*").eq("id", user_id).execute()
            if not profile_res.data:
                return None
            onboard_res = self.supabase.table("onboarding_responses").select("*").eq("user_id", user_id).execute()
            return self._map_to_context(profile_res.data[0], onboard_res.data)
        except Exception as e:
            print(f"Database Error: {e}")
            return None

    def _map_to_context(self, profile, responses):
        def get_tags(index):
            match = next((r for r in responses if r.get("step_index") == index), None)
            return match.get("selection_tags", []) if match else []

        return {
            "display_name": profile.get("display_name", "User"),
            "short_bio": profile.get("short_bio", ""),
            "role": get_tags(0)[0] if get_tags(0) else "Professional",
            "current_focus": get_tags(1)[0] if get_tags(1) else "General",
            "industry": get_tags(2)[0] if get_tags(2) else "Technology",
            "goal": get_tags(3)[0] if get_tags(3) else "Growth",
            "formats": get_tags(4),
            "platforms": get_tags(5),
            "audience": get_tags(6)
        }
    
    def fetch_top_trends(self, limit: int = 5):
        try:
            response = self.supabase.table("dummy_trending_topics") \
                .select("*") \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            return response.data
        except Exception as e:
            print(f"Trend Fetch Error: {e}")
            return []