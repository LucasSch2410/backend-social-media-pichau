import csv, requests
import dropbox
import base64
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from flask import Flask, jsonify, request, redirect, send_file
from bs4 import BeautifulSoup
from dropbox.exceptions import AuthError

# from app.oauth.connection import authenticate_dropbox
from app.layouts.stories.stories_layout import InstagramLayout

app = Flask(__name__)


@app.route('/instagram', methods=['GET'])
def create_media():
    try:
        dbx = dropbox_connect()

        final_layout_image = InstagramLayout(request.args["product"], dbx)()

        if final_layout_image:
            final_layout_image.save("data/output/file.png")  # Save the image if successful
            with open("data/output/file.png", 'rb') as f:
                image_base64 = base64.b64encode(f.read())
                image_base64_str = image_base64.decode('utf-8')
            response = jsonify(image_base64_str)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

        else:
            raise Exception("Error occurred during layout creation.")
    except AuthError as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/sheet', methods=['GET'])
def scrap_sheet():
    """
    Scrap the HTML of the Google Sheet in the URL from the request
    """

    html = requests.get(request.args['sheet_url'])
    soup = BeautifulSoup(html.text, "html.parser")
    table = soup.find("tbody")
    products = {}
    index = 0

    # Iterate across product lines
    for line in table:
        index = int(line.find('th').get_text())
        if index > 1:
            product = line.find('td').get_text()
            if product != "":
                products.update({index:product})
                index += 1

    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# Auth2 redirect
@app.route('/auth2', methods=['GET'])
def auth2():
    client_id = 'emm8mikk0bmdwbn'
    client_secret = 'ldxj4yfnixjfhdz'
    refresh_token = '3_63z0G-Y_IAAAAAAAAAAcgOLuMn6bvTvJDW4fYcu9FfsEpdm-YfdP96FWilulA9'

    token_url = "https://api.dropboxapi.com/oauth2/token"
    params = {
        "grant_type": 'refresh_token',
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }

    r = requests.post(token_url, data=params)

    if r.status_code != 200:
        return f'Error {r.content}'
    
    access_token = r.json()['access_token']
    
    return redirect(f'http://localhost:5173?access_token={access_token}')


# Production connection 
def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox('sl.BsxYynhTTiphy9usSzmW0gEhcehSH1Hz0gir5yl5ZIa4qwDp_ahg35OjSa5rKcCRJ1_N0TbKR1OMujy3Bu_OnINFpgisznzOS78FA8NQdvVyEyl-Wg10n2gx2prlgUGzn0ahqPqPTQ68Xi4OXyZbxwc')
    except AuthError as e:
        raise Exception(f'Error connecting to Dropbox with access token: {str(e)}')
    return dbx

app.run(port=3000, host='localhost', debug=True)
