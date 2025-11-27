import time
from google import genai
from google.genai import types

client = genai.Client()

dress_image = ""
glasses_image = ""
woman_image = ""

prompt = ("The video opens with a medium, eye-level shot of a beautiful woman with dark hair "
          "and warm brown eyes. She wears a magnificent, high-fashion flamingo dress with layers "
          "of pink and fuchsia feathers, complemented by whimsical pink, heart-shaped sunglasses. "
          "She walks with serene confidence through the crystal-clear, shallow turquoise water of "
          "a sun-drenched lagoon. The camera slowly pulls back to a medium-wide shot, revealing "
          "the breathtaking scene as the dress's long train glides and floats gracefully on the "
          "water's surface behind her. The cinematic, dreamlike atmosphere is enhanced by the "
          "vibrant colors of the dress against the serene, minimalist landscape, capturing a "
          "moment of pure elegance and high-fashion fantasy.")

dress_reference = types.VideoGenerationReferenceImage(
  image=dress_image, # Generated separately with Nano Banana
  reference_type="asset"
)

glasses_reference = types.VideoGenerationReferenceImage(
  image=glasses_image, # Generated separately with Nano Banana
  reference_type="asset"
)

woman_reference = types.VideoGenerationReferenceImage(
  image=woman_image, # Generated separately with Nano Banana
  reference_type="asset"
)

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    config=types.GenerateVideosConfig(
      reference_images=[dress_reference, glasses_reference, woman_reference],
    ),
)

# Poll the operation status until the video is ready.
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(10)
    operation = client.operations.get(operation)

# Download the video.
video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("veo3.1_with_reference_images.mp4")
print("Generated video saved to veo3.1_with_reference_images.mp4")