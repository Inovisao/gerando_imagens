
# Gerando imagens a partir de uma única

Este é um algoritmo de aumento de dados para imagens, utilizando a biblioteca `imgaug` para aplicar técnicas de aumento (augmentations) como espelhamento, rotação, corte e ruído. Além disso, o algoritmo utiliza o método de *inpainting* da biblioteca `diffusers` para combinar imagens de entrada com fundos aleatórios, criando um conjunto expandido de imagens aumentadas e realistas.



## Requisitos

Para executar o código, certifique-se de ter as seguintes bibliotecas Python instaladas:

- **Pillow**: para manipulação de imagens.
- **imgaug**: para técnicas de aumento de dados em imagens.
- **diffusers**: para inpainting usando o modelo Stable Diffusion.
- **torch**: como backend para o modelo `diffusers`.
- **transformers** e **accelerate**: para rodar o pipeline de inpainting da Hugging Face.

### Instalação das Bibliotecas

Execute os seguintes comandos para instalar as bibliotecas:

```bash
conda create --name gerando_imagens
conda activate gerando_imagens
pip install pillow imgaug diffusers torch transformers accelerate
```

## Estrutura de Pastas

- **`input_images/`**: Pasta onde as imagens de entrada devem ser armazenadas.
- **`backgrounds/`**: Pasta contendo imagens de fundo para o inpainting.
- **`output_images/`**: Pasta onde as imagens inseridas pelo inpainting estão salvas.
- **`final_dataset/`**: Pasta onde as imagens processadas ficarão salvas.



## Como Executar
1. **Defina os caminhos das pastas** no código `main.py`, conforme o exemplo abaixo:

    ```
    background_folder = "./background"
    output_folder = "./final_dataset"
    image_path = "./original_dataset/"
    output_images = "./output_images"
    ```

2. **Execute o script principal**:
   
   Para rodar o script, utilize o seguinte comando:
   
   ```
   python main.py
   ```


3.  ** Adicionando dataset **

 - Selecione a pasta onde as imagens do seu banco de imagens que deseja processar
 - Supondo que ela esteja em na pasta "Imagens" e o código esteja na pasta "Documentos"

  
    ```
    cd /home/seu_usuario/
    mv /Imagens/pasta_com_imagens/ pasta_ate_gerando_images/gerando_images/original_dataset/
    ```

- Caso selecione a primeira opção, as imagens devem ser inseridas na pasta "original_dataset" com a anotação coco.

- Caso selecione a segunda opção, as imagens originais devem ser inseridas na pasta "original_dataset" e as imagens de fundo na pasta "backgrounds"

4. **Informe o número de imagens aumentadas a serem geradas** quando solicitado pelo programa. Esse valor controla quantas variações aumentadas serão geradas para cada imagem de entrada.


