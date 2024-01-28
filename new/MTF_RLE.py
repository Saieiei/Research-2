from PIL import Image
import itertools
import os
#

def move_to_front(encoding, symbol):
    if symbol in encoding:
        index = encoding.index(symbol)
        del encoding[index]
        encoding.insert(0, symbol)
    return encoding

def mtf_encode(data):
    encoding = list(range(256))  # Initialize MTF encoding as a list of integers from 0 to 255
    encoded_data = []
    
    for symbol in data:
        index = encoding.index(symbol)
        encoded_data.append(index)
        encoding = move_to_front(encoding, symbol)
    
    return encoded_data

def run_length_encode(data):
    encoded_data = []
    
    for symbol, group in itertools.groupby(data):
        run_length = len(list(group))
        encoded_data.extend([symbol, run_length])
    
    return encoded_data

def compress_image(image_path):
    # Load the image
    image = Image.open(image_path)
    image_data = list(image.tobytes())
    
    # Perform MTF encoding
    mtf_encoded_data = mtf_encode(image_data)
    
    # Perform Run-Length Encoding
    rle_encoded_data = run_length_encode(mtf_encoded_data)
    
    return rle_encoded_data

def calculate_compression_factor(original_size, compressed_size):
    return original_size / compressed_size

def main():
    # Specify the image file path
    image_path = "image/sample.jpg"
    
    # Perform MTF and RLE compression
    compressed_data = compress_image(image_path)
    
    # Calculate and display compression information
    original_image_size_bits = os.path.getsize(image_path) * 8       # 8 bits per byte
    compressed_size = len(compressed_data) * 8
    compression_factor = calculate_compression_factor(original_image_size_bits, compressed_size)

    print("MTF + RLE compression:")
    print("Original Size:", original_image_size_bits, "bits")
    print("Compressed Size:", compressed_size, "bits")
    print("Compression Factor:", compression_factor)

if __name__ == "__main__":
    main()
