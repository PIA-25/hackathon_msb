from google import genai
from google.genai import types
from google.genai.errors import ClientError

import os
import time
from datetime import datetime
import json


def load_in_local_video(client: genai.Client,
                        video_path: str) -> types.Video:

    uploaded_file = client.files.upload(
        file=video_path
    )

    video = types.Video(
        uri=uploaded_file.uri
    )

    return video


def load_in_video_from_uri(video_uri: str) -> types.Video:
    video = types.Video(
        uri=video_uri
    )

    return video



def poll_video(client: genai.Client,
               operation: types.GenerateVideosOperation,
               poll_interval: int = 10,
               rate_limit_delay: int = 60) -> types.Video:

    while True:
        try:
            while not operation.done:

                print("Waiting for video generation to complete...")
                time.sleep(poll_interval)
                operation = client.operations.get(operation)

            print("Finished generating video!")
            return operation.response.generated_videos[0].video

        except ClientError:
            print("Rate limit hit — waiting 60s...")
            time.sleep(rate_limit_delay)


def save_video_locally(video: types.Video,
                       save_dir: str) -> None:

    os.makedirs(save_dir, exist_ok=True)

    todays_datetime = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")

    save_dir += "/" if not save_dir.endswith("/") else ""
    output_file_name = f"{save_dir}video_{todays_datetime}.mp4"

    video.save(path=output_file_name)

    print("Video saved!")


def create_ai_prompt(user_info: dict,
                     scenario_number: int,
                     extended: bool = False) -> str:

    age = user_info["age"]
    gender = user_info["gender"]

    scenario_key = f"scenario_{scenario_number}"

    if extended:
        prompt_type = "ext_prompt"
    else:
        prompt_type = "base_prompt"

    with open("prompts.json", "r") as file:
        scenario = json.load(file)[scenario_key]

    prompt = (
        scenario[prompt_type]
        .replace("{age}", age)
        .replace("{gender}", gender)
    )

    return f"{prompt}"
