import os
from google import genai
from google.genai import types # Import for structured output

class StrategicGenerator:
    def __init__(self):
        # Gemini 2.5 Flash is highly efficient for high-throughput tasks
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-2.5-flash" 

    def generate_publish_ready_posts(self, context: dict, trends: list):
        # Convert trends list to a readable string for the prompt
        trend_text = "\n".join([f"- {t['title']}: {t['snippet']}" for t in trends])

        prompt = f"""
        Act as a premier social media ghostwriter for a {context['role']}.
        
        <context>
        Bio: {context['short_bio']}
        Current Focus: {context['current_focus']}
        Industry: {context['industry']}
        Goal: {context['goal']}
        </context>
        
        <trending_now>
        {trend_text}
        </trending_now>

        TASK:
        Generate 3 distinct, high-impact posts for {', '.join(context['platforms'])}.
        The target audience is: {', '.join(context['audience'])}.
        Style: Use {', '.join(context['formats'])}.
        
        STRATEGY:
        Anchoring: Every post MUST reference or be inspired by one of the 'trending_now' topics.
        """

        # Gemini 2.5 supports 'response_mime_type' for guaranteed JSON
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                # Define the exact schema your iOS app expects
                response_schema={
                    "type": "object",
                    "properties": {
                        "posts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "platform": {"type": "string"},
                                    "content": {"type": "string"},
                                    "hashtags": {"type": "array", "items": {"type": "string"}},
                                    "trend_ref": {"type": "string"},
                                    "predicted_score_reason": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            )
        )
        return response.text
    
    def generate_trend_deep_dive(self, trend: dict, context: dict):
        prompt = f"""
        Analyze this trend for a {context['role']}:
        Trend: {trend['topic_name']} - {trend['short_description']}
        
        Task: 
        1. Explain why this matters to their brand.
        2. Generate 4 publish-ready templates (The Contrarian, The Educator, The Visionary, The Connector).
        
        Return as JSON matching the 'publish_ready_posts' schema.
        """
        # Gemini 2.5 Flash handles this reasoning in <1s
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return response.text