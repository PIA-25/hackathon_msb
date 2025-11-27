import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

import os


load_dotenv()


def generate_video(client, prompt, extended_from_vid=None):
    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        video=extended_from_vid if extended_from_vid else None,
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            resolution="720p"
        ),
    )

    return operation


def save_video(client, operation, save_dir):
    extended_video = operation.result.generated_videos[0]

    output_file_name = f"{save_dir}extended_video.mp4"
    client.files.download(file=extended_video.video)
    extended_video.video.save(path=output_file_name)
    print("Extended video saved!")

    # Optional
    # client.files.delete(name=uploaded_file.name)
    # print(f"Deleted the uploaded file: {uploaded_file.name}")


def main(video_path, save_dir, prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # uploaded_file = client.files.upload(file=VIDEO_PATH)
    #video = types.Video.from_file(location=video_path)

    file = client.files.get(name="files/w1kv924hqo8d")

    operation = generate_video(client, prompt, extended_from_vid=None)
    #operation = generate_video(client, prompt, extended_from_vid=types.Video(uri=file.uri))

    # Poll the operation status until the video is ready.
    while not operation.done:
        print("Waiting for video generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)

    if operation.result and operation.result.generated_videos:
        save_video(client, operation, save_dir)

    client.close()


if __name__ == "__main__":
    # Optional (if you want the generated vid to extend of an existing vid)
    VIDEO_PATH = "videos/video0.mp4"
    SAVE_DIR = "videos/"

    # The prompt to give to the AI
    prompt = """
    Följ den unge mannen ut ur klassrumsdörren. Den unge mannen och resten av klassen ska sedan
    föras till ett skyddsrum. Rektorn ska säga att dom måste stanna kvar där till vidare.
    Det här ska vara en len övergång från den första videon.
    """

    main(
        prompt=prompt,
        save_dir=SAVE_DIR,
        video_path=VIDEO_PATH,
    )
