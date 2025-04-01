import os

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Pasta criada: {path}")
    else:
        print(f"Pasta já existe: {path}")
