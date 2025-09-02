from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
import pytesseract
import spacy
import os, json

app = Flask(__name__, static_folder="../frontend", static_url_path="")

nlp = spacy.load("en_core_web_sm")

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    img = Image.open(f.stream).convert('RGB')
    text = pytesseract.image_to_string(img, lang='eng')
    doc = nlp(text)
    ents = [(ent.text, ent.label_) for ent in doc.ents]
    return jsonify({'text': text, 'entities': ents})

@app.route('/api/fra')
def get_fra():
    with open("../data/fra.geojson") as f:
        return jsonify(json.load(f))

@app.route('/api/water')
def get_water():
    with open("../data/water.geojson") as f:
        return jsonify(json.load(f))

@app.route('/api/veg')
def get_veg():
    with open("../data/veg.geojson") as f:
        return jsonify(json.load(f))

@app.route('/')
def root():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)

from dss import recommend

# @app.route('/api/recommendations')
# def recommendations():
#     # Demo record (would come from DB in real system)
#     record = {"land_size":0.5, "landholding_type":"smallholder", "is_farmer":True}
#     water_index = 0.1  # demo value
#     recs = recommend(record, water_index)
#     return jsonify(recs)
