from google import genai
from google.genai import types
from dotenv import load_dotenv

import os

from utils import create_ai_prompt, save_video_locally, poll_video


load_dotenv()


def _generate_video(client: genai.Client,
                   base_prompt: str,
                   ext_prompt: str,
                   local_download_folder: str | None = None) -> dict:

    base_video_duration = 8  # seconds

    # Generate base video
    base_operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=base_prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            resolution="720p",
            duration_seconds=base_video_duration
        )
    )
    generated_base_video: types.Video = poll_video(base_operation)

    # Generate extended video
    ext_operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        video=generated_base_video,
        prompt=ext_prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            resolution="720p"
        )
    )
    generated_extended_video: types.Video = poll_video(ext_operation)

    # Download video to Google
    video_bytes = client.files.download(file=generated_extended_video)

    if local_download_folder:
        save_video_locally(generated_extended_video, local_download_folder)

    video_info = {
        "video_bytes": video_bytes,
        "uri": generated_extended_video.uri,
        "locally_downloaded": True if local_download_folder else False,
        "pause_at_seconds": base_video_duration
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

    video_info = _generate_video(
        client,
        base_prompt,
        extended_prompt,
        video_folder
    )

    client.close()

    return video_info


if __name__ == "__main__":

    video_folder = "videos/"

    user_info = {
        "strategy": "stay",
        "age": "21",
        "gender": "male",
        # Maybe unused
        "leadership_style": "",
        "occupation": "",
        "priority": "",
        "team_role": "",
        "risk_tolerance": ""
    }

    scenario_number = 2

    for i in range(2):
        video = get_video(
            user_info,
            i+1,
            video_folder
        )

        #print(video["video_bytes"])
        print(video["uri"])
        print(video["locally_downloaded"])
        print(video["pause_at_seconds"])

    # taktisk, logisk, lojal, omtänksam, riskbenägen, försiktig, pragmatisk, moralisk

    #import base64
    #source = f"data:video/mp4;base64,{base64.b64encode(video["video_bytes"]).decode()}"
