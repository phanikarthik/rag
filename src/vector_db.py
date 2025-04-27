import ollama
import faiss
import numpy as np
from customer_files.config import EMBEDDING_MODEL, LANGUAGE_MODEL, INPUT_FILE_NAME
from pathlib import Path
import sqlite3
import pickle
from tqdm import tqdm

VECTOR_DB = []
TUPLES = []
global_sql3_db_sanity_check = False

def prepare_lists_for_database(chunk, sqlite_cur, idx):
  embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
  no_of_features_per_tuple = len(embedding)
  sqlite_cur.execute("INSERT INTO chunks (id, text) VALUES (?, ?)", (idx, chunk))

  global global_sql3_db_sanity_check, VECTOR_DB, TUPLES
  if(global_sql3_db_sanity_check):
      VECTOR_DB.append((chunk, embedding))

  TUPLES.append(embedding)


def create_IVFPQ_db(data, sqlite_db_sanity_check = False):

    global global_sql3_db_sanity_check, VECTOR_DB, TUPLES
    if(sqlite_db_sanity_check):
       global_sql3_db_sanity_check = True

    # Connect to SQLite DB (creates the file if it doesn't exist)
    conn = sqlite3.connect("faiss_chunks.db")
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY,
            text TEXT NOT NULL
        )
    ''')

    for i, chunk in tqdm(enumerate(data), desc="Number of chunks added to database", unit=" chunks", total = len(data)):
        prepare_lists_for_database(chunk, cursor, i)
        #print(f'Added chunk {i+1}/{len(data)} to the database')
    
    conn.commit()
    conn.close()

    if(global_sql3_db_sanity_check):
        # Save to a file
        with open("my_list.pkl", "wb") as f:
          pickle.dump(VECTOR_DB, f)

    no_of_vectors_nb = len(data)
    no_of_features_per_vector_d = len(TUPLES[0])
    no_of_subvectors_per_vector_m = 32
    subvectors_encode_length_n_bits = 4 #8
    no_of_clusters_n_list = round(no_of_vectors_nb ** 0.5) #sqrt(no_of_vectors_nb)

    # 2. Create a flat quantizer (used for coarse clustering)
    #quantizer is a helper index used to find which cluster a vector belongs to.
    quantizer = faiss.IndexFlatL2(no_of_features_per_vector_d)

    index = faiss.IndexIVFPQ(quantizer, no_of_features_per_vector_d, no_of_clusters_n_list, no_of_subvectors_per_vector_m, subvectors_encode_length_n_bits)
    xb_np = np.array(TUPLES).astype('float32')
    index.train(xb_np)
    index.add(xb_np)

    folder = Path("customer_files")
    op_file = INPUT_FILE_NAME
    if not op_file.endswith(".ivfpq"):
        op_file += ".ivfpq"

    op_file = folder / op_file

    faiss.write_index(index, str(op_file))
    print(f"Saved the databse as {op_file} using FAISS version: {faiss.__version__}")
    return index