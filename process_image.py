import os
import json
from imgaug import augmenters as iaa
from PIL import Image
import numpy as np

def process_and_augment_images(input_folder, output_folder, num_augmentations):
    json_path = os.path.join(input_folder, 'annotations.coco.json')
    
    # Verifica se o arquivo JSON existe
    if not os.path.exists(json_path):
        print(f"Erro: O arquivo {json_path} não foi encontrado. Criando um novo arquivo.")
        coco_data = {
            "info": {"year": "2024", "version": "2"},
            "licenses": [{"id": 1, "name": "CC BY 4.0"}],
            "categories": [{"id": 1, "name": "insect"}],
            "images": [],
            "annotations": []
        }
    else:
        # Tenta abrir o arquivo JSON
        try:
            with open(json_path, 'r') as json_file:
                coco_data = json.load(json_file)
        except OSError as e:
            print(f"Erro ao abrir o arquivo {json_path}: {e}")
            return

    # Verifica se há imagens no diretório de entrada
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print(f"Erro: Nenhuma imagem encontrada no diretório {input_folder}.")
        return

    # Cria a pasta de saída, se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    augmenter = iaa.Sequential([
        iaa.Multiply((0.9, 1.1)),  # Ajuste de multiplicação de cores
        iaa.MultiplyBrightness((0.9, 1.1)),  # Ajuste de iluminação
        iaa.LinearContrast((0.8, 1.2)),  # Ajuste de contraste
        iaa.AddToHueAndSaturation((-10, 10)),  # Ajuste de saturação
        iaa.AddToBrightness((-10, 10)),  # Ajuste de brilho
        iaa.GammaContrast((0.9, 1.1)),  # Ajuste de contraste gamma
        iaa.SigmoidContrast(gain=(5, 7), cutoff=(0.45, 0.55)),  # Ajuste de contraste sigmoidal
        iaa.LogContrast(gain=(0.9, 1.1)),  # Ajuste de contraste logarítmico
        iaa.CLAHE(clip_limit=(1, 2)),  # Equalização de histograma adaptativa
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
            augmented_image = Image.fromarray(augmented_image)
            output_image_path = os.path.join(output_folder, f"{os.path.splitext(image_info['file_name'])[0]}_aug_{i}.jpg")
            augmented_image.save(output_image_path)
            print(f"Imagem aumentada salva em: {output_image_path}")

    # Salva o arquivo JSON no formato COCO
    with open(json_path, 'w') as json_file:
        json.dump(coco_data, json_file, indent=4)

