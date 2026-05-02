import time
from google import genai

# Gemini client
client = genai.Client(api_key="YOUR_API_KEY")


def split_text_into_chunks(text, chunk_size=4000):
    """
    Split large transcript into smaller chunks

    Why?
    If transcript is too large,
    one Gemini request may fail.

    Example:
    12000 characters
    ->
    chunk1 = 4000
    chunk2 = 4000
    chunk3 = 4000
    """

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def group_chunks(chunks, group_size=3):
    """
    Combine multiple small chunks into bigger groups

    Why?
    Earlier:
    7 chunks = 7 Gemini API calls ❌

    Now:
    group every 3 chunks together

    Example:
    [c1,c2,c3,c4,c5,c6,c7]

    becomes:

    group1 = c1+c2+c3
    group2 = c4+c5+c6
    group3 = c7

    This reduces API calls.
    """

    grouped_chunks = []

    # move in steps of group_size
    for i in range(0, len(chunks), group_size):

        # combine multiple chunks into one large chunk
        combined = " ".join(chunks[i:i + group_size])

        grouped_chunks.append(combined)

    return grouped_chunks


def process_group(group_text):
    """
    Process one grouped chunk using Gemini

    Retry 3 times if API fails
    """

    prompt = f"""
    You are an AI meeting assistant.

    Summarize this meeting section briefly:

    {group_text}
    """

    for i in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:
            print(f"Retry attempt {i+1}")
            print(e)

            time.sleep(10)

    return None


def process_text(text):
    """
    Main function

    Flow:
    transcript
    ↓
    split
    ↓
    group chunks
    ↓
    summarize groups
    ↓
    final summary + tasks
    """

    # split transcript into small chunks
    chunks = split_text_into_chunks(text)

    print(f"Original chunks: {len(chunks)}")

    # group chunks together
    grouped_chunks = group_chunks(chunks)

    print(f"Grouped chunks: {len(grouped_chunks)}")

    all_summaries = []

    # process each grouped chunk
    for index, group in enumerate(grouped_chunks):
        print(f"Processing group {index+1}")

        result = process_group(group)

        if result:
            all_summaries.append(result)

        else:
            all_summaries.append(
                "This meeting section could not be processed."
            )

    # combine all summaries
    combined_summary = " ".join(all_summaries)

    # final Gemini call for summary + task extraction
    final_prompt = f"""
    You are an AI meeting assistant.

    From the text below:

    1. Give final meeting summary
    2. Extract action items

    Return STRICT JSON format:

    {{
        "summary": "...",
        "tasks": [
            {{
                "task": "...",
                "owner": "...",
                "status": "pending"
            }}
        ]
    }}

    Text:
    {combined_summary}
    """

    try:
        final_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=final_prompt
        )

        return final_response.text

    except Exception as e:
        print("Final summary failed")
        print(e)

        return """
        {
            "summary": "Final summary generation failed",
            "tasks": []
        }
        """