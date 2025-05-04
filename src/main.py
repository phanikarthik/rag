import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import ollama
import faiss
import numpy as np
from customer_files.config import EMBEDDING_MODEL, LANGUAGE_MODEL, INPUT_FILE_NAME
from vector_db import create_IVFPQ_db, VECTOR_DB, TUPLES
from chunking import chunk_text_with_overlap
from textblob import TextBlob
from pdfminer.high_level import extract_text
from pdfminer.pdfpage import PDFPage
from tqdm import tqdm

# Each element in the VECTOR_DB will be a tuple (chunk, embedding)
# The embedding is a list of floats, for example: [0.1, 0.04, -0.34, 0.21, ...]



def cosine_similarity(a, b):
  dot_product = sum([x * y for x, y in zip(a, b)])
  norm_a = sum([x ** 2 for x in a]) ** 0.5
  norm_b = sum([x ** 2 for x in b]) ** 0.5
  return dot_product / (norm_a * norm_b)


def process_pdf(ip_file):

  if not ip_file.endswith(".pdf"):
    ip_file += ".pdf"
  
  #page_texts = []
  all_pages_sentences = []
  cur_page_sentences = []
  with open(ip_file, 'rb') as f:
    for i, page in tqdm(enumerate(PDFPage.get_pages(f), start=1), desc = 'Reading pages', unit=" pages"):
        cur_page_text = extract_text(ip_file, page_numbers=[i-1])  # 0-based index
        cur_page_text_striped = cur_page_text.strip()
        cur_page_sentences = chunk_text_with_overlap(cur_page_text_striped, False) #not tested with True param
        #all_pages_sentences.extend(cur_page_sentences)

        # Store each chunk with metadata
        for chunk in cur_page_sentences:
            all_pages_sentences.append({
                "page_no": i,
                "chapter": "-",
                "text": chunk
            })

        #page_texts.append((i, cur_page_text_striped))

  return all_pages_sentences



def main():
  annotated_sentences = process_pdf(INPUT_FILE_NAME)
  create_IVFPQ_db(annotated_sentences, True)


if __name__ == "__main__":
    main()
