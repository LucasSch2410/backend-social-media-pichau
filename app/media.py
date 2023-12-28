import csv, requests
import dropbox

from PIL import Image, ImageDraw, ImageFont
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
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
    """
    Scrap the HTML of the Google Sheet in the URL from the request
    """

    html = requests.get(request.json["sheet_url"]).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("tbody")
    products = []

    # Iterate across product lines
    for line in table:
        index = int(line.find('th').get_text())
        if index > 1:
            product = line.find('td').get_text()
            if product != "":
                products.append(product)
    return jsonify({"products": products})

# Production connection 
def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox('sl.Bsl4y581fMelsbwTc4XMn56KesbVjWX51-LyZ0DtHkPmtF54DkmWcFhT7oQPMyKjr97typUSgdw7SQg5aImwYkCZg0icWNZChh_-n0o7ysDW2Pz1w0RI9WyDobvMSF7lv-Xga25IfcJldr0qBe1jEZ8')
    except AuthError as e:
        raise Exception(f'Error connecting to Dropbox with access token: {str(e)}')
    return dbx

app.run(port=5000, host='localhost', debug=True)
