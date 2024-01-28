import zlib
import heapq

def run_length_encode(data):
    encoded_data = []
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            i += 1
            count += 1
        encoded_data.append((data[i], count))
        i += 1
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
    compressed_data = ''.join(code_table[symbol] for symbol in data)

    return compressed_data, code_table

def lzw_compress(data):
    compressed_data = zlib.compress(data.encode('utf-8'))
    return compressed_data

def main():
    # Example image file path
    image_path = "image/sample3.jpg"

    # Read and process image data
    with open(image_path, 'rb') as file:
        image_data = file.read()

    # Convert bytes to string for RLE and Huffman encoding
    image_data_str = image_data.decode("latin-1")

    # RLE compression
    rle_encoded_data = run_length_encode(image_data_str)
    
    # Flatten the list of tuples for Huffman encoding
    rle_encoded_data_flat = [char * count for char, count in rle_encoded_data]
    
    # Huffman compression
    huffman_compressed_data, _ = huffman_compress(rle_encoded_data_flat)
    
    # LZW compression
    lzw_compressed_data = lzw_compress(image_data_str)

    # Combine compressed results
    final_compressed_data = rle_encoded_data_flat + huffman_compressed_data + lzw_compressed_data

    # Calculate sizes
    original_size_bits = len(image_data) * 8
    compressed_size_bits = len(''.join(final_compressed_data)) * 8

    # Display compression information
    print("Combined RLE + Huffman + LZW Compression:")
    print(f"Original Size: {original_size_bits} bits")
    print(f"Compressed Size: {compressed_size_bits} bits")
    print(f"Compression Factor: {original_size_bits / compressed_size_bits}")

if __name__ == "__main__":
    main()
