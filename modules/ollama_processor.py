import ollama


def chunk_text(text, chunk_size=4000):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])

    return chunks


def summarize_chunk(chunk):
    prompt = f"""
Summarize this meeting chunk clearly.

Focus on:
- decisions
- tasks
- deadlines
- owners

Ignore:
- greetings
- jokes
- personal announcements

Meeting chunk:
{chunk}
"""

    response = ollama.chat(
        model="llama3.1:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"] 


def process_large_transcript(transcript):
    
    chunks = chunk_text(transcript)

    summaries = []

    for chunk in chunks:
        print("Processing chunk...")

        summary = summarize_chunk(chunk)
        summaries.append(summary)

    combined_summary = "\n".join(summaries)

    return combined_summary