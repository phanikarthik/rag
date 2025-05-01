import nltk
from nltk.tokenize import sent_tokenize
from nltk.data import find
import re

def download_dependencies():
    try:
       # Check if 'punkt' tokenizer is already downloaded
       find('tokenizers/punkt')
    except LookupError:
       # If not found, download it quietly
       nltk.download('punkt', quiet=True)

def chunk_text_with_sentence_overlap(text, chunk_size=1000, overlap_size=200):
    download_dependencies()
    """
    Splits a large text into chunks by sentence boundaries, maintaining overlap between chunks.

    Args:
        text (str): The large text to split and chunk.
        chunk_size (int): Maximum size (in characters) for each chunk.
        overlap_size (int): Overlapping size (in characters) between chunks.

    Returns:
        List[str]: A list of chunked texts.
    """
    sentences = sent_tokenize(text)  # Split into sentences
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # If adding this sentence exceeds the chunk size
        if len(current_chunk) + len(sentence) + 1 > chunk_size:
            chunks.append(current_chunk.strip())
            # Start the next chunk with the last `overlap_size` characters
            current_chunk = current_chunk[-overlap_size:] + " " + sentence
        else:
            current_chunk += " " + sentence
    
    # Add any remaining text as a final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def split_into_sentences(text):
    """
    Split text into sentences using basic punctuation marks.
    """
    sentence_endings = re.compile(r'(?<=[.!?]) +')  # Split after '.', '!', or '?' followed by a space
    sentences = sentence_endings.split(text)
    return sentences

#def chunk_text_with_overlap(text, chunk_size=1000, overlap_size=200):
    """
    Chunks a large text into smaller chunks with a specified overlap.

    Args:
        text (str): The large input text to chunk.
        chunk_size (int): Size of each chunk (in characters).
        overlap_size (int): Number of overlapping characters between chunks.

    Returns:
        List of strings: A list where each string is a chunk of the input text.
    """
    chunks = []  # This will store all the text chunks
    start = 0  # The starting index of the current chunk
    
    # Iterate through the text to create chunks
    while start < len(text):
        # Define the end of the chunk (it should not exceed the text length)
        end = start + chunk_size
        
        # Add the chunk to the list
        chunks.append(text[start:end])
        
        # Move the starting point forward by chunk_size - overlap_size
        start = end - overlap_size
        
    return chunks

def chunk_text_with_overlap(text_with_newline, chunk_size=500, overlap_size=100):
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