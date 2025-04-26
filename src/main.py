import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import ollama
import faiss
import numpy as np
from customer_files.config import EMBEDDING_MODEL, LANGUAGE_MODEL, INPUT_FILE_NAME
from vector_db import create_IVFPQ_db, VECTOR_DB, TUPLES


# Each element in the VECTOR_DB will be a tuple (chunk, embedding)
# The embedding is a list of floats, for example: [0.1, 0.04, -0.34, 0.21, ...]



def cosine_similarity(a, b):
  dot_product = sum([x * y for x, y in zip(a, b)])
  norm_a = sum([x ** 2 for x in a]) ** 0.5
  norm_b = sum([x ** 2 for x in b]) ** 0.5
  return dot_product / (norm_a * norm_b)




def main():
  dataset = []
  ip_file = INPUT_FILE_NAME

  if not ip_file.endswith(".txt"):
    ip_file += ".txt"

  with open(ip_file, 'r') as file:
    dataset = file.readlines()
    print(f'Loaded {len(dataset)} entries')
  
  create_IVFPQ_db(dataset)



if __name__ == "__main__":
    main()
