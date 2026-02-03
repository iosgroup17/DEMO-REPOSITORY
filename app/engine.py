import os
import json
from google import genai
from google.genai import types

class StrategicGenerator:
    def __init__(self):
        # Gemini 2.5 Flash for high-speed, real-time generation
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-2.5-flash" 

    def generate_personalized_feed(self, context: dict, trends: list):
        """Phase 2: Generates 6 posts with full context and DB-ready keys."""
        trend_text = "\n".join([f"- {t['topic_name']}: {t['short_description']}" for t in trends])

        prompt = f"""
        Act as a premier social media ghostwriter for {context['display_name']}.
        
        <identity_context>
        - Role: {context['role']} in {context['industry']}
        - Short Bio: {context['short_bio']}
        - Current Focus: {context['current_focus']}
        - Strategic Goal: {context['goal']}
        </identity_context>
        
        <audience_targeting>
        - Target Audience: {', '.join(context['audience'])}
        - Content Platforms: {', '.join(context['platforms'])}
        - Content Style: {', '.join(context['formats'])}
        </audience_targeting>

        <trending_now>
        {trend_text}
        </trending_now>

        TASK:
        Generate 6 distinct content ideas. Use the Global Trends as hooks but solve the specific problems of the Industry and Audience listed above.
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                # STRICT SCHEMA: Matches publish_ready_posts table
                response_schema={
                    "type": "object",
                    "properties": {
                        "posts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "post_heading": {"type": "string", "description": "The title or headline of the post."},
                                    "platform_icon": {"type": "string", "enum": ["icon-x", "icon-instagram", "icon-linkedin"]},
                                    "caption": {"type": "string", "description": "The full body text of the post."},
                                    "hashtags": {"type": "array", "items": {"type": "string"}},
                                    "prediction_text": {"type": "string", "description": "Why this content will perform well for this specific audience."}
                                },
                                "required": ["post_heading", "platform_icon", "caption", "hashtags", "prediction_text"]
                            }
                        }
                    }
                }
            )
        )
        return json.loads(response.text).get("posts", [])
    
    def generate_trend_deep_dive(self, trend: dict, context: dict):
        """
        Phase 3: Deep analysis when a user clicks a specific trend card.
        """
        prompt = f"""
        Analyze this trend for a {context['role']}:
        Trend: {trend['topic_name']} - {trend['short_description']}
        
        Task: 
        1. Explain why this matters to their brand.
        2. Generate 4 publish-ready templates (The Contrarian, The Educator, The Visionary, The Connector).
        
        Return as JSON.
        """
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)