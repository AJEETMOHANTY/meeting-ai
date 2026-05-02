import time
from google import genai

# Gemini client
client = genai.Client(api_key="YOUR_API_KEY")


def split_text_into_chunks(text, chunk_size=4000):
    """
    Split large transcript into smaller chunks

    text -> full transcript
    chunk_size -> max characters per chunk
    """

    chunks = []

    # split text into smaller parts
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def process_single_chunk(chunk):
    """
    Process one chunk
    Retry 3 times if API fails
    """

    prompt = f"""
    You are an AI meeting assistant.

    Summarize this meeting chunk briefly:

    {chunk}
    """

    # retry this chunk 3 times
    for i in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as e:
            print(f"Retrying chunk attempt {i+1}")
            time.sleep(5)

    # if all retries fail
    return None


def process_text(text):
    """
    Main function:
    handles chunking + failed chunk retry
    """

    # split transcript
    chunks = split_text_into_chunks(text)

    all_summaries = []
    failed_chunks = []

    print(f"Total chunks created: {len(chunks)}")

    # -------------------------
    # First round processing
    # -------------------------
    for index, chunk in enumerate(chunks):
        print(f"Processing chunk {index+1}")

        result = process_single_chunk(chunk)

        if result:
            all_summaries.append(result)

        else:
            print(f"Chunk {index+1} failed")
            failed_chunks.append(chunk)

    # -------------------------
    # Retry failed chunks again
    # -------------------------
    if failed_chunks:
        print("Retrying failed chunks again...")

    retry_failed_chunks = []

    for index, chunk in enumerate(failed_chunks):
        print(f"Retrying failed chunk {index+1}")

        result = process_single_chunk(chunk)

        if result:
            all_summaries.append(result)

        else:
            retry_failed_chunks.append(chunk)

    # -------------------------
    # Final fallback
    # -------------------------
    for chunk in retry_failed_chunks:
        all_summaries.append(
            "Some part of meeting could not be processed."
        )

    # combine all summaries
    combined_summary = " ".join(all_summaries)

    # final prompt for summary + task extraction
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

    # final Gemini call
    try:
        final_response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=final_prompt
        )

        return final_response.text

    except Exception:
        return """
        {
            "summary": "Final summary generation failed",
            "tasks": []
        }
        """