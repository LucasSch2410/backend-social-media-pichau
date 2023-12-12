import sys
from PIL import Image, ImageFont
from io import BytesIO

def load_background(path):
    """Import the background template."""
    try:
        template = Image.open(path)
        return template
    except Exception as e:
        print("Erro ao importar a imagem de template: " + str(e))
        sys.exit(1)

# Download the image from Dropbox
def load_product_image(sku, dropbox):
    """Download a file from Dropbox."""

    try:
        metadata, response = dropbox.files_download(f"/automacao_midia/{sku}.png")
        
        # Get the binary content of the file
        data = BytesIO(response.content)

        if data is not None:
            image = Image.open(data)
        else:
            print("Erro ao retornar a imagem.")
            sys.exit(1)

        return image
    except Exception as e:
        print('Erro ao fazer o download da imagem no Dropbox: ' + str(e))
        sys.exit(1)


def load_font():
        """Import the BebasNeue Font"""
        try:
            font = ImageFont.truetype("data/input/fonts/BebasNeue-Bold.ttf", 120)
            return font
        except Exception as e:
             print("Erro ao importar a fonte: " + str(e))
             sys.exit(1)