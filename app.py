from flask import Flask, request, jsonify
import openai
import tensorflow.keras.applications.mobilenet as mobilenet
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, origins=["http://localhost:5000", "http://127.0.0.1:5000"])

openai.api_key = "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"


@app.route('/generate_meme', methods=['POST'])
def generate_meme():
    img_file = request.files['img']
    img = Image.open(img_file.stream)
    img = img.resize((224, 224))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = mobilenet.preprocess_input(x)
    model = mobilenet.MobileNet(weights='imagenet', include_top=True)
    preds = model.predict(x)
    decode_preds = mobilenet.decode_predictions(preds)[0][0][1]

    prompt = f"generate a funny caption for a {decode_preds} image."
    print(prompt)
    response = openai.Completion.create(engine="text-davinci-002", 
prompt=prompt, max_tokens=20)
    meme_text = response['choices'][0]['text'].strip()
    print(meme_text)
    return jsonify({"meme_text": meme_text})

