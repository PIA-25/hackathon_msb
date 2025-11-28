from google import genai
from google.genai import types
from dotenv import load_dotenv

import os
import time
from datetime import datetime

from utils import create_ai_prompt


load_dotenv()


def generate_first_vid(client: genai.Client,
                       prompt: str,
                       local_download: bool = False):

    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            resolution="720p"
        )
    )

    while not operation.done:
        print("Waiting for video generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)

    generated_video: types.Video = operation.response.generated_videos[0].video
    video_uri = generated_video.uri

    # Download to Google
    video_bytes = client.files.download(file=generated_video)

    if local_download:
        # Download to local computer
        generated_video.save(f"base_video_{datetime.today()}.mp4")

    video_info = {
        "video": generated_video,
        "uri": video_uri,
        "video_bytes": video_bytes,
        "locally_downloaded": local_download
    }

    return video_info


def generate_extended_video(client: genai.Client,
                            prompt: str,
                            base_video: types.Video,
                            local_download: bool = False):

    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        video=base_video,
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            resolution="720p"
        )
    )

    while not operation.done:
        print("Waiting for video generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)

    generated_extended_video: types.Video = operation.response.generated_videos[0].video
    video_uri = generated_extended_video.uri

    # Download to Google
    video_bytes = client.files.download(file=generated_extended_video)

    if local_download:
        # Download to local computer
        generated_extended_video.save(f"extended_video_{datetime.today()}.mp4")

    video_info = {
        "video": generated_extended_video,
        "uri": video_uri,
        "video_bytes": video_bytes,
        "locally_downloaded": local_download,
    }

    return video_info


if __name__ == "__main__":

    user_info = {
        "strategy": "flee",
        "age": 26,
        "gender": "male"
    }

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    base_prompt = create_ai_prompt(
        user_info=user_info,
        scenario_number=1
    )

    extended_prompt = create_ai_prompt(
        user_info=user_info,
        scenario_number=1,
        extended=True
    )

    base_vid_info = generate_first_vid(
        client,
        base_prompt,
        True
    )
    ext_vid_info = generate_extended_video(
        client,
        extended_prompt,
        base_vid_info["video"],
        True
    )

    client.close()
