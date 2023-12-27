import sys
from PIL import Image, ImageFont
from io import BytesIO

def load_background(path):
    """Import the background template."""
    try:
        template = Image.open(path)
        return template
    except Exception as e:
        raise Exception(f'Error importing template image: {str(e)}')

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
            raise Exception("Image is null.")
        return image
    except Exception as e:
        raise Exception(f'Error when downloading image from dropbox: {str(e)}')


def load_font():
        """Import the BebasNeue Font"""
        try:
            font = ImageFont.truetype("data/input/fonts/BebasNeue-Bold.ttf", 80)
            return font
        except Exception as e:
            raise Exception(f'Error importing font: {str(e)}')
