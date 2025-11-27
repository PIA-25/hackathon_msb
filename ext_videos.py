import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

import os


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


VIDEO_NAME = "video0.mp4"
VIDEO_DIR = "videos/"
VIDEO_PATH = f"{VIDEO_DIR}{VIDEO_NAME}"

#print(f"Uploading file: {VIDEO_PATH}...")
#uploaded_file = client.files.upload(file=VIDEO_PATH)
#(f"File uploaded successfully. URI: {uploaded_file.uri}")
video = types.Video.from_file(location=VIDEO_PATH)

file = client.files.get(name="files/od3vuqvf6gs9")

#operation: GenerateVideosOperation = None

prompt = """
Följ den unge mannen ut ur klassrumsdörren. Den unge mannen och resten av klassen ska sedan
föras till ett skyddsrum. Rektorn ska säga att dom måste stanna kvar där till vidare.
Det här ska vara en len övergång från den första videon.
"""

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    #video=operation.response.generated_videos[0].video, # This must be a video from a previous generation
    #video=uploaded_file.video_metadata,
    video=types.Video(
        uri=file.uri
    ),
    prompt=prompt,
    config=types.GenerateVideosConfig(
        number_of_videos=1,
        resolution="720p"
    ),
)

# Poll the operation status until the video is ready.
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(10)
    operation = client.operations.get(operation)

if operation.result and operation.result.generated_videos:
    extended_video = operation.result.generated_videos[0]

    output_file_name = f"{VIDEO_DIR}extended_{VIDEO_NAME}"
    client.files.download(file=extended_video.video)
    extended_video.video.save(path=output_file_name)
    print("Extended video saved!")

    # Optional
    #client.files.delete(name=uploaded_file.name)
    #print(f"Deleted the uploaded file: {uploaded_file.name}")

client.close()
