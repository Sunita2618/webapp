import streamlit as st
import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import requests
from bs4 import BeautifulSoup

# Function to display PDF content
def display_pdf(pdf_path):
    # Convert the selected PDF to a list of images
    pages = convert_from_path(pdf_path)

    st.title(f"PDF Viewer: {selected_pdf}")

    # Display each page as an image
    for page_num, page_image in enumerate(pages):
        st.image(page_image, caption=f"Page {page_num + 1}")

# Function to display web page content
def display_web_page(url):
    # Send an HTTP GET request to fetch the HTML content of the web page
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract and display the content you want (e.g., the article text)
        article_text = soup.find("div", class_="article-text")

        st.title("Web Page Viewer")

        if article_text:
            # Display the article text
            st.write(article_text.get_text())
        else:
            st.warning("Content not found on the page.")
    else:
        st.error("Failed to fetch the web page. Please check the URL.")

# Function to display images from a directory
def display_images(image_directory):
    # List all image files in the directory
    image_files = [f for f in os.listdir(image_directory) if f.endswith((".jpg", ".png", ".jpeg", ".gif"))]

    if image_files:
        st.title("Images")

        # Display each image in the directory
        for image_file in image_files:
            image_path = os.path.join(image_directory, image_file)
            st.image(image_path, caption=image_file, use_column_width=True)
    else:
        st.warning("No image files found in the directory.")

# Directory where your PDF files are located
pdf_directory = "webapp-pdf/pdf/"

# Directory where your image files are located
image_directory = "images/"

# List all PDF files in the directory
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith(".pdf")]

# Check if there are PDF files in the directory
if pdf_files:
    # Let the user select a PDF file or web page
    option = st.selectbox("Select an option", ["PDF"])

    if option == "PDF":
        # Let the user select a PDF file to display
        selected_pdf = st.selectbox("Select a PDF file", pdf_files)
        pdf_path = os.path.join(pdf_directory, selected_pdf)
        pdf_reader = PdfReader(pdf_path)
        num_pages = len(pdf_reader.pages)

        st.title(f"PDF Viewer: {selected_pdf}")
    
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            st.write(page.extract_text())
else:
    st.warning("No PDF files found in the directory.")

display_images(image_directory)
