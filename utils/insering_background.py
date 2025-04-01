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
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return mask

def is_valid_position(mask, x, y, width, height):
    region = mask[y:y+height, x:x+width]
    return np.mean(region) > 200

def create_shadow(insect_img, offset=(5, 5), alpha=0.5):
    """Cria uma sombra para o inseto deslocando, escurecendo e ajustando a transparência."""
    h, w = insect_img.shape[:2]
    shadow = insect_img.copy()
    
    # Tornar a imagem completamente preta (sombra)
    shadow = cv2.multiply(shadow, np.array([0.0, 0.0, 0.0, 1.0]))  # Deixa a imagem preta mantendo a transparência

    # Deslocar a sombra um pouco para baixo e para a direita
    M = np.float32([[1, 0, offset[0]], [0, 1, offset[1]]])
    shadow = cv2.warpAffine(shadow, M, (w, h))

    # Ajustar a opacidade da sombra
    shadow[:, :, 3] = (shadow[:, :, 3] * alpha).astype(np.uint8)

    return shadow

def adjust_levels(image, in_min=0, in_max=180, out_min=0, out_max=255):
    """Ajusta os níveis da imagem para melhorar o contraste."""
    image = np.clip((image - in_min) * ((out_max - out_min) / (in_max - in_min)) + out_min, 0, 255)
    return image.astype(np.uint8)

def decrease_brightness(image, factor=0.9):
    """Diminui a claridade da imagem."""
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)

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

    for background_filename in background_images:
        background_path = os.path.join(background_folder, background_filename)
        background = cv2.imread(background_path)
        bg_height, bg_width = background.shape[:2]

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
            insect = insect.resize((int(insect.width * 0.2), int(insect.height * 0.2)), Image.LANCZOS)

            # Converter para OpenCV (BGR com canal alfa)
            insect_cv = cv2.cvtColor(np.array(insect), cv2.COLOR_RGBA2BGRA)
            insect_height, insect_width = insect_cv.shape[:2]

            max_attempts = 10
            while max_attempts > 0:
                x, y = random.randint(0, bg_width - insect_width), random.randint(0, bg_height - insect_height)
                if is_valid_position(mask, x, y, insect_width, insect_height):
                    break
                max_attempts -= 1

            if max_attempts == 0:
                continue

            # Criar sombra
            shadow = create_shadow(insect_cv, offset=(5, 5), alpha=0.5)

            # Ajustar níveis do inseto original
            adjusted_insect = adjust_levels(insect_cv)

            # Diminuir a claridade do inseto
            adjusted_insect = decrease_brightness(adjusted_insect, factor=0.7)

            # Inserir a sombra primeiro
            alpha_channel_shadow = shadow[:, :, 3] / 255.0
            for c in range(3):
                background[y:y+insect_height, x:x+insect_width, c] = \
                    (1 - alpha_channel_shadow) * background[y:y+insect_height, x:x+insect_width, c] + \
                    alpha_channel_shadow * shadow[:, :, c]

            # Inserir o inseto ajustado
            alpha_channel_insect = adjusted_insect[:, :, 3] / 255.0
            for c in range(3):
                background[y:y+insect_height, x:x+insect_width, c] = \
                    (1 - alpha_channel_insect) * background[y:y+insect_height, x:x+insect_width, c] + \
                    alpha_channel_insect * adjusted_insect[:, :, c]

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
        cv2.imwrite(output_image_path, background)

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
