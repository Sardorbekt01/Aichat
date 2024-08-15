# controllers/tts_controller.py
import openai
from config import settings

openai.api_key = settings.TTS_TOKEN

async def generate_tts(text):
    response = openai.Completion.create(
        model="text-to-speech",
        prompt=text,
        voice="en_us",
        output_format="mp3"
    )
    audio_content = response['choices'][0]['audio']
    return audio_content
