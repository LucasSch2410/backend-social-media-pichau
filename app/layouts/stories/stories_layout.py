from app.resources.resource_handler import load_background, load_product_image, load_font
from PIL import Image, ImageDraw, ImageFont
import sys

class InstagramLayout:

    def __init__(self, product_name, dropbox):
        self.product_name = product_name.upper().split(", ")
        self.background = load_background("data/input/templates/template-storie.jpg")
        self.product = load_product_image(self.product_name[len(self.product_name) - 1], dropbox)
        self.titleFont, self.featureFont = load_font()
    
    def text_wrap(self, text, font, max_width, isTitle=False):
        """ 
        Wrap the text if it's bigger than the template width.
        
        Args:
            text: The full text. (str)
            font: The font object. (Font)
            max_width: The maximum width that the text will can be. (Int)
            isTitle: Verify if the text is the Title or no (Boolean)
        
        Return:
            A lines list with length less than or equal to 2, each item represents 
            a line to draw. (List[str])
        """

        lines = []

        # Return if the text width is smaller than max_width and isn't the title
        if font.getlength(text[:-1]) <= max_width and isTitle == False:
            lines.append(text[:-1]) 
        else:
            words = text.split(' ')  
            i = 0
            while i < len(words):
                line = ''         
                while i < len(words) and font.getlength(line + words[i]) <= max_width:                
                    line = line + words[i] + " "
                    i += 1
                lines.append(line)  
                # Stop if there more than two lines and removes clipped features
                if len(lines) > 1:
                    if isTitle:
                        break
                    elif lines[1][-2:] != ', ':
                        temp = lines[1].split(', ')
                        temp = ', '.join(temp[:-1])
                        lines[1] = temp
                    elif lines[1][-2:] == ', ':
                        lines[1] = lines[1][:-2]
                    break  
        return lines
    
    def create_text(self):
        """
        Creates the text on the top of the image.
        """

        draw = ImageDraw.Draw(self.background)

        wraped_title = self.text_wrap(self.product_name[0], self.titleFont, self.background.width - 200, True) # Wrap title based on template width.
        wrapped_features = self.text_wrap(', '.join(self.product_name[1:-1]) + ',', self.featureFont, self.background.width - 200) # Wrap features based on template width.

        draw.text((110,480), '\n'.join(wraped_title), font=self.titleFont, fill=(255, 255, 255), # Draw text with white fill.
                stroke_width=6, stroke_fill=(0, 0, 0)) # Add black stroke around text for better visibility.
        
        # Calculate text height based on font size and number of lines.
        text_height = self.titleFont.getbbox('\n'.join(wraped_title))[3] * len(wraped_title) + (25 * len(wraped_title))

        draw.text((110,480 + text_height), '\n'.join(wrapped_features), font=self.featureFont, fill=(255, 255, 255), # Draw text with white fill.
                stroke_width=6, stroke_fill=(0, 0, 0)) # Add black stroke around text for better visibility.

        self.text_height = text_height + self.featureFont.getbbox('\n'.join(wrapped_features))[3] * len(wrapped_features) + (25 * len(wrapped_features))

        return True
    
    def product_create(self):
        """ 
        Resize the Image and put in the template.
        
        Args:
            product: The product image object. (Image)
            template: The template image object. (Image)
            text_height: The height of the text created. (int)
        """

        # Calculate the width and height of the non-transparent region
        cropped_image = self.product.crop(self.product.getbbox())
        
        # Calculate the aspect ratio
        aspect_ratio = cropped_image.width / cropped_image.height

        # Calculate the new height based on the template aspect ratio
        new_width = self.background.width - 200
        new_height = int(new_width / aspect_ratio)

        # Resize if the image is bigger than 600 pixels
        if new_height > 600:
            new_height = 600
            new_width = int(new_height * aspect_ratio)

        # Resize the product image with the new dimensions
        resized_image = cropped_image.resize((new_width, new_height))

        margin_top = int(((1960 + self.text_height) / 2) - new_height / 2)
        margin_left = int((self.background.width - new_width) / 2)

        position = (margin_left, margin_top) 
        self.background.paste(resized_image, position, mask=resized_image) 
        return True

    def create_layout(self):
        """Generates the complete Instagram layout."""
        try:
            self.create_text()  
            self.product_create()  
            return self.background  
        except Exception as e:
            raise Exception(f'Error occurred during layout creation: {str(e)}')

    def __call__(self):
        return self.create_layout()


    
