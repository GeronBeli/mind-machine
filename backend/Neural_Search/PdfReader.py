"""
PDF Helper Functions

Author: Abdelrahman Elsharkawi
Creation Date: 11.11.2023
"""
import PyPDF2
from Neural_Search.DocVec import DocVec
import re
import logHandler
logger = logHandler.LogHandler(name="PdfReader").get_logger()

def split_string_to_chunks(input_string, chunk_length, overlap):
    """
    Splits an input string into chunks of specified length with a given overlap.

    Args:
        input_string (str): The input string to be split into chunks.
        chunk_length (int): The desired length of each chunk.
        overlap (int): The number of words to overlap between consecutive chunks.

    Returns:
        list: A list of chunks, where each chunk is a string of words.

    """
    words = input_string.split()
    chunks = []

    while words:
        chunk = ' '.join(words[:chunk_length])
        chunks.append(chunk)
        words = words[chunk_length - overlap:]

    return chunks

def pdf_to_text(path, chunk_length, overlap):
    """
    Convert PDF file to plain text.

    Parameters:
    - path (str): Path to the PDF file.

    Returns:
    dict: {'text':extracted_text, 'paragraphs':paragraphs}.
    """
    pdffileobj=open(path,'rb')
    pdfreader=PyPDF2.PdfReader(pdffileobj)
    extracted_text = ""
    paragraphs = []

    for page in pdfreader.pages:
        extracted_text += page.extract_text()

    paragraphs = split_string_to_chunks(extracted_text, chunk_length, overlap)
    return {'text':extracted_text, 'paragraphs':paragraphs}

def pdf_to_docVec(path, encoder, chunk_length = 0, remove_stop_words=False, overlap = 30):
    """
    Convert PDF file to DocVec object.

    Parameters:
    - path (str): Path to the PDF file.
    - encoder: Sentence embeddings encoder.

    Returns:
    DocVec: DocVec object containing document vectors and paragraph vectors.
    """
    if chunk_length == 0:
        chunk_length = encoder.max_seq_length
    doc = pdf_to_text(path, chunk_length, overlap)
    paras_vecs = []
    for idp, para in enumerate(doc['paragraphs']):
        paras_vecs.append({"paragraph":para,"vec":encoder.encode(para).tolist()})
        #print(paras_vecs)
        logger.debug(f"Paragraph {idp} vectorized: {para}")


    return DocVec(path, doc['text'], paras_vecs)
