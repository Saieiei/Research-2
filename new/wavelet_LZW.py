import cv2
import pywt
import numpy as np
import zlib
import lzw
#


def read_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return image

def wavelet_lzw_compress(image):
    # Step 1: Wavelet Compression
    coeffs = pywt.dwt2(image, 'haar')
    
    # Select a subset of coefficients (you can customize the selection criteria)
    compressed_coeffs = select_coefficients(coeffs)
    
    # Convert coefficients to bytes
    coefficients_bytes = np.array(compressed_coeffs).tobytes()

    # Step 2: LZW Compression
    compressed_data = zlib.compress(coefficients_bytes)

    return compressed_data

def select_coefficients(coeffs):
    # Example: Keep only the top-left quadrant of the LL subband
    return [coeffs[0][:len(coeffs[0])//2, :len(coeffs[0][0])//2]]

def decompress_wavelet_lzw(compressed_data, original_shape):
    # Separate the compressed data into wavelet coefficients and LZW compressed data
    compressed_coeffs, lzw_compressed_data = compressed_data

    # Decompress LZW
    decompressed_data = lzw.decompress(lzw_compressed_data)

    # Convert the decompressed data to numpy array
    decompressed_data = np.frombuffer(decompressed_data, dtype=np.uint8)

    # Reshape the decompressed data to the original shape
    decompressed_image = decompressed_data.reshape(original_shape)

    # Perform inverse wavelet transform
    reconstructed_image = pywt.idwt2(compressed_coeffs, 'haar')

    return reconstructed_image

# Load the image
image_path = "/workspaces/Research-2/image/sample3.jpg"
original_image = read_image(image_path)

# Apply compression
compressed_data = wavelet_lzw_compress(original_image)

# Decompress and reconstruct the image
reconstructed_image = decompress_wavelet_lzw(compressed_data, original_image.shape)

# Save the reconstructed image
cv2.imwrite("/workspaces/Research-2/image/reconstructed_image.jpg", reconstructed_image)
