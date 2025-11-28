from google import genai
from google.genai import types
from dotenv import load_dotenv

import os
import time
from datetime import datetime


load_dotenv()


def make_vid_from_prompt(client: genai.Client,
                         prompt: str,
                         local_download: bool = False):

    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
    )

    while not operation.done:
        print("Waiting for video generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)

    generated_video: types.Video = operation.response.generated_videos[0].video
    video_uri = generated_video.uri

    # Download to Google
    client.files.download(file=generated_video)

    if local_download:
        # Download to local computer
        generated_video.save(f"video_{datetime.today()}.mp4")

    return video_uri


if __name__ == "__main__":
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = """
    
    """

    make_vid_from_prompt(client, prompt)
