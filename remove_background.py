from PIL import Image
from rembg import remove  # Usando a biblioteca rembg para remoção de fundo
from io import BytesIO  # Importando BytesIO
import os

def remove_background_from_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory, filename)
            print(f"Processando imagem: {image_path}")
            
            try:
                # Converte a imagem para bytes
                with open(image_path, 'rb') as img_file:
                    input_data = img_file.read()
                
                # Remove o fundo usando a biblioteca rembg
                output_data = remove(input_data)
                
                # Salva a imagem sem fundo como PNG
                output_image = Image.open(BytesIO(output_data)).convert("RGBA")
                output_path = os.path.join(directory, f"no_bg_{os.path.splitext(filename)[0]}.png")
                output_image.save(output_path, format='PNG')
                print(f"Imagem sem fundo salva em: {output_path}")
                
                # Remove a imagem original
                os.remove(image_path)
                print(f"Imagem original removida: {image_path}")
            except Exception as e:
                print(f"Erro ao processar a imagem {image_path}: {e}")
