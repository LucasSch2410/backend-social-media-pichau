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
    
    
    # Import essential files
    template_storie = load_background("data/input/templates/template-storie.jpg")
    
    dropbox_file = load_product_image(product_name[len(product_name) - 1], dbx)
    if dropbox_file is not None:
        image = Image.open(dropbox_file)
    else:
        print("Erro ao retornar a imagem.")
        sys.exit(1)


    # Put the text into template
    text_height = create_text(product_name, template_storie, load_font())

    # Put the image into template
    product_create(image, template_storie, text_height)

    template_storie.save("data/output/file.png")

    sys.exit(0)


# Production connection
def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox('sl.BrRAK8HuXD67WPeyGj2zmEpjRrgYEUwuRvSWXR29rOkwWLd7ihrXYN_9059SIjLqEjMRdhUtK74YFYk-J-1i6xOA0MGO4oKZaMG5s3tXGcbKHCCVWdDtzi3LIiePGw5b3h40byWd3CTKXlCaqt6fjjA')
    except AuthError as e:
        print('Erro ao se conectar ao Dropbox com o token de acesso: ' + str(e))
        sys.exit(3)
    return dbx


def product_create(product, template, text_height):
    """ 
    Resize the Image and put in the template.
    
    Args:
        product: The product image object. (Image)
        template: The template image object. (Image)
        text_height: The height of the text created. (int)
    """

    try:
        # Calculate the width and height of the non-transparent region
        cropped_image = product.crop(product.getbbox())
        
        # Calculate the aspect ratio
        aspect_ratio = cropped_image.width / cropped_image.height

        # Calculate the new height based on the template aspect ratio
        new_width = template.width - 200
        new_height = int(new_width / aspect_ratio)

        # Resize the product image with the new dimensions
        resized_image = cropped_image.resize((new_width, new_height))

        position = (100, 480 + text_height) 
        template.paste(resized_image, position, mask=resized_image) 
        return True
    except Exception as e:
        print("Error when add the product image into background: ", e)
        sys.exit(4)


# TODO Creates the red background in the price section
def create_layout():
    return None


def text_wrap(text, font, max_width):
    """ 
    Wrap the text if it's bigger than the template width.
    
    Args:
        text: The full text separated by commas. (str)
        font: The font object. (Font)
        max_width: The maximum width that the text will can be. (Int)
    
    Return:
        A lines list with length less than or equal to 3, each item represents 
        a line to draw. (List[str])
    """

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
            # Stop if there more than three lines and removes the last two characters
            if len(lines) > 2:
                if lines[-1][-2:] == ", ":
                    lines[-1] = lines[-1][:-2]
                break  
    return lines



def create_text(text, template, font):
    """
    Creates the text on the top of the image.

    Args:
        text: A list of strings representing the text to be displayed. (List[str])
        template: The template image object. (Image)
        font: The font object. (Font)
    
    Return:
       The height of the text created. (int)
    """

    draw = ImageDraw.Draw(template)

    full_text = ', '.join(text[:len(text)-1]) # Combine all text except the last element (SKU).
    wraped_text = text_wrap(full_text, font, template.width - 200) # Wrap text based on template width.
    multilines_text = '\n'.join(wraped_text) # Join wrapped lines with newline characters.

    draw.text((110,480), multilines_text, font=font, fill=(255, 255, 255), # Draw text with white fill.
              stroke_width=10, stroke_fill=(0, 0, 0)) # Add black stroke around text for better visibility.
    
    # Calculate text height based on font size and number of lines.
    text_height = font.getbbox(multilines_text)[3] * len(wraped_text) + (25 * len(wraped_text))
    return text_height




main()