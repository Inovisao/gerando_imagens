import os
import json
import random
from PIL import Image, ImageEnhance
import numpy as np
import cv2
from remove_background import remove_background_from_directory

def generate_brightness_mask(image_path, threshold=90):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar um limiar para criar uma máscara onde áreas claras são brancas
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return mask

def is_valid_position(mask, x, y, width, height):
    """Verifica se a área selecionada na máscara é clara o suficiente para inserir o inseto."""
    region = mask[y:y+height, x:x+width]
    if np.mean(region) < 200:  # Verifica se a média de brilho da região é alta
        return False
    return True

def inpainting_with_annotations(background_folder, original_datasets_folder, output_folder, insects_per_image):
    remove_background_from_directory(original_datasets_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    json_path = os.path.join(output_folder, 'annotations.coco.json')
    if not os.path.exists(json_path):
        coco_data = {
            "info": {"year": "2024", "version": "2"},
            "licenses": [{"id": 1, "name": "CC BY 4.0"}],
            "categories": [{"id": 1, "name": "insect"}],
            "images": [],
            "annotations": []
        }
        annotation_id = 1
        image_id = 1
    else:
        with open(json_path, 'r') as json_file:
            coco_data = json.load(json_file)
            annotation_id = max([ann['id'] for ann in coco_data['annotations']], default=0) + 1
            image_id = max([img['id'] for img in coco_data['images']], default=0) + 1

    background_images = [f for f in os.listdir(background_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    insect_images = [f for f in os.listdir(original_datasets_folder) if f.startswith('no_bg_') and f.endswith(('.png', '.jpg', '.jpeg'))]

    if not insect_images:
        print("Erro: Nenhuma imagem de inseto encontrada.")
        return

    for background_filename in background_images:
        background_path = os.path.join(background_folder, background_filename)
        background = Image.open(background_path).convert("RGBA")
        bg_width, bg_height = background.size

        # Gera a máscara de brilho para a imagem de fundo
        mask = generate_brightness_mask(background_path)

        used_insects = set()
        annotations_for_image = []

        for _ in range(insects_per_image):
            insect_filename = random.choice(insect_images)
            while insect_filename in used_insects and len(used_insects) < len(insect_images):
                insect_filename = random.choice(insect_images)
            used_insects.add(insect_filename)
            
            insect_path = os.path.join(original_datasets_folder, insect_filename)
            insect = Image.open(insect_path).convert("RGBA")
            insect_width, insect_height = insect.size

            scale_factor = 0.2 
            insect = insect.resize((int(insect_width * scale_factor), int(insect_height * scale_factor)), Image.LANCZOS)
            insect_width, insect_height = insect.size

            max_attempts = 10
            while max_attempts > 0:
                x, y = random.randint(0, bg_width - insect_width), random.randint(0, bg_height - insect_height)
                
                if is_valid_position(mask, x, y, insect_width, insect_height):
                    break
                max_attempts -= 1

            if max_attempts == 0:
                print(f"Não foi possível encontrar uma posição válida para '{insect_filename}' em '{background_filename}'.")
                continue

            mask_alpha = insect.split()[3]
            enhancer = ImageEnhance.Brightness(mask_alpha)
            mask_alpha = enhancer.enhance(0.8)
            background.paste(insect, (x, y), mask_alpha)

            annotations_for_image.append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": 1,
                "bbox": [x, y, insect_width, insect_height],
                "area": insect_width * insect_height,
                "iscrowd": 0
            })
            annotation_id += 1

        output_image_path = os.path.join(output_folder, f"combined_{image_id}.jpg")
        background.convert("RGB").save(output_image_path)

        coco_data["images"].append({
            "id": image_id,
            "file_name": f"combined_{image_id}.jpg",
            "height": bg_height,
            "width": bg_width
        })
        coco_data["annotations"].extend(annotations_for_image)
        image_id += 1

    with open(json_path, 'w') as json_file:
        json.dump(coco_data, json_file, indent=4)
