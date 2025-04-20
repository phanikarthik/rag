import sys
import ollama
import faiss
import numpy as np
from config import EMBEDDING_MODEL, LANGUAGE_MODEL, INPUT_FILE_NAME
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

  index = faiss.read_index("sample_data.ivfpq")
  index.nprobe = 10  # How many clusters to search in
  input_query = input('Ask me a question: ')
  query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=input_query)['embeddings'][0]
  Q_TUPLE = []
  Q_TUPLE.append(query_embedding)
  query_np = np.array(Q_TUPLE).astype('float32')
  D, I = index.search(query_np, k=5)
 
 

  print('Retrieved knowledge:')
  chunks_collection = []
  for i in I[0]:
     chunk = VECTOR_DB[int(i)][0]
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
 


if __name__ == "__main__":
    main()
