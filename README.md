NÃO ESTÁ PRONTO


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
pip install pillow imgaug diffusers torch transformers accelerate pillow imgaug
```

## Estrutura de Pastas

- **`input_images/`**: Pasta onde as imagens de entrada devem ser armazenadas.
- **`backgrounds/`**: Pasta contendo imagens de fundo para o inpainting.
- **`output_images/`**: Pasta onde as imagens aumentadas e processadas serão salvas.

Certifique-se de criar essas pastas na mesma pasta onde o script está localizado.

## Obseração
- Há imagens nas pastas `input_files` e `background` utilizadas para teste. Para aplicação é necessário removê-las

## Inserindo Token no Hubbing Face

### Gerando Token

- Acesse Hugging Face.
- Faça login ou crie uma conta se ainda não tiver uma.
- Vá para as configurações da sua conta clicando na sua foto de perfil e selecionando "Settings".
- Vá até a seção "Access Tokens".
- Clique em "New token" para criar um novo token. Dê um nome a ele e selecione as permissões necessárias (por exemplo, "read").

### Inserindo no códigio

- Entre no arquivo `insering_background.py`
- Ache a variável `login` e insira o token lá

  obs: Se não for inserida corretamente, NÃO vai funcionar.


 ### Adicionando dataset

 - Selecione a pasta onde as imagens do seu banco de imagens que deseja processar
 - Supondo que ela esteja em na pasta "Imagens" e o código esteja na pasta "Documentos"

  
    ```
    cd /home/seu_usuario/
    mv /Imagens/pasta_com_imagens/ Documentos/gerando_imanges/input_files/
    ```
   

## Como Executar
1. **Defina os caminhos das pastas** no código `main.py`, conforme o exemplo abaixo:

    ```
    image_folder = "./input_images"
    background_folder = "./backgrounds"
    output_folder = "./output_images"
    ```

2. **Execute o script principal**:
   
   Para rodar o script, utilize o seguinte comando:
   
   ```bash
   python main.py
   ```

3. **Informe o número de imagens aumentadas a serem geradas** quando solicitado pelo programa. Esse valor controla quantas variações aumentadas serão geradas para cada imagem de entrada.

## Descrição do Processo

- O algoritmo carrega imagens de uma pasta de entrada (`input_images`) e aplica uma série de aumentos, como espelhamento, rotação e adição de ruído.
- Para cada imagem aumentada, o algoritmo escolhe uma imagem de fundo aleatória da pasta `backgrounds` e aplica o método de inpainting para inserir a imagem aumentada sobre o fundo.
- As imagens processadas são salvas na pasta de saída (`output_images`) com nomes sequenciais para facilitar o acesso e o controle.

Esse processo cria uma série de imagens variadas e realistas, útil para expandir conjuntos de dados de imagens e aprimorar modelos de aprendizado de máquina.

