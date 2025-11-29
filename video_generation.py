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
                       local_download_folder: str | None = None):

    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            resolution="720p",
            duration_seconds=8
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

    if local_download_folder:
        # Download to local computer
        todays_datetime = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        generated_video.save(f"{local_download_folder}base_video_{todays_datetime}.mp4")

    video_info = {
        "video": generated_video,
        "uri": video_uri,
        "video_bytes": video_bytes,
        "locally_downloaded": True if local_download_folder else False,
        "duration_seconds": 8
    }

    return video_info


def generate_extended_video(client: genai.Client,
                            prompt: str,
                            base_video: types.Video,
                            local_download_folder: str | None = None):

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

    if local_download_folder:
        # Download to local computer
        todays_datetime = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        generated_extended_video.save(f"{local_download_folder}extended_video_{todays_datetime}.mp4")

    video_info = {
        "video": generated_extended_video,
        "uri": video_uri,
        "video_bytes": video_bytes,
        "locally_downloaded": True if local_download_folder else False
    }

    return video_info


def get_video(user_info: dict,
              scenario_number: int,
              video_folder: str | None = None):

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    base_prompt = create_ai_prompt(
        user_info=user_info,
        scenario_number=scenario_number
    )

    extended_prompt = create_ai_prompt(
        user_info=user_info,
        scenario_number=scenario_number,
        extended=True
    )

    base_vid_info = generate_first_vid(
        client,
        base_prompt,
        video_folder
    )
    ext_vid_info = generate_extended_video(
        client,
        extended_prompt,
        base_vid_info["video"],
        video_folder
    )

    client.close()

    print(base_vid_info["uri"])
    print(ext_vid_info["uri"])

    ext_vid_info["pause_at_seconds"] = base_vid_info["duration_seconds"]

    return ext_vid_info


if __name__ == "__main__":

    video_folder = "videos/"

    user_info = {
        "strategy": "flee",
        "age": "40",
        "gender": "male",
        # Maybe unused
        "leadership_style": "",
        "occupation": "",
        "priority": "",
        "team_role": "",
        "risk_tolerance": ""
    }

    scenario_number = 1

    video = get_video(
        user_info,
        scenario_number,
        video_folder
    )

    # taktisk, logisk, lojal, omtänksam, riskbenägen, försiktig, pragmatisk, moralisk
