import sys
from PIL import Image, ImageDraw

import dropbox
from dropbox.exceptions import AuthError

from app.oauth.connection import authenticate_dropbox
from app.resource_handler import load_background, load_product_image, load_font


def main(): 
    dbx = dropbox_connect()
    
    product_name = input("Nome do produto: ").upper().split(", ")

    # Import essential files
    template_storie = load_background("data/input/templates/template-storie.jpg")
    
    dropbox_file = load_product_image(product_name[len(product_name) - 1], dbx)
    if dropbox_file is not None:
        image = Image.open(dropbox_file)
    else:
        print("Erro ao retornar a imagem.")
        sys.exit(1)


    # Put the text into template
    create_text(product_name, template_storie)

    # Put the image into template
    product_create(image, template_storie)

    template_storie.save("data/output/output.png")

    sys.exit(0)


# Production connection
def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox('sl.BrLjXJsXMIxiDiMiZ9Cz9YJ6K0TVquXhDooo3d6nt1YGi47VAN6wAV4GYrHfvBCgDhypl84ua5RRlSNm8p1stdCwo9oEmkGbENEJYFcMCR6RqGzdFipdwfF-9otmZoJ2sT5xJDlTGaCtd9QMBNKMrJ4')
    except AuthError as e:
        print('Erro ao se conectar ao Dropbox com o token de acesso: ' + str(e))
        sys.exit(3)
    return dbx


# Resize the Image and put in the template
def product_create(product, template):
    try:
        # Calculate the width and height of the non-transparent region
        bbox = product.getbbox()
        croped_image = product.crop((bbox[0], bbox[1], bbox[2], bbox[3]))
        
        # Calculate the aspect ratio
        aspect_ratio = croped_image.width / croped_image.height

        # Calculate the new height based on the template aspect ratio
        new_width = template.width - 200
        new_height = int(new_width / aspect_ratio)

        # Resize the product image with the new dimensions
        new_image = croped_image.resize((new_width, new_height))

        position = (100, 650) 
        template.paste(new_image, position, mask=new_image) 
        return True
    except Exception as e:
        print("Error when add the product image into background: ", e)
        sys.exit(4)


# TODO Creates the red background in the price section
def create_layout():
    return None


# TODO Creates the text in the image
def create_text(text, template):

    
    return True


main()