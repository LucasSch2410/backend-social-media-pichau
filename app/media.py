import csv, requests
import dropbox

from PIL import Image, ImageDraw, ImageFont
from flask import Flask, jsonify, request, redirect
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


# Auth2 redirect
@app.route('/auth2', methods=['GET'])
def auth2():
    authorization_code = str(request.args.get('code'))
    token_url = "https://api.dropboxapi.com/oauth2/token"
    params = {
        "code": authorization_code,
        "grant_type": 'authorization_code',
        "redirect_uri": 'http://localhost:5000/auth2',
        "client_id": 'emm8mikk0bmdwbn',
        "client_secret": 'ldxj4yfnixjfhdz'
    }

    r = requests.post(token_url, data=params)

    if r.status_code != 200:
        return f'Error {r}'
    
    access_token = r.json()['access_token']
    
    return redirect(f'http://localhost:5173?access_token={access_token}')


# Production connection 
def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox('sl.Bsl4y581fMelsbwTc4XMn56KesbVjWX51-LyZ0DtHkPmtF54DkmWcFhT7oQPMyKjr97typUSgdw7SQg5aImwYkCZg0icWNZChh_-n0o7ysDW2Pz1w0RI9WyDobvMSF7lv-Xga25IfcJldr0qBe1jEZ8')
    except AuthError as e:
        raise Exception(f'Error connecting to Dropbox with access token: {str(e)}')
    return dbx

app.run(port=5000, host='localhost', debug=True)
