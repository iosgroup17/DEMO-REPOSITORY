import os
from google import genai

class StrategicGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def generate_publish_ready_posts(self, context: dict):
        prompt = f"""
        Act as a premier social media ghostwriter for a {context['role']}.
        
        CONTEXT:
        - Bio: {context['short_bio']}
        - Current Focus: {context['current_focus']} (This is what they are doing right now)
        - Industry: {context['industry']}
        - Goal: {context['goal']}
        
        TASK:
        Generate 3 distinct, high-impact posts for {', '.join(context['platforms'])}.
        The target audience is: {', '.join(context['audience'])}.
        Style: Use {', '.join(context['formats'])}.
        
        OUTPUT FORMAT:
        Return ONLY a JSON object with a key "posts" containing a list of objects.
        Each object must have: "platform", "content", "hashtags", and "predicted_score_reason".
        """
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text