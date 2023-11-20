import re
from openai import OpenAI
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled


def extract_youtube_video_id(url: str) -> str | None:
    """Extracts YouTube video ID from the given URL."""
    match = re.search(r"(?:youtu\.be\/|watch\?v=)([\w-]+)", url)
    if match:
        return match.group(1)
    return None

def get_video_transcript(video_id: str) -> str | None:
    """Gets the transcript of a YouTube video by its ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except TranscriptsDisabled:
        print(f"Transcripts are disabled for this video: {video_id}")
        return None
    except Exception as e:
        print(f"An error occurred while fetching transcript: {e}")
        return None

    text = " ".join([line["text"] for line in transcript])
    return text

def generate_summary(text: str) -> str:
    """Generates a summary using OpenAI GPT-3.5-turbo model."""
    client = OpenAI()
    system_message = "Please summarize the provided text in bullet points"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": text}
        ],
        temperature=0.2,
        n=1,
        max_tokens=200,
        presence_penalty=0,
        frequency_penalty=0.1,
    )
    return response.choices[0].message.content.strip()

def summarize_youtube_video(video_url: str) -> str:
    """Summarizes a YouTube video using its URL."""
    video_id = extract_youtube_video_id(video_url)
    if not video_id:
        return f"Invalid YouTube URL: {video_url}"

    transcript = get_video_transcript(video_id)
    if not transcript:
        return f"No English transcript found for this video: {video_url}"
    load_dotenv()
    summary = generate_summary(transcript)
    return summary

if __name__ == '__main__':
    youtube_url = "https://www.youtube.com/watch?v=J-3zlPVQJqc&t=14s"
    result = summarize_youtube_video(youtube_url)
    print(result)
