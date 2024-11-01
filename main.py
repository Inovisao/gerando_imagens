from process_image import process_and_save_images



number_process_images = int(input("Informe a quantidade de imagens a ser geradas: "))
image_path = "./input_images" # Defina aqui o caminho das imagens originais
output_folder = "./output_images" #Defina aqui o caminho de saida
background_folder = "./background" #Defina aqui o caminho dos fundos das imagens



process_and_save_images(image_path, background_folder, output_folder, number_process_images)