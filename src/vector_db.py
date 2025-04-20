import ollama
import faiss
import numpy as np
from config import EMBEDDING_MODEL, LANGUAGE_MODEL, INPUT_FILE_NAME

VECTOR_DB = []
TUPLES = []

def prepare_lists_for_database(chunk):
  embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
  no_of_features_per_tuple = len(embedding)
  VECTOR_DB.append((chunk, embedding))
  TUPLES.append(embedding)

def create_IVFPQ_db(data):
    for i, chunk in enumerate(data):
        prepare_lists_for_database(chunk)
        print(f'Added chunk {i+1}/{len(data)} to the database')
    
    no_of_vectors_nb = len(data)
    no_of_features_per_vector_d = len(VECTOR_DB[0][1])
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

    op_file = INPUT_FILE_NAME
    if not op_file.endswith(".ivfpq"):
        op_file += ".ivfpq"

    faiss.write_index(index, op_file)
    print(f"Saved the databse as {op_file} using FAISS version: {faiss.__version__}")
    return index