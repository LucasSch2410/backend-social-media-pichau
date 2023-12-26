import sys
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, jsonify, request

import dropbox
from dropbox.exceptions import AuthError

# from app.oauth.connection import authenticate_dropbox
from app.layouts.stories.stories_layout import InstagramLayout

app = Flask(__name__)

@app.route('/media', methods=['POST'])
def create_media():

    dbx = dropbox_connect()

    product = request.json["product"]

    product_name = product.upper().split(", ")
    
    for i in range(len(product_name)):
        product_name[i].replace(",", "")

    final_layout_image = InstagramLayout(product_name, dbx)()

    if final_layout_image:
        final_layout_image.save("data/output/file.png")  # Save the image if successful
        return 'Success!'
    else:
        return "Error occurred during layout creation."

@app.route('/post', methods=['POST'])
def scrap_sheet():
    return True

# Production connection 
def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox('sl.BsdDhpjWYz9ieoXQsYYfhopRmKasZedYepKHNAY9Wel-CJhBRnmp5AB4qAukC_Wr3ZT-Gqc7aqkHFp7ON4-x-E_MCtJMKb-2gico1fApuoerMJ6pFAcEVMI4PdUgbHSGRhmXY_mI-PlZsCu2JTMH18Y')
    except AuthError as e:
        print('Erro ao se conectar ao Dropbox com o token de acesso: ' + str(e))
        sys.exit(3)
    return dbx

app.run(port=5000, host='localhost', debug=True)
