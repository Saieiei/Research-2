import os
from PIL import Image
import numpy as np

def bwt_transform(text):
    rotations = [text[i:] + text[:i] for i in range(len(text))]
    rotations.sort()
    bwt_transformed = ''.join(rot[-1] for rot in rotations)
    return bwt_transformed

def move_to_front_encode(text):
    alphabet = list(set(text))
    encoded = []
    for char in text:
        index = alphabet.index(char)
        encoded.append(index)
        # Move the character to the front of the alphabet
        alphabet.pop(index)
        alphabet.insert(0, char)
    return encoded

def calculate_compression_factor(original_size, compressed_size):
    return compressed_size / original_size  # Corrected the calculation

def process_image_in_chunks(file_path, chunk_size):
    with open(file_path, 'rb') as file:
        bwt_mtf_encoded = ""
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            chunk_str = chunk.decode('latin-1')
            
            # Perform BWT on the chunk
            bwt_transformed = bwt_transform(chunk_str)
            
            # Perform MTF on the BWT result
            mtf_encoded = move_to_front_encode(bwt_transformed)
            
            # Convert MTF result to string
            mtf_encoded_str = ''.join(map(str, mtf_encoded))
            
            bwt_mtf_encoded += mtf_encoded_str
        return bwt_mtf_encoded

if __name__ == "__main__":
    # Image file path
    image_file_path = "/workspaces/Research-2/image/sample.jpg"  # Replace with your actual image path

    # Chunk size for processing the image
    chunk_size = 1024

    # Perform BWT + MTF in chunks
    bwt_mtf_encoded = process_image_in_chunks(image_file_path, chunk_size)

    # Calculate sizes
    original_size_bits = os.path.getsize(image_file_path) * 8
    compressed_size_bits = len(bwt_mtf_encoded) * 8

    # Display BWT + MTF compression results
    print("BWT + MTF Compression:")
    print(f"Original Size: {original_size_bits} bits")
    print(f"Compression Size: {compressed_size_bits} bits")
    print(f"Compression Factor: {calculate_compression_factor(original_size_bits, compressed_size_bits)}")
