import sys
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, jsonify, request

import dropbox
from dropbox.exceptions import AuthError

# from app.oauth.connection import authenticate_dropbox
from app.layouts.stories.stories_layout import InstagramLayout

app = Flask(__name__)

@app.route('/instagram', methods=['POST'])
def create_media():

    try:
        dbx = dropbox_connect()

        final_layout_image = InstagramLayout(request.json["product"], dbx)()

        if final_layout_image:
            final_layout_image.save("data/output/file.png")  # Save the image if successful
            return 'Success!'
        else:
            raise Exception("Error occurred during layout creation.")
    except AuthError as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500



@app.route('/sheet', methods=['POST'])
def scrap_sheet():
    return True

# Production connection 
def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox('sl.Bsi3zDT5sWq6xiYzSSojCKm8SfrysuzYPHfLvfbuCodL5KtLGZIZI6dH6BICl_7JurmCiX0COpZx-wuayWyQqWUhbo08mtGEqOacO8XWa0XxzVWXeBemJ7VmlEBWGJk-UeDGmrJdRN3czfhTmoXGD6c')
    except AuthError as e:
        raise Exception(f'Error connecting to Dropbox with access token: {str(e)}')
    return dbx

app.run(port=5000, host='localhost', debug=True)
