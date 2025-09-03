<!-- # FRA Atlas Prototype

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
See backend/dss.py for simple scheme recommendation logic. -->

# 🌳 AI-Powered FRA Atlas & WebGIS DSS Prototype

## 📌 Overview
This project is a working prototype for the **AI-powered FRA Atlas and WebGIS-based Decision Support System (DSS)**.  
It demonstrates how **Forest Rights Act (FRA) claims** can be **digitized, mapped, and analyzed** alongside **AI-driven asset detection** (water, vegetation) to support decision-making and scheme allocation.  

The prototype integrates:
- **OCR digitization of FRA documents**  
- **AI-based asset mapping from satellite data (NDVI & NDWI)**  
- **WebGIS visualization with filters**  
- **Rule-based Decision Support System (DSS)** for recommending schemes  
- **Dashboard** with stats, OCR results, scheme recommendations, and filters  

---

## ⚙️ Workflow

### 1. **Data Collection & Digitization**
- FRA claim documents (PDF/JPEG) are uploaded.
- OCR (**Tesseract**) extracts text.
- NLP (**spaCy**) detects entities (patta holder, village, etc.).
- Records are standardized and stored.

### 2. **AI-Powered FRA Atlas**
- Sentinel-2 satellite bands processed using **Rasterio + Numpy**:
  - **NDVI** → detects vegetation/forest cover.
  - **NDWI** → detects water bodies (ponds, rivers).
- Binary masks are vectorized into **GeoJSON layers**.

### 3. **WebGIS Integration**
- **LeafletJS** frontend shows interactive layers:
  - FRA claims (IFR/CR/CFR)
  - Water bodies
  - Vegetation/forests
- Filters: by **State** and **Tribal Group**.
- Stats panel shows counts of claims and assets.

### 4. **Decision Support System (DSS)**
- Simple **rule-based engine** links FRA attributes + asset indices to government schemes.
- Example rules:
  - Low water availability → Recommend **Jal Shakti (borewell)**.
  - Smallholder farmer → Recommend **PM-KISAN**.
- Future scope: AI/ML models for smarter recommendations.

### 5. **Dashboard**
- **Upload section** → process FRA docs.
- **Recommendations panel** → DSS outputs.
- **Stats & Filters** → progress tracking by state/tribe.
- **Interactive map** → visualize assets and claims.

---

## 🛠️ Tools & Frameworks

### 🔹 Backend
- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/) – API & server
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) – text extraction
- [spaCy](https://spacy.io/) – NLP for entity recognition
- [Rasterio](https://rasterio.readthedocs.io/) – satellite raster processing
- [Numpy](https://numpy.org/) – NDVI/NDWI calculations
- [GeoPandas](https://geopandas.org/) – vector data handling
- [Shapely](https://shapely.readthedocs.io/) – geometry operations

### 🔹 Frontend
- [LeafletJS](https://leafletjs.com/) – interactive maps
- HTML/CSS/JavaScript – dashboard & UI

### 🔹 Database (Optional, for scaling)
- [PostgreSQL + PostGIS](https://postgis.net/) – spatial DB for FRA claims & assets

---

## 📦 Requirements

### System Dependencies
- Python 3.11+
- Tesseract OCR  
  - macOS: `brew install tesseract`  
  - Ubuntu: `sudo apt install tesseract-ocr`  
  - Windows: [Download here](https://github.com/UB-Mannheim/tesseract/wiki)

### Python Libraries
```bash
pip install flask pillow pytesseract spacy rasterio geopandas shapely numpy
python -m spacy download en_core_web_sm
