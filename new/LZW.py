import zlib
import os

def compress_image(image_path, output_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()

    compressed_data = zlib.compress(image_data, level=zlib.Z_BEST_COMPRESSION)

    with open(output_path, 'wb') as f:
        f.write(compressed_data)

def calculate_compression_factor(original_size, compressed_size):
    return original_size / compressed_size

def main():
    # Specify the image file path
    image_path = "image/sample.jpg"

    # Specify the output path for the compressed image
    output_path = "image/compressed_image_lzw.jpg"

    # Perform LZW-based compression
    compress_image(image_path, output_path)

    # Calculate and display compression information
    original_image_size_bits = os.path.getsize(image_path) * 8       # 8 bits per byte
    compressed_size = os.path.getsize(output_path) * 8
    compression_factor = calculate_compression_factor(original_image_size_bits, compressed_size)

    print("LZW-based compression:")
    print("Original Size:", original_image_size_bits, "bits")
    print("Compressed Size:", compressed_size, "bits")
    print("Compression Factor:", compression_factor)

if __name__ == "__main__":
    main()
