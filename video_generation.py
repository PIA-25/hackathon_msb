from google import genai
from google.genai import types
from dotenv import load_dotenv

import os
import time
from datetime import datetime

from utils import save_video


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

    print(video_uri)

    # Download to Google
    video_bytes = client.files.download(file=generated_video)

    if local_download:
        # Download to local computer
        generated_video.save(f"base_video_{datetime.today()}.mp4")

    video_info = {
        "uri": video_uri,
        "locally_downloaded": local_download,
        "video_bytes": video_bytes,
        "video": generated_video
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

    print(video_uri)

    # Download to Google
    video_bytes = client.files.download(file=generated_extended_video)

    if local_download:
        # Download to local computer
        generated_extended_video.save(f"extended_video_{datetime.today()}.mp4")

    video_info = {
        "uri": video_uri,
        "locally_downloaded": local_download,
        "video_bytes": video_bytes,
        "video": generated_extended_video
    }

    return video_info


if __name__ == "__main__":
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = """

    """

    video_info = generate_first_vid(client, prompt)

    base_vid_info = generate_first_vid(client, prompt, True)
    ext_vid_info = generate_extended_video(client, prompt, base_vid_info["video"], True)

    client.close()
