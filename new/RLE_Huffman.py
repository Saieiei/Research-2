from PIL import Image
import heapq
#


def run_length_encode(image_data):
    encoded_data = []
    current_run = [image_data[0], 1]

    for pixel in image_data[1:]:
        if pixel == current_run[0]:
            current_run[1] += 1
        else:
            encoded_data.append(tuple(current_run))
            current_run = [pixel, 1]

    encoded_data.append(tuple(current_run))
    return encoded_data

def build_huffman_tree(freq_table):
    heap = [[weight, [symbol, ""]] for symbol, weight in freq_table.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    return heap[0][1:]

def huffman_compress(encoded_data):
    frequency_table = dict.fromkeys(encoded_data, 0)
    for symbol in encoded_data:
        frequency_table[symbol] += 1

    huffman_tree = build_huffman_tree(frequency_table)
    
    code_table = {symbol: code for symbol, code in huffman_tree}

    compressed_data = ''.join(code_table[symbol] for symbol in encoded_data)

    return compressed_data, code_table

def calculate_compression_factor(original_size, compressed_size):
    return original_size / compressed_size

def load_image(image_path):
    image = Image.open(image_path)
    pixel_values = list(image.getdata())
    return pixel_values

def main():
    # Image path
    image_path = "/workspaces/Research-2/image/sample3.jpg"

    # Load image
    image_data = load_image(image_path)

    # Step 1: Run-Length Encoding
    encoded_data = run_length_encode(image_data)

    # Step 2: Huffman Coding
    compressed_data, code_table = huffman_compress(encoded_data)

    # Calculate and display compression information
    original_size_bits = len(image_data) * 8 * 3  # Assuming 8 bits per channel (RGB image)
    compressed_size_bits = len(compressed_data)
    compression_factor = calculate_compression_factor(original_size_bits, compressed_size_bits)

    print("Combined RLE + Huffman Compression:")
    print(f"Original Size: {original_size_bits} bits")
    print(f"Compressed Size: {compressed_size_bits} bits")
    print(f"Compression Factor: {compression_factor}")

if __name__ == "__main__":
    main()
