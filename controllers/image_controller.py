import openai
from config import settings

openai.api_key = settings.IMAGE_TOKEN

async def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']
