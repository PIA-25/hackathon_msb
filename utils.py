from google import genai
from google.genai import types

import os
from datetime import datetime


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


def create_ai_prompt(user_info: dict) -> str:
    strategy = user_info["strategy"]
    age = user_info["age"]
    gender = user_info["gender"]

    # Base Cinematic Style for consistency
    BASE_STYLE = "A low-angle, shaky, handheld camera shot of a dark, smoke-filled, destroyed city street at dawn. Cinematic, high contrast, photo-realistic."

    # Context based on User's Choice
    if strategy == 'flee':
        ACTION_SCENE = (
            f"The scene focuses on a {age}-year-old {gender} desperately running towards a crowded checkpoint. "
            f"They carry a small backpack and look over their shoulder in panic. "
            f"The shot should emphasize the chaos and urgency of evacuation. "
            f"Show other civilians climbing into a military-style vehicle."
        )
    else:  # fight
        ACTION_SCENE = (
            f"The scene follows a determined {age}-year-old {gender} wearing a tactical vest. "
            f"They are crouching behind rubble, aiming a rifle. "
            f"The shot should focus on their intense concentration and the defensive posture, "
            f"with dust and debris swirling around. A comrade waves them forward."
        )

    # Narrative/Thematic Context
    THEME_CONTEXT = (
        "The audio should feature distant thunderous explosions, followed by immediate silence. "
        "The clip must maintain a consistent camera shake to convey realism."
    )

    return f"{BASE_STYLE} {ACTION_SCENE} {THEME_CONTEXT}"
