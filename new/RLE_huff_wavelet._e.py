import pywt
import heapq
import numpy as np
from skimage import io as imageio  # Import the 'io' submodule from skimage as imageio

def run_length_encode(data):
    encoded_data = []
    current_run = [data[0], 1]

    for pixel in data[1:]:
        if pixel == current_run[0]:
            current_run[1] += 1
        else:
            encoded_data.append(tuple(current_run))
            current_run = [pixel, 1]

    encoded_data.append(tuple(current_run))
    return encoded_data


def huffman_compress(data):
    frequency_table = dict.fromkeys(data, 0)

    for symbol in data:
        frequency_table[symbol] += 1

    heap = [(-frequency, [symbol, ""]) for symbol, frequency in frequency_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, (lo[0] + hi[0], lo[1:] + hi[1:]))

    code_table = dict(heapq.heappop(heap)[1:])
    
    # Encode data using the generated Huffman codes
    compressed_data = ''.join(code_table[symbol] for symbol, _ in data)

    return compressed_data, code_table



def wavelet_compress(data, wavelet='haar', level=1):
    # Apply 2D wavelet transform
    coeffs = pywt.wavedec2(data, wavelet, level=level)

    # Discard high-frequency coefficients (details)
    coeffs = [coeff if i == 0 else None for i, coeff in enumerate(coeffs)]

    # Reconstruct the image from modified coefficients
    reconstructed_data = pywt.waverec2(coeffs, wavelet)

    return reconstructed_data


def main():
    # Image file path
    image_file_path = "/workspaces/Research-2/image/sample3.jpg"

    # Load the image
    image = imageio.imread(image_file_path)

    # Flatten the image data
    image_data = image.flatten()

    # Run-Length Encoding
    encoded_data = run_length_encode(image_data)

    # Huffman Compression
    compressed_data, code_table = huffman_compress(encoded_data)

    # Wavelet Compression
    wavelet_compressed_data = wavelet_compress(image, wavelet='haar', level=1)

    # Calculate and display compression information
    original_size_bits = len(image_data) * 8
    compressed_size = len(compressed_data)
    compression_factor = original_size_bits / compressed_size

    print("Combined RLE + Huffman + Wavelet Compression:")
    print("Original Size:", original_size_bits, "bits")
    print("Compressed Size:", compressed_size, "bits")
    print("Compression Factor:", compression_factor)


if __name__ == "__main__":
    main()
