import imageio
from fic import encode, decode

def compress_image(input_path, output_path):
    image = imageio.imread(input_path)
    compressed_data = encode(image)
    with open(output_path, 'wb') as file:
        file.write(compressed_data)

def decompress_image(input_path, output_path):
    with open(input_path, 'rb') as file:
        compressed_data = file.read()
    decompressed_image = decode(compressed_data)
    imageio.imsave(output_path, decompressed_image)

# Example usage
input_image_path = "/workspaces/Research-2/image/sample3.jpg"
compressed_image_path = "/workspaces/Research-2/image/compressed.fic"
decompressed_image_path = "/workspaces/Research-2/image/decompressed.jpg"

# Compression
compress_image(input_image_path, compressed_image_path)

# Decompression
decompress_image(compressed_image_path, decompressed_image_path)
