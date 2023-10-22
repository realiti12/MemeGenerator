from flask import Flask
from flask_cors import CORS

CORS(app)

app = Flask(__name__)

from flask import request
from PIL import Image

@app.route('/generate_meme', methods=['POST'])
def generate_meme():
    img_file = request.files['img']
    img = Image.open(img_file.stream)
    return "Image received"

