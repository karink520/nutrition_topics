import pdfplumber
import os
import fitz
import pytesseract
from PIL import Image
from tempfile import TemporaryDirectory

def get_date_list_from_filenames(filenames):
    """
    Extracts years from a list of filenames each ending in YYYY.xyz
    where xyz is any three-character file extension

    Parameters:
    -----------
    filenames : list of str
        Each element is a filename ending in YYYY.pdf or YYYY.txt
    Returns:
    --------
    years :list of int
        List, length the same as length of filenames,
        each element giving the year of the coresponding
        paper
    """

    years = []
    for filename in filenames:
        years.append(int(filename[-8:-4]))
    return years


def pdf_to_text_via_ocr(pdf_file, out_directory):
    """
    Convert a pdf file to text via ocr and save the output.
    
    Parameters:
    -----------
    pdf_file: str
        Assumed to be of the format DIRECTORY_NAME/filename.pdf
    out_directory: str
        E.g. 'level2_txt_ocr'

    Notes:
    ------
    Partially adapted from https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
    """
    
    # create path to output file
    article_filename = PDF_file.split("/")[-1]
    article_filename_root = article_filename.split(".")[0]
    text_file = out_directory + "/" + article_filename_root + ".txt" # output file

     # Store all the pages of the PDF in a variable
    image_file_list = []

    with TemporaryDirectory() as tempdir:
        # Create a temporary directory to hold our temporary images.

        # 1. Convert PDF to images
        doc = fitz.open(PDF_file)
        page_enumeration = 1

        # Iterate through pages and convert to image
        for page in doc:
            # Create a file name to store the image
            filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
            # save the image
            pix = page.get_pixmap()
            pix.save(filename, "JPEG")
            image_file_list.append(filename)
            page_enumeration+=1

        # 2. Convert image to text via ocr
        with open(text_file, "a") as output_file:
            # Process the image of each page
            for image_file in image_file_list:

                # Recognize the text as string in image using pytesserct
                text = str(((pytesseract.image_to_string(Image.open(image_file)))))
                # Process hyphens at the end of a line
                text = text.replace("-\n", "")

                # Finally, write the processed text to the file.
                output_file.write(text)


def create_doc_list_from_pdfs(pdf_filenames, txt_directory, to_txt=False):
    """
    Parses a list of pdfs whose filepaths are given, and optionally
    saves the results to .txt files in the given directory.

    Parameters:
    -----------
    pdf_filenames : list of str
        paths to pdf to be parsed
        
    Returns:
    --------
    documents: list of str
        list of strings, one for each paper whose pdf was processed
    txt_directory: str
        If to_txt is true, this is where .txx files get saved, one for
        each pdf in pdf_filnames.
    to_txt: bool
        If true, save the parsed text from each pdf to a .txt file 
        within txt_directory
    """
    
    documents = []
    for filename in pdf_filenames:
        doc_text = ''
        print(filename)
        paper_pdf = pdfplumber.open(filename)
        for page in paper_pdf.pages:
         #Get text info from each page
            doc_text += ' '
            doc_text += page.extract_text(x_tolerance=2, use_text_flow=True,) 
        paper_pdf.close()
        documents.append(doc_text)
        
        if to_txt:
            filename_short = filename.split('/')[1][:-4]
            with open(txt_directory + '/' + filename_short + '.txt', 'w') as f:
                f.write(doc_text)
            
    return documents


def load_documents_from_txt(txt_directory):
    """
    Given a directory containing only a list of .txt files, extracts
    the text from each file and returns a list giving the text for
    each document

    Parameters:
    -----------
    txt_directory : str
        directory containing (only) .txt files to put into the doc list
        
    Returns:
    --------
    documents: list of str
        list of strings, one for each paper whose txt file was processed
    """
    documents = []
    years = []
    refids = []
    txt_filenames = [txt_directory + '/' + f for f in os.listdir(txt_directory) if not f.startswith(".")]
    for txt_filename in txt_filenames:
        doc_text = ''
        with open(txt_filename) as f:
            lines = f.readlines()
            for line in lines:
                doc_text += line
        documents.append(doc_text)
        year = int(txt_filename[-8:-4])
        years.append(year)
        refid =  txt_filename.split("/")[-1].split("-")[0] # get ints after / and before -
        refids.append(refid)
        
    return documents, years, refids, txt_filenames

            