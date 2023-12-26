from app.resources.resource_handler import load_background, load_product_image, load_font
from PIL import Image, ImageDraw, ImageFont
import sys

class InstagramLayout:

    def __init__(self, product_name, dropbox):
        self.product_name = product_name
        self.background = load_background("data/input/templates/template-storie.jpg")
        self.product = load_product_image(self.product_name[len(product_name) - 1], dropbox)
        self.titleFont = load_font()
    
    def text_wrap(self, text, font, max_width):
        """ 
        Wrap the text if it's bigger than the template width.
        
        Args:
            text: The full text. (List[str])
            font: The font object. (Font)
            max_width: The maximum width that the text will can be. (Int)
        
        Return:
            A lines list with length less than or equal to 3, each item represents 
            a line to draw. (List[str])
        """

        lines = []

        separated_text = ', '.join(text[:-1]) + ','

        # Return if the text width is smaller than max_width
        if font.getlength(separated_text) <= max_width:
            lines.append(separated_text) 
        else:
            words = separated_text.split(' ')  
            i = 0
            while i < len(words):
                line = ''         
                while i < len(words) and font.getlength(line + words[i]) <= max_width:                
                    line = line + words[i] + " "
                    i += 1
                lines.append(line)  
                # Stop if there more than three lines and and removes clipped features
                if len(lines) > 2:
                    if lines[2][-1] != ',':
                        temp = lines[2].split(', ')
                        temp = ', '.join(temp[:-1])
                        lines[2] = temp
                    break  
        return lines
    
    def create_text(self):
        """
        Creates the text on the top of the image.

        Args:
            text: A list of strings representing the text to be displayed. (List[str])
            template: The template image object. (Image)
            font: The font object. (Font)
        
        Return:
        The height of the text created. (int)
        """

        draw = ImageDraw.Draw(self.background)

        wraped_text = self.text_wrap(self.product_name, self.titleFont, self.background.width - 200) # Wrap text based on template width.
        multilines_text = '\n'.join(wraped_text) # Join wrapped lines with newline characters.

        draw.text((110,480), multilines_text, font=self.titleFont, fill=(255, 255, 255), # Draw text with white fill.
                stroke_width=10, stroke_fill=(0, 0, 0)) # Add black stroke around text for better visibility.
        
        # Calculate text height based on font size and number of lines.
        text_height = self.titleFont.getbbox(multilines_text)[3] * len(wraped_text) + (25 * len(wraped_text))
        self.text_height = text_height
        return True
    
    def product_create(self):
        """ 
        Resize the Image and put in the template.
        
        Args:
            product: The product image object. (Image)
            template: The template image object. (Image)
            text_height: The height of the text created. (int)
        """

        try:
            # Calculate the width and height of the non-transparent region
            cropped_image = self.product.crop(self.product.getbbox())
            
            # Calculate the aspect ratio
            aspect_ratio = cropped_image.width / cropped_image.height

            # Calculate the new height based on the template aspect ratio
            new_width = self.background.width - 200
            new_height = int(new_width / aspect_ratio)

            # Resize the product image with the new dimensions
            resized_image = cropped_image.resize((new_width, new_height))

            position = (100, 480 + self.text_height) 
            self.background.paste(resized_image, position, mask=resized_image) 
            return True
        except Exception as e:
            print("Error when add the product image into background: ", e)
            sys.exit(4)

    def create_layout(self):
        """Generates the complete Instagram layout."""
        try:
            self.create_text()  
            self.product_create()  
            return self.background  
        except Exception as e:
            print("Erro durante a criação do layout:", e)
            return None  # Indicate failure

    def __call__(self):
        return self.create_layout()


    
