from faster_whisper import WhisperModel
import os


def transcribe_audio(audio_path):
    """
    Convert audio file → transcript text
    """

    # load whisper model
    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    # transcribe audio
    segments, info = model.transcribe(audio_path)

    transcript = ""

    # combine all segments
    for segment in segments:
        transcript += segment.text + " "

    return transcript