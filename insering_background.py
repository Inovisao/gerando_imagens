import os
import numpy as np
from PIL import Image
import imgaug.augmenters as iaa
from diffusers import StableDiffusionInpaintPipeline
import torch



def load_images_from_folder(folder_path):
    image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not image_paths:
        raise ValueError(f"A pasta '{folder_path}' não contém imagens válidas.")
    return image_paths

def inpaint_with_background(image, background, mask):
    pipe = StableDiffusionInpaintPipeline.from_pretrained("runwayml/stable-diffusion-inpainting", torch_dtype=torch.float16)
    pipe = pipe.to("cuda") if torch.cuda.is_available() else pipe.to("cpu")

    image = Image.fromarray(image).resize((512, 512))
    background = background.resize((512, 512))
    mask = mask.resize((512, 512))

    inpainted_image = pipe(prompt="",
                           init_image=background,
                           mask_image=mask).images[0]
    return np.array(inpainted_image)