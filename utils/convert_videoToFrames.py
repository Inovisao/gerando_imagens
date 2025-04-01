import moviepy.editor as mp
import os


def convert_videoToFrames(video_path, output_path):
    if not os.path.exists(output_path): # Cria pasta se não existir
        os.makedirs(output_path)
        print(f"Pasta criada: {output_path}")
    
    for video in os.listdir(video_path): # percorre todos os videos dentro da pasta
        if video.lower().endswith('.avi','.mov','.mkv','.mpw'): # verifica se é um vídeo
            clip = mp.VideoFileClip(video_path + video) # carrega os videos
            clip.write_images_sequence(output_path + video + '_frame%04d.jpg') # transforma em frames
            print(f"Frames extraídos de {video}")
        else: 
            print(f"Arquivo {video} não é um vídeo")
            