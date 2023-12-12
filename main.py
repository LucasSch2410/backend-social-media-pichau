import sys
from PIL import Image, ImageDraw, ImageFont

import dropbox
from dropbox.exceptions import AuthError

from app.oauth.connection import authenticate_dropbox
from app.layouts.stories.stories_layout import InstagramLayout

def main(): 
    dbx = dropbox_connect()
    
    product_name = input("Nome do produto: ").upper().split(", ")
    
    for i in range(len(product_name)):
        product_name[i].replace(",", "")

    product = InstagramLayout(product_name, dbx)

    # Put the text into template
    product.create_text()

    # Put the image into template
    product.product_create()

    product.background.save("data/output/file.png")

    sys.exit(0)


# Production connection
def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox('sl.BrlKP7lENyhKOR5vWN6RhKEj87k5r7lgnI9y5Y8a0hx29BH8jRdbqs8Ty4WzU-U01GuJN5hbKWQHdWMHh3X8w96r5mtuip2A8YItt4B9AChWYJyz3o_tCF0whf9PVO4wAUcEbaYUtigWMC2H5GT-fPU')
    except AuthError as e:
        print('Erro ao se conectar ao Dropbox com o token de acesso: ' + str(e))
        sys.exit(3)
    return dbx


# TODO Creates the red background in the price section
def create_layout():
    return None





main()