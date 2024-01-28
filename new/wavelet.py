import pywt
import numpy as np
import imageio
import os
#

def wavelet_compress(image_path, output_path):
    # Load the image
    image = imageio.imread(image_path)

    # Convert the image to grayscale if it's in color
    if len(image.shape) == 3:
        image = np.mean(image, axis=-1).astype(np.uint8)

    # Apply wavelet transform
    coeffs = pywt.dwt2(image, 'bior1.3')
    cA, (cH, cV, cD) = coeffs

    # Quantize coefficients (adjust the threshold for different compression ratios)
    threshold = 10
    cA[cA < threshold] = 0
    cH[cH < threshold] = 0
    cV[cV < threshold] = 0
    cD[cD < threshold] = 0

    # Reconstruct the compressed image
    compressed_image = pywt.idwt2((cA, (cH, cV, cD)), 'bior1.3')

    # Save the compressed image
    imageio.imwrite(output_path, compressed_image.astype(np.uint8))

def calculate_compression_factor(original_size, compressed_size):
    return original_size / compressed_size

def main():
    # Specify the image file path
    image_path = "image/sample.jpg"

    # Specify the output path for the compressed image
    output_path = "image/scompressed_image_wavelet.jpg"

    # Perform wavelet-based compression
    wavelet_compress(image_path, output_path)

    # Calculate and display compression information
    original_image_size_bits = os.path.getsize(image_path) * 8       # 8 bits per byte
    compressed_size = os.path.getsize(output_path) * 8
    compression_factor = calculate_compression_factor(original_image_size_bits, compressed_size)

    print("Wavelet-based compression:")
    print("Original Size:", original_image_size_bits, "bits")
    print("Compressed Size:", compressed_size, "bits")
    print("Compression Factor:", compression_factor)

if __name__ == "__main__":
    main()
