import sys
import ollama
import faiss
import numpy as np

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

# Each element in the VECTOR_DB will be a tuple (chunk, embedding)
# The embedding is a list of floats, for example: [0.1, 0.04, -0.34, 0.21, ...]
VECTOR_DB = []
TUPLES = []
def add_chunk_to_database(chunk):
  embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
  no_of_features_per_tuple = len(embedding)
  VECTOR_DB.append((chunk, embedding))
  TUPLES.append(embedding)

def cosine_similarity(a, b):
  dot_product = sum([x * y for x, y in zip(a, b)])
  norm_a = sum([x ** 2 for x in a]) ** 0.5
  norm_b = sum([x ** 2 for x in b]) ** 0.5
  return dot_product / (norm_a * norm_b)


def retrieve(query, top_n=3):
  query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]
  # temporary list to store (chunk, similarity) pairs
  similarities = []
  for chunk, embedding in VECTOR_DB:
    similarity = cosine_similarity(query_embedding, embedding)
    similarities.append((chunk, similarity))
  # sort by similarity in descending order, because higher similarity means more relevant chunks
  similarities.sort(key=lambda x: x[1], reverse=True)
  # finally, return the top N most relevant chunks
  return similarities[:top_n]

def main():
  dataset = []
  with open('sample_data.txt', 'r') as file:
    dataset = file.readlines()
    print(f'Loaded {len(dataset)} entries')

    for i, chunk in enumerate(dataset):
      add_chunk_to_database(chunk)
      print(f'Added chunk {i+1}/{len(dataset)} to the database')

  no_of_vectors_nb = len(dataset)
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

  index.nprobe = 10  # How many clusters to search in
  #sanity_q = xb_np[:1]
  #D, I = index.search(sanity_q, k=5) # sanity check
  #print(I)
  #print(D)

  input_query = input('Ask me a question: ')
  query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=input_query)['embeddings'][0]
  Q_TUPLE = []
  Q_TUPLE.append(query_embedding)
  query_np = np.array(Q_TUPLE).astype('float32')
  D, I = index.search(query_np, k=5)
  print(I)
  print(D)

  #retrieved_knowledge = retrieve(input_query)

  print('Retrieved knowledge:')
  chunks_collection = []
  #print(VECTOR_DB[I][0])
  for index in I[0]:
     chunk = VECTOR_DB[int(index)][0]
     print(chunk)
     chunks_collection.append(chunk)

  context = "\n".join(chunks_collection)
  #for chunk, similarity in retrieved_knowledge:
  #  print(f' - (similarity: {similarity:.2f}) {chunk}')

  instruction_prompt = f"""You are a helpful chatbot.
  Use only the following pieces of context to answer the question. Don't make up any new information:
  Context: {context}
  Question: {input_query}
  Answer: """

  stream = ollama.chat(
  model=LANGUAGE_MODEL,
  messages=[
    {'role': 'user', 'content': instruction_prompt},
  ],
  stream=True,
  )

  print('Chatbot response:')
  for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
  print("Hello, World!")


if __name__ == "__main__":
    main()
