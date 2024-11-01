import os
import numpy as np
from PIL import Image
import imgaug.augmenters as iaa
from insering_background import load_images_from_folder, inpaint_with_background

def process_and_save_images(image_folder, background_folder, output_folder, num_augmented_images):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Carregar imagens e backgrounds
    images = load_images_from_folder(image_folder)
    backgrounds = load_images_from_folder(background_folder)

    for image_path in images:
        image = np.array(Image.open(image_path))

        augmenter = iaa.Sequential([
            iaa.Fliplr(0.5),
            iaa.Crop(percent=(0, 0.1)),
            iaa.Affine(rotate=(-25, 25)),
            iaa.AdditiveGaussianNoise(scale=(0, 0.05 * 255)),
            iaa.Multiply((0.8, 1.2))
        ])

        for i in range(num_augmented_images):
            # Escolher um fundo aleatório
            background_path = np.random.choice(backgrounds)
            background = Image.open(background_path)

            # Criar uma máscara binária para o inpainting (onde branco é a área a ser preenchida)
            mask = Image.new("L", (image.shape[1], image.shape[0]), 255)

            # Aplicar aumentos e inpainting
            augmented_image = augmenter(image=image)
            inpainted_image = inpaint_with_background(augmented_image, background, mask)

            # Salvar a imagem resultante
            output_path = os.path.join(output_folder, f"inpainted_image_{i + 1}_{os.path.basename(image_path)}")
            Image.fromarray(inpainted_image).save(output_path)
            print(f"Imagem salva em: {output_path}")