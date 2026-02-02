import os
from dotenv import load_dotenv
from supabase import create_client

# 1. Load keys
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# 2. Initialize Supabase Client
supabase = create_client(url, key)

# 3. Try to fetch something (Replace 'profiles' with your actual table name)
# We'll just fetch the first 1 row to test the link
try:
    response = supabase.table("onboarding_responses").select("*").execute()
    print("--- Supabase Connection Successful ---")
    print(f"Data Found: {response.data}")
except Exception as e:
    print(f"--- Connection Failed ---")
    print(e)