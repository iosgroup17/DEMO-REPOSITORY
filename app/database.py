import os
from supabase import create_client, Client
from dotenv import load_dotenv

class SupabaseContextManager:
    def __init__(self):
        load_dotenv()
        url = os.getenv("SUPABASE_URL", "").strip()
        key = os.getenv("SUPABASE_KEY", "").strip()
        
        if not url or not key:
            raise ValueError("Supabase URL or Key is missing from .env")
            
        self.supabase: Client = create_client(url, key)

    def fetch_user_context(self, user_id: str):
        target_id = user_id.strip()
        try:
            response = self.supabase.table("profiles").select("*").eq("id", target_id).execute()
            if not response.data:
                return None
            profile_data = response.data[0]
            
            res_onboarding = self.supabase.table("onboarding_responses").select("*").eq("user_id", target_id).execute()
            
            return self._map_to_context(res_onboarding.data, profile_data)
        except Exception as e:
            print(f"Supabase API Error: {str(e)}")
            return None
    
    def _map_to_context(self, responses, profile):
        def get_tags(idx):
            item = next((r for r in responses if r['step_index'] == idx), None)
            return item['selection_tags'] if item else []

        return {
            "display_name": profile.get("display_name", "Founder"),
            "short_bio": profile.get("short_bio", ""),
            "role": get_tags(0)[0] if get_tags(0) else "Professional",
            "current_focus": get_tags(1)[0] if get_tags(1) else "General Work",
            "industry": get_tags(2)[0] if get_tags(2) else "Technology",
            "goal": get_tags(3)[0] if get_tags(3) else "Growth",
            "formats": get_tags(4),
            "platforms": get_tags(5),
            "audience": get_tags(6)
        }