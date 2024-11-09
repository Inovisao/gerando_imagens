from create_folder import create_folder
from insering_background import inpainting_with_annotations as inpainting
from process_image import process_and_augment_images as ps


number_per_image = int(input("Informe a quantidade de imagens a ser inseridas por fundo: "))
number_process_images = int(input("\nInforme a quantidade de imagens a ser geradas por classe: "))

# Defina aqui os caminhos da pasta
background_folder = "./background"
output_folder = "./final_dataset"
image_path = "./original_dataset/"
output_images = "./output_images"

# Cria as pastas se não existirem
create_folder(background_folder)
create_folder(output_folder)
create_folder(image_path)
create_folder(output_images)

print("\nInserindo imagens em fundos...")
inpainting(background_folder, image_path, output_images, number_per_image)

print("\nAplicando aumento de dados nas imagens resultantes...")
ps(output_images, output_folder, number_process_images)

print("\nProcessamento concluído com sucesso!")
