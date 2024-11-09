import os
import json
import random
from PIL import Image
from datetime import datetime
from remove_background import remove_background_from_directory

def inpainting_with_annotations(background_folder, original_datasets_folder, output_folder, insects_per_image):
    # Remove background from insect images
    remove_background_from_directory(original_datasets_folder)
    
    # Cria a pasta de saída, se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Configuração inicial para o arquivo JSON no formato COCO
    json_path = os.path.join(output_folder, 'annotations.coco.json')
    if not os.path.exists(json_path):
        coco_data = {
            "info": {"year": "2024", "version": "2"},
            "licenses": [{"id": 1, "name": "CC BY 4.0"}],
            "categories": [{"id": 1, "name": "insect"}],
            "images": [],
            "annotations": []
        }
    else:
        with open(json_path, 'r') as json_file:
            coco_data = json.load(json_file)

    # Carrega as imagens de fundo e as imagens de insetos com fundo removido
    
    background_images = [f for f in os.listdir(background_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not background_images:
        print(f"Erro: Nenhuma imagem encontrada no diretório {background_images}.")
        return
    
    insect_images = [f for f in os.listdir(original_datasets_folder) if f.startswith('no_bg_') and f.endswith(('.png', '.jpg', '.jpeg'))]
    if not insect_images:
        print(f"Erro: Nenhuma imagem encontrada no diretório {insect_images}.")
        return

    annotation_id = len(coco_data["annotations"]) + 1
    image_id = len(coco_data["images"]) + 1
    for background_filename in background_images:
        background_path = os.path.join(background_folder, background_filename)
        background = Image.open(background_path).convert("RGBA")
        bg_width, bg_height = background.size
        used_insects = set()
        annotations_for_image = []

        for _ in range(insects_per_image):
            insect_filename = random.choice(insect_images)
            # Evitar repetição de imagens de insetos
            while insect_filename in used_insects and len(used_insects) < len(insect_images):
                insect_filename = random.choice(insect_images)
            used_insects.add(insect_filename)
            
            insect_path = os.path.join(original_datasets_folder, insect_filename)
            insect = Image.open(insect_path).convert("RGBA")
            insect_width, insect_height = insect.size

            # Reduz o tamanho do inseto antes de inseri-lo no fundo
            scale_factor = 0.08  # Fator de escala fixo de 10%
            insect = insect.resize(
                (int(insect_width * scale_factor), int(insect_height * scale_factor)), 
                Image.LANCZOS
            )
            insect_width, insect_height = insect.size

            # Verifica se o inseto é maior que o fundo e redimensiona se necessário
            if insect_width > bg_width or insect_height > bg_height:
                scale_factor = min(bg_width / insect_width, bg_height / insect_height)
                insect = insect.resize(
                    (int(insect_width * scale_factor), int(insect_height * scale_factor)), 
                    Image.LANCZOS
                )
                insect_width, insect_height = insect.size

            max_x = bg_width - insect_width
            max_y = bg_height - insect_height

            # Verificação para evitar valores negativos em max_x e max_y
            if max_x < 0 or max_y < 0:
                print(f"Imagem do inseto '{insect_filename}' é maior que o fundo '{background_filename}'. Pulando...")
                continue

            # Gera coordenadas aleatórias para inserir o inseto no fundo
            x, y = random.randint(0, max_x), random.randint(0, max_y)
            background.paste(insect, (x, y), insect)

            # Cria a anotação no formato COCO
            annotations_for_image.append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": 1,
                "bbox": [x, y, insect_width, insect_height],
                "area": insect_width * insect_height,
                "iscrowd": 0
            })
            annotation_id += 1

        # Salva a imagem combinada no diretório de saída
        output_image_path = os.path.join(output_folder, f"combined_{image_id}.jpg")
        background.convert("RGB").save(output_image_path)

        # Adiciona os metadados da imagem ao JSON COCO
        coco_data["images"].append({
            "id": image_id,
            "file_name": f"combined_{image_id}.jpg",
            "height": bg_height,
            "width": bg_width
        })
        coco_data["annotations"].extend(annotations_for_image)
        image_id += 1

    # Salva o arquivo JSON no formato COCO
    with open(json_path, 'w') as json_file:
        json.dump(coco_data, json_file, indent=4)
