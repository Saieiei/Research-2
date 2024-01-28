import imageio
import numpy as np
from skimage import color
from sklearn.decomposition import PCA
import os

def compress_image(image_path, output_path, components=0):
    # Read the image
    image = imageio.imread(image_path)

    # Convert the image to grayscale
    grayscale_image = color.rgb2gray(image)

    # Apply PCA for dimensionality reduction
    pca = PCA(n_components=components)
    compressed_image = pca.fit_transform(grayscale_image)

    # Reconstruct the compressed image
    reconstructed_image = pca.inverse_transform(compressed_image)

    # Save the compressed image
    imageio.imwrite(output_path, reconstructed_image)

def calculate_compression_factor(original_size, compressed_size):
    return original_size / compressed_size

def main():
    # Specify the image file path
    image_path = "image/sample3.jpg"

    # Specify the output path for the compressed image
    output_path = "/workspaces/Research-2/image/compressed_output2.txt"

    # Perform DCT-based compression
    compress_image(image_path, output_path)

    # Calculate and display compression information
    original_image_size_bits = os.path.getsize(image_path) * 8       # 8 bits per byte
    compressed_size = os.path.getsize(output_path) * 8
    compression_factor = calculate_compression_factor(original_image_size_bits, compressed_size)

    print("DCT-based compression:")
    print("Original Size:", original_image_size_bits, "bits")
    print("Compressed Size:", compressed_size, "bits")
    print("Compression Factor:", compression_factor)

if __name__ == "__main__":
    main()
