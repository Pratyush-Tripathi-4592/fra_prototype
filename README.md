# FRA Atlas Prototype

## Setup
```bash
cd backend
pip install flask pillow pytesseract spacy
python -m spacy download en_core_web_sm
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Features
- OCR endpoint: POST /upload (upload scanned FRA doc)
- GeoJSON endpoints: /api/fra, /api/water, /api/veg
- Frontend: Leaflet map (shows FRA claims, water bodies, vegetation)

## DSS
See backend/dss.py for simple scheme recommendation logic.
