import os
#


def run_length_encode(data):
    encoded_data = []
    count = 1

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data.append((data[i - 1], count))
            count = 1

    encoded_data.append((data[-1], count))
    return encoded_data

def compress_image_rle(image_path, output_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()

    encoded_data = run_length_encode(image_data)

    with open(output_path, 'wb') as f:
        for symbol, count in encoded_data:
            f.write(bytes([symbol]))
            f.write(count.to_bytes(2, byteorder='big'))

def calculate_compression_factor(original_size, compressed_size):
    return original_size / compressed_size

def main():
    # Specify the image file path
    image_path = "image/sample3.jpg"

    # Specify the output path for the compressed image
    output_path = "image/compressed_image_rle.jpg"

    # Perform RLE-based compression
    compress_image_rle(image_path, output_path)

    # Calculate and display compression information
    original_image_size_bits = os.path.getsize(image_path) * 8       # 8 bits per byte
    compressed_size = os.path.getsize(output_path) * 8
    compression_factor = calculate_compression_factor(original_image_size_bits, compressed_size)

    print("RLE-based compression:")
    print("Original Size:", original_image_size_bits, "bits")
    print("Compressed Size:", compressed_size, "bits")
    print("Compression Factor:", compression_factor)

if __name__ == "__main__":
    main()
