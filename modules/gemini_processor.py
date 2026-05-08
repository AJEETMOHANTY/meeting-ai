import google.generativeai as genai
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

# configure api key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_final_json(summary_text):

    prompt = f"""
You are an AI meeting assistant.

Analyze the combined meeting summary and return ONLY valid JSON.

Return in this exact format:

{{
    "summary": "final meeting summary",
    "tasks": [
        {{
            "task": "task description",
            "owner": "person name",
            "status": "pending"
        }}
    ]
}}

Focus on:
- actionable tasks
- deadlines
- decisions
- assigned owners

Ignore:
- greetings
- jokes
- personal announcements
- celebrations

Meeting Summary:
{summary_text}
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(prompt)

        # return response.text

        # raw Gemini output
        raw_output = response.text.strip()

        print("Raw Gemini Output:")
        print(raw_output)

        # remove markdown wrappers if Gemini adds them
        cleaned_output = raw_output.replace("```json", "")
        cleaned_output = cleaned_output.replace("```", "")
        cleaned_output = cleaned_output.strip()

        print("Cleaned Gemini Output:")
        print(cleaned_output)

        return cleaned_output

    except Exception as e:
        print("Gemini API Error:", e)

        return """
        {
            "summary": "Final summary generation failed",
            "tasks": []
        }
        """