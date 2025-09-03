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

from dss import recommend
import numpy as np

def calculate_water_index(geojson_path):
    with open(geojson_path) as f:
        water_data = json.load(f)
    # Calculate total water area ratio from features
    total_area = 0
    water_area = 0
    for feature in water_data['features']:
        if 'area' in feature['properties']:
            area = feature['properties']['area']
            total_area += area
            if feature['properties'].get('isWater', True):  # Assuming water features
                water_area += area
    return water_area / max(total_area, 1e-6)  # Avoid division by zero

@app.route('/api/recommendations')
def recommendations():
    # Calculate real water index from water.geojson
    water_index = calculate_water_index("../data/water.geojson")
    
    # Get real record from FRA data
    with open("../data/fra.geojson") as f:
        fra_data = json.load(f)
    
    if fra_data['features']:
        # Use the first FRA record for demo
        props = fra_data['features'][0]['properties']
        record = {
            "land_size": props.get('area', 0.5),
            "landholding_type": "smallholder",  # This could be determined from area
            "is_farmer": True  # This could be determined from land use
        }
    else:
        # Fallback to demo data
        record = {"land_size":0.5, "landholding_type":"smallholder", "is_farmer":True}
    
    recs = recommend(record, water_index)
    return jsonify(recs)

if __name__ == '__main__':
    app.run(debug=True)
