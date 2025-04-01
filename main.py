from utils.create_folder import create_folder
from utils.insering_background import inpainting_with_annotations as inpainting
from utils.process_image import process_and_augment_images as ps
from utils.process_video import process_video

def main(mode=None):
    if mode is None:
        mode = int(input("Escolha o modo de operação:\n1. Apenas processar imagens\n2. Converter vídeos em frames\n3. Inserir as imagens e processar\nEscolha: "))
    
    if mode not in [1, 2, 3]:
        print("Opção inválida. Saindo...")
        return

    number_process_images = int(input("\nInforme a quantidade de imagens a ser geradas por classe: "))

    # Defina aqui os caminhos da pasta
    background_folder = "./background"
    output_folder = "./final_dataset"
    image_path = "./original_dataset"
    output_images = "./output_images"

    # Cria as pastas se não existirem
    create_folder(background_folder)
    create_folder(output_folder)
    create_folder(image_path)
    create_folder(output_images)

    if mode == 2:
        video_path = "./videos"
        print("\nConvertendo vídeo em frames...")
        process_video(video_path, background_folder)  # Frames extraídos serão usados como background
        print("\nVídeo convertido com sucesso!")
        
        choice = int(input("\nDeseja inserir imagens nos fundos e processá-los?\n1. Sim\n2. Não\nEscolha: "))
        if choice == 1:
            main(mode=3)  # Chama a função main novamente para inserir as imagens nos fundos
    
    if mode == 3:
        number_per_image = int(input("Informe a quantidade de imagens a ser inseridas por fundo: "))
        print("\nInserindo imagens em fundos...")
        inpainting(background_folder, image_path, output_images, number_per_image)
        print("\nAplicando aumento de dados nas imagens resultantes...")
        ps(output_images, output_folder, number_process_images)
    else:
        print("\nAplicando aumento de dados nas imagens resultantes...")
        ps(image_path, output_folder, number_process_images)

    print("\nProcessamento concluído com sucesso!")

if __name__ == "__main__":
    main()
