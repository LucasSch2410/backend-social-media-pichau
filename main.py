import sys
from PIL import Image, ImageDraw, ImageFont

import dropbox
from dropbox.exceptions import AuthError

from app.oauth.connection import authenticate_dropbox
from app.resource_handler import load_background, load_product_image, load_font


def main(): 
    dbx = dropbox_connect()
    
    product_name = input("Nome do produto: ").upper().split(", ")
    
    for i in range(len(product_name)):
        product_name[i].replace(",", "")


    print(product_name)
    # Import essential files
    template_storie = load_background("data/input/templates/template-storie.jpg")
    
    dropbox_file = load_product_image(product_name[len(product_name) - 1], dbx)
    if dropbox_file is not None:
        image = Image.open(dropbox_file)
    else:
        print("Erro ao retornar a imagem.")
        sys.exit(1)


    # Put the text into template
    height = create_text(product_name, template_storie, load_font())

    # Put the image into template
    product_create(image, template_storie, height)

    template_storie.save("data/output/file.png")

    sys.exit(0)


# Production connection
def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox('sl.BrIZf3B-rqu6qAAJ5D3IdpaKA-AnMJPbRCY3qRlLdAFi7_CaLuuTBFHlyMA0wkry_h1KSi9vvmqRssbH7XOwPFyYOiV0Y1ZV1ZEFfhhOGRpi_MCypU9eFRtFXXlnetRIJtAUHBFN5Shl8z-isnYOBWM')
    except AuthError as e:
        print('Erro ao se conectar ao Dropbox com o token de acesso: ' + str(e))
        sys.exit(3)
    return dbx


# Resize the Image and put in the template
def product_create(product, template, height):
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

        position = (100, 480 + height) 
        template.paste(new_image, position, mask=new_image) 
        return True
    except Exception as e:
        print("Error when add the product image into background: ", e)
        sys.exit(4)


# TODO Creates the red background in the price section
def create_layout():
    return None


# Wrap the text if it's bigger than the template width
def text_wrap(text, font, max_width):
    lines = []
    # Return if the text width is smaller than max_width
    if font.getlength(text) <= max_width:
        lines.append(text) 
    else:
        words = text.split(' ')  
        i = 0
        while i < len(words):
            line = ''         
            while i < len(words) and font.getlength(line + words[i]) <= max_width:                
                line = line + words[i] + " "
                i += 1
            lines.append(line)  
            # Stop if have too many lines and excludes the last two characters
            if len(lines) > 2:
                lines[len(lines)-1] = lines[len(lines)-1][:-2]
                break  
    return lines


# Creates the top text in the image
def create_text(text, template, font):
    draw = ImageDraw.Draw(template)

    full_text = ', '.join(text[:len(text)-1])
    wraped_text = text_wrap(full_text, font, template.width - 200)
    multilines_text = '\n'.join(wraped_text)
    draw.text((110,480), multilines_text, font=font, fill=(255, 255, 255), stroke_width=10, stroke_fill=(0, 0, 0))
    
    # Returns the height of the text
    height = font.getbbox(multilines_text)[3] * len(wraped_text) + (25 * len(wraped_text))
    return height




main()