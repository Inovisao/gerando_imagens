import os
import numpy as np
from PIL import Image
import imgaug.augmenters as iaa

def process_and_save_images(input_folder, output_folder, num_augmented_images=5):
    # Verifica se a pasta de saída existe, senão cria
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Pergunta ao usuário quais tipos de processamento ele deseja aplicar
    apply_fliplr = input("Deseja incluir o espelhamento horizontal no processamento? (s/n): ").lower() == 's'
    apply_flipud = input("Deseja incluir o espelhamento vertical no processamento? (s/n): ").lower() == 's'
    apply_crop = input("Deseja incluir corte aleatório no processamento? (s/n): ").lower() == 's'
    apply_rotate = input("Deseja incluir rotação aleatória no processamento? (s/n): ").lower() == 's'
    apply_noise = input("Deseja incluir ruído gaussiano no processamento? (s/n): ").lower() == 's'
    apply_brightness = input("Deseja incluir alteração de brilho no processamento? (s/n): ").lower() == 's'
    apply_blur = input("Deseja incluir desfoque gaussiano no processamento? (s/n): ").lower() == 's'
    apply_contrast = input("Deseja incluir alteração de contraste no processamento? (s/n): ").lower() == 's'
    apply_color = input("Deseja incluir alteração de matiz e saturação no processamento? (s/n): ").lower() == 's'
    apply_perspective = input("Deseja incluir transformação de perspectiva no processamento? (s/n): ").lower() == 's'
    apply_invert = input("Deseja incluir inversão de cores no processamento? (s/n): ").lower() == 's'
    apply_resize = input("Deseja incluir redimensionamento aleatório no processamento? (s/n): ").lower() == 's'

    # Define um pipeline de aumentação com base nas escolhas do usuário
    augmenters = []
    if apply_fliplr:
        augmenters.append(iaa.Fliplr(0.5))
    if apply_flipud:
        augmenters.append(iaa.Flipud(0.3))
    if apply_crop:
        augmenters.append(iaa.Crop(percent=(0, 0.1)))
    if apply_rotate:
        augmenters.append(iaa.Affine(rotate=(-25, 25)))
    if apply_noise:
        augmenters.append(iaa.AdditiveGaussianNoise(scale=(0, 0.05 * 255)))
    if apply_brightness:
        augmenters.append(iaa.Multiply((0.8, 1.2)))
    if apply_blur:
        augmenters.append(iaa.GaussianBlur(sigma=(0, 3.0)))
    if apply_contrast:
        augmenters.append(iaa.LinearContrast((0.75, 1.5)))
    if apply_color:
        augmenters.append(iaa.AddToHueAndSaturation((-20, 20)))
    if apply_perspective:
        augmenters.append(iaa.PerspectiveTransform(scale=(0.01, 0.1)))
    if apply_invert:
        augmenters.append(iaa.Invert(0.1, per_channel=True))
    if apply_resize:
        augmenters.append(iaa.Resize((0.9, 1.1)))

    augmenter = iaa.Sequential(augmenters)

    # Itera sobre todas as imagens na pasta de entrada
    for image_filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, image_filename)
        
        # Verifica se é realmente um arquivo de imagem
        if not os.path.isfile(image_path) or not image_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        image = np.array(Image.open(image_path))

        # Gera e salva as imagens aumentadas
        for i in range(num_augmented_images):
            augmented_image = augmenter(image=image)
            output_path = os.path.join(output_folder, f"{os.path.splitext(image_filename)[0]}_augmented_{i + 1}.jpg")
            Image.fromarray(augmented_image).save(output_path)
            print(f"Imagem salva em: {output_path}")

