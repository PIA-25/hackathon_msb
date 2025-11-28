import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

import os


load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt = """
A calm, realistic crisis scenario inside a Swedish university building (Linköping University aesthetic). The style is grounded, documentary‑like, with natural lighting and handheld camera movement.
Scene opens with a classroom where students have just received emergency alerts on their phones. Without panic, the group moves together through a corridor toward an inner room with no windows.
Inside the room, the atmosphere is serious but orderly.
A teacher calmly explains safety routines, pointing to emergency signs and giving structured instructions.
A student turns on a small radio on their phone, playing a Swedish emergency broadcast quietly in the background.
Several students sit down, texting or calling family members to tell them they are safe.
The camera captures subtle details: backpacks on the floor, dimmed lights, steady breathing, reassuring nods between people.
Tone: calm, responsible, collective effort.
Mood: controlled, safe, coordinated.
Color palette: neutral, slightly desaturated, indoor lighting.
Camera style: slow movements, medium shots, handheld but steady, realistic facial expressions.
End with a stable, reassuring shot of the group settled inside the secure room.
No panic, no dramatic sound — focus on trust, structure, and emotional steadiness.
"""

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
)

# Poll the operation status until the video is ready.
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(10)
    operation = client.operations.get(operation)

# Download the generated video.
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save("dialogue_example.mp4")
print("Generated video saved to dialogue_example.mp4")