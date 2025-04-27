import sys
import ollama
import faiss
import numpy as np
from config import EMBEDDING_MODEL, LANGUAGE_MODEL, INPUT_FILE_NAME

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import sqlite3
import pickle

def retrieve_chunks(indices):
    # Connect to your SQLite database
    conn = sqlite3.connect("faiss_chunks.db")
    cursor = conn.cursor()

    # Build a SQL query to get texts by IDs
    placeholders = ",".join("?" * len(indices))  # Creates "?, ?, ?" based on number of indices
    sql = f"SELECT id, text FROM chunks WHERE id IN ({placeholders})"

    # Execute the query
    cursor.execute(sql, list(indices))
    rows = cursor.fetchall()

    conn.close()

    return rows

def answer_query(sqlite_db_sanity_check = False):
   # Connect to your SQLite database
   conn = sqlite3.connect("faiss_chunks.db")
   cursor = conn.cursor()

   if(sqlite_db_sanity_check):
       # Load from file
       with open("my_list.pkl", "rb") as f:
          VECTOR_DB = pickle.load(f)

   VECTOR_DB_LIST = []
   index = faiss.read_index("customer_files/sample_data.ivfpq")
   index.nprobe = 10  # How many clusters to search in
   input_query = input('Ask me a question: ')
   query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=input_query)['embeddings'][0]
   Q_TUPLE = []
   Q_TUPLE.append(query_embedding)
   query_np = np.array(Q_TUPLE).astype('float32')
   D, I = index.search(query_np, k=5)

   print('Retrieved knowledge:')

   if(sqlite_db_sanity_check):
      for i in I[0]:
         chunk = VECTOR_DB[int(i)][0]
         print(chunk)
         VECTOR_DB_LIST.append(chunk)

   print('Retrieved knowledge from sqlite database:')
   indices = I[0].tolist()
   rows = retrieve_chunks(indices)

   chunks_collection = []
   # Display results
   for id, text in rows:
      print(f"[{id}] {text}\n")
      chunks_collection.append(text)

   if(sqlite_db_sanity_check):
      if(sorted(VECTOR_DB_LIST) == sorted(chunks_collection)):
         print('SQLITE database sanity check PASS. PROCEED')
      else:
         print('SQLITE database sanity check FAIL! .')
         print('SQLITE database has retrieved different chunks as in the local list')
         sys.exit(1)

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

def main():
   answer_query(True)

if __name__ == "__main__":
    main()
