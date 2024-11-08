import os
import json
from imgaug import augmenters as iaa
from PIL import Image
import numpy as np
def process_and_augment_images(input_folder, output_folder, num_augmentations):
    json_path = os.path.join(input_folder, 'annotations.coco.json')
    
    # Verifica se o arquivo JSON existe
    if not os.path.exists(json_path):
        print(f"Erro: O arquivo {json_path} não foi encontrado.")
        return
    
    # Tenta abrir o arquivo JSON
    try:
        with open(json_path, 'r') as json_file:
            coco_data = json.load(json_file)
    except OSError as e:
        print(f"Erro ao abrir o arquivo {json_path}: {e}")
        return

    # Cria a pasta de saída, se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    augmenter = iaa.SomeOf((1, 3), [
        iaa.GaussianBlur(sigma=(0, 1.0)),
        iaa.LinearContrast((0.75, 1.5)),
        iaa.AdditiveGaussianNoise(scale=(0, 0.05 * 255)),
        iaa.Multiply((0.8, 1.2)),
        iaa.Affine(rotate=(-25, 25))
    ], random_order=True)

    for image_info in coco_data["images"]:
        image_path = os.path.join(input_folder, image_info["file_name"])
        
        # Verifica se a imagem existe antes de tentar abri-la
        if not os.path.exists(image_path):
            print(f"Imagem {image_info['file_name']} não encontrada. Pulando...")
            continue
        
        image = Image.open(image_path)
        for i in range(num_augmentations):
            augmented_image = augmenter(image=np.array(image))
            output_image_path = os.path.join(output_folder, f"{os.path.splitext(image_info['file_name'])[0]}_aug_{i}.jpg")
            Image.fromarray(augmented_image).save(output_image_path)
            print(f"Imagem aumentada salva em: {output_image_path}")
