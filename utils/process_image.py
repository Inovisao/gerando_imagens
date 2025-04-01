import os
import json
from imgaug import augmenters as iaa
from PIL import Image
import numpy as np

def process_and_augment_images(input_folder, output_folder, num_augmentations):
    json_path = os.path.join(input_folder, 'annotations.coco.json')
    output_json_path = os.path.join(output_folder, 'annotations.coco.json')
    
    # Verifica se o arquivo JSON existe
    if not os.path.exists(json_path):
        print(f"Erro: O arquivo {json_path} não foi encontrado. Certifique-se de que o arquivo annotations.coco.json existe na pasta de entrada.")
        return

    # Tenta abrir o arquivo JSON
    try:
        with open(json_path, 'r') as json_file:
            coco_data = json.load(json_file)
            annotation_id = max([ann['id'] for ann in coco_data['annotations']], default=0) + 1
            image_id = max([img['id'] for img in coco_data['images']], default=0) + 1
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

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        
        # Verifica se a imagem existe antes de tentar abri-la
        if not os.path.exists(image_path):
            print(f"Imagem {image_file} não encontrada. Pulando...")
            continue
        
        image = Image.open(image_path)
        for i in range(num_augmentations):
            augmented_image = augmenter(image=np.array(image))
            augmented_image = Image.fromarray(augmented_image)
            output_image_path = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}_aug_{i}.jpg")
            augmented_image.save(output_image_path)
            print(f"Imagem aumentada salva em: {output_image_path}")

            # Adiciona os metadados da imagem ao JSON COCO
            coco_data["images"].append({
                "id": image_id,
                "file_name": f"{os.path.splitext(image_file)[0]}_aug_{i}.jpg",
                "height": image.height,
                "width": image.width
            })
            coco_data["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": 1,
                "bbox": [0, 0, image.width, image.height],
                "area": image.width * image.height,
                "iscrowd": 0
            })
            annotation_id += 1
            image_id += 1

    # Salva o arquivo JSON no formato COCO
    with open(output_json_path, 'w') as json_file:
        json.dump(coco_data, json_file, indent=4)

    print(f"\nProcessamento concluído. Imagens aumentadas salvas em: {output_folder}")
