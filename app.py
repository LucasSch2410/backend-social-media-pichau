import sys
from PIL import Image, ImageDraw
from io import BytesIO

import dropbox
from dropbox.exceptions import AuthError

def main():
    connection = dropbox_connect()

    product = input("sku: ").upper().split(", ")

    template_storie = Image.open('templates/template-storie.jpg')
    dropbox_file = dropbox_download_file(product[len(product) - 1], connection)

    if dropbox_file is not None:
        image = Image.open(dropbox_file)
    else:
        print("Erro ao retornar a imagem.")
        sys.exit(2)

    # Put the text into template
    create_text(product, template_storie)

    # Put the image into template
    product_create(image, template_storie)

    template_storie.save("output.png")

    sys.exit(0)








def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox('sl.BrHnAYYkYr54rZovRiH26x2E6JPDc4Iq59YncJha81pLJZLAl9yZLoQXQ83DzhoEbR8Nekw_SSsN4BRaxAC4HiFwYIdwKwdNWEiIzaDzyw8eLtt6EURPDOt_DrRfuO5eWpAQWYETP3I_DypL1lBF5wE')
    except AuthError as e:
        print('Erro ao se conectar ao Dropbox com o token de acesso: ' + str(e))
        sys.exit(3)
    return dbx


def dropbox_download_file(sku, dropbox):
    """Download a file from Dropbox to the local machine."""

    try:
        metadata, response = dropbox.files_download(f"/automacao_midia/{sku}.png")
        
        # Get the binary content of the file
        data = BytesIO(response.content)

        return data
    except Exception as e:
        print('Erro ao fazer o download da imagem no Dropbox: ' + str(e))
        sys.exit(1)

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







# Creates the red background in the price section
def create_layout():
    return None

# Creates the text in the image
def create_text(text, template):
    
    d1 = ImageDraw.Draw(template)
    titleSize = d1.textlength(text[0], font_size=50)
    if titleSize > template.width:
        text1 = text[0].split(" ").pop()
        ' '.join(text1)
        text2 = text.split(" ")

        d1.multiline_text((28, 36), text1 + "\n" + text2[len(text2) - 1], fill=(255, 0, 0), font_size=50)
    else:
        d1.multiline_text((28, 36), text[0], fill=(255, 0, 0), font_size=50)


    template.show()
    return True

main()