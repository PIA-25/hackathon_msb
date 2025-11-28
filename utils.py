from google import genai
from google.genai import types

import os
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


def save_video(client: genai.Client,
               video: types.Video,
               save_dir: str,
               local_download: bool = False) -> None:

    client.files.download(file=video)

    if local_download:
        # TODO: Decide to include "/" or not, between folder and file
        output_file_name = f"{save_dir}video_{datetime.today()}.mp4"
        video.save(path=output_file_name)

    print("Extended video saved!")

    # Optional
    # client.files.delete(name=uploaded_file.name)
    # print(f"Deleted the uploaded file: {uploaded_file.name}")


def create_ai_prompt(user_info: dict,
                     scenario_number: int,
                     extended: bool = False) -> str:

    strategy = user_info["strategy"]
    age = user_info["age"]
    gender = user_info["gender"]

    scenario_key = f"scenario_{scenario_number}"
    scenario_key += "_extended" if extended else ""

    with open("prompts.json", "r") as file:
        scenario = json.load(file)[scenario_key]

    # Base Cinematic Style for consistency
    BASE_STYLE = (
        scenario["base_prompt"]
        .replace("{age}", age)
        .replace("{gender}", gender)
    )

    # Context based on User's Choice
    if strategy == 'flee':
        ACTION_SCENE = (
            scenario["flee"]
            .replace("{age}", age)
            .replace("{gender}", gender)
        )
    else:  # stay
        ACTION_SCENE = (
            scenario["stay"]
            .replace("{age}", age)
            .replace("{gender}", gender)
        )

    # Narrative/Thematic Context
    THEME_CONTEXT = (
        scenario["theme_context"]
        .replace("{age}", age)
        .replace("{gender}", gender)
    )

    return f"{BASE_STYLE} {ACTION_SCENE} {THEME_CONTEXT}"
