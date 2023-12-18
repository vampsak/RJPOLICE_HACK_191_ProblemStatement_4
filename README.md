# FIR Analysis Project 🕵️‍♂️📋

This project utilizes OCR (Optical Character Recognition) and other technologies to analyze Sample First Information Reports (FIRs) and extract crucial information. The goal is to provide insights into crime types, details, and related legal sections.

## Project Overview 📑

The project involves the following key components:

1. **OCR and Text Extraction**: Utilizes the EasyOCR library for OCR to extract text and bounding boxes from images of FIRs.

2. **Crime Information Extraction**: Parses the OCR results to identify the crime type and details. Draws bounding boxes around relevant information on the image.

3. **PDF Search**: Converts PDFs containing Indian crime laws into images and performs keyword searches using regular expressions. Identifies matches and extracts related legal section numbers.

4. **IndiaCode Integration**: Searches on the IndiaCode platform to find additional information related to the identified crime type.

## How to Use 🚀

1. **Image Processing**: Provide the path to the image of the FIR (`SampleFIR.png`) to initiate the analysis.

2. **Visualization**: The image will be displayed with bounding boxes around the identified crime type and details.

3. **PDF Search**: If crime information is complete, the project searches a PDF file (`criminal_laws.pdf`) for matches, highlighting type and details, and providing section numbers.

4. **IndiaCode Integration**: Additional information related to the crime type is fetched from the IndiaCode platform.

## Important Note 📝

- **Sample Data**: The project is currently using sample FIR data (`SampleFIR.png`) and a document of crime laws (`criminal_laws.pdf`) for analysis.

- **Section Identification**: In further development, the project aims to identify specific legal sections related to the identified crime types.

- **Web Scraping**: The project includes web scraping from the IndiaCode site to enhance the information retrieval process.

## Requirements 🛠️

Make sure you have the following Python libraries installed:

- `re`
- `easyocr`
- `requests`
- `bs4` (BeautifulSoup)
- `pdf2image`
- `matplotlib`
- `PIL` (Pillow)

Install any missing libraries using:

```bash
pip install library_name
