import os
#1.0

def bwt_transform(text):
    rotations = [text[i:] + text[:i] for i in range(len(text))]
    rotations.sort()
    bwt_transformed = ''.join(rot[-1] for rot in rotations)
    return bwt_transformed

def calculate_compression_factor(original_size, compressed_size):
    return original_size / compressed_size

def process_image_in_chunks(file_path, chunk_size):
    with open(file_path, 'rb') as file:
        bwt_transformed = ""
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            chunk_str = chunk.decode('latin-1')
            bwt_transformed += bwt_transform(chunk_str)
        return bwt_transformed

if __name__ == "__main__":
    # Image file path
    image_file_path = "/workspaces/Research-2/image/sample3.jpg"

    # Chunk size for processing the image
    chunk_size = 1024

    # Perform BWT in chunks
    bwt_transformed = process_image_in_chunks(image_file_path, chunk_size)

    # Calculate sizes
    original_size_bits = os.path.getsize(image_file_path) * 8
    compressed_size_bits = len(bwt_transformed) * 8

    # Display BWT results
    print("BWT Compression:")
    print(f"Original Size: {original_size_bits} bits")
    print(f"Compression Size: {compressed_size_bits} bits")
    print(f"Compression Factor: {calculate_compression_factor(original_size_bits, compressed_size_bits)}")
