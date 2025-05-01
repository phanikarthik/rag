import nltk
from nltk.tokenize import sent_tokenize
from nltk.data import find
import re

from textblob import TextBlob

def download_dependencies():
    try:
       # Check if 'punkt' tokenizer is already downloaded
       find('tokenizers/punkt')
    except LookupError:
       # If not found, download it quietly
       nltk.download('punkt', quiet=True)

def split_into_sentences(text):
    """
    Split text into sentences using basic punctuation marks.
    """
    sentence_endings = re.compile(r'(?<=[.!?]) +')  # Split after '.', '!', or '?' followed by a space
    sentences = sentence_endings.split(text)
    return sentences

def chunk_text_with_overlap(text_with_newline, doOverlapping = True, chunk_size=1000, overlap_size=200):
    """
    Chunks text into overlapping blocks using sentence boundaries from TextBlob.
    
    Args:
        text (str): The input text.
        chunk_size (int): Max characters in a chunk.
        overlap_size (int): Number of characters to overlap.

    Returns:
        List[str]: A list of text chunks.
    """
    text = text_with_newline.replace('\n', ' ')
    blob = TextBlob(text)
    sentences = [str(s) for s in blob.sentences]

    chunks = []
    current_chunk = ""

    if(doOverlapping):
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 > chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = current_chunk[-overlap_size:] + " " + sentence
            else:
                current_chunk += " " + sentence

        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        return chunks
    else:
        return sentences



#def chunk_text_with_overlap(text_with_newline, chunk_size=500, overlap_size=100):
    """
    Chunks a large text into smaller chunks with sentence boundaries and a specified overlap.

    Args:
        text (str): The large input text to chunk.
        chunk_size (int): Maximum size of each chunk (in characters).
        overlap_size (int): Number of overlapping characters between chunks.

    Returns:
        List of strings: A list where each string is a chunk of the input text.
    """

    text = text_with_newline.replace('\n', ' ')
    sentences = split_into_sentences(text)  # Split text into sentences manually
    chunks = []  # This will store all the text chunks
    current_chunk = ""  # Holds sentences for the current chunk
    current_length = 0  # Keeps track of the length of the current chunk
    
    for sentence in sentences:
        # If adding this sentence exceeds the chunk size, we finalize the current chunk
        if current_length + len(sentence) + 1 > chunk_size:
            chunks.append(current_chunk.strip())
            # Start the next chunk with the last `overlap_size` characters of the current chunk
            current_chunk = current_chunk[-overlap_size:] + " " + sentence
            current_length = len(current_chunk)
        else:
            current_chunk += " " + sentence
            current_length += len(sentence) + 1
    
    # Add any remaining text as a final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks