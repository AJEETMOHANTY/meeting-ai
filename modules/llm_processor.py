from google import genai   # New Gemini library
import time

# create client using API key
client = genai.Client(api_key="AIzaSyDpx17pu_MOI27TPyhYVik43TF59cAtBBk")

def process_text(text):
    # this function sends text to Gemini

    prompt = f"""
    You are a strict AI meeting parser.

    Your task:
    - Extract ONLY structured data
    - DO NOT behave like a chat assistant

    Instructions:
    - Return ONLY valid JSON
    - No explanation
    - No formatting
    - No headings
    - No markdown
    - No extra text
    - No suggestions
    - No rewriting
    - No multiple options

    If you add anything outside JSON, the output is WRONG.

    Output format (STRICT):

    {{
    "summary": "one single sentence summary",
    "tasks": [
        {{
        "task": "short task description",
        "owner": "person name or null",
        "status": "pending"
        }}
    ]
    }}

    Text:
    {text}
    """

     # try API call maximum 3 times
    for i in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )
            return response.text     # return immediately if success

        except Exception as e:
            print("Retrying...", i+1)
            time.sleep(5)


    # if all retries fail
    return """
    {
        "summary": "Failed to process meeting due to API issue",
        "tasks": []
    }
    """