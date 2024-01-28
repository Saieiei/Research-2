import heapq
import os
#

def read_image_from_file(file_path):
    with open(file_path, 'rb') as file:
        image_data = file.read()
    return image_data

def write_compressed_data_to_file(output_file_path, compressed_data, code_table):
    with open(output_file_path, 'w') as file:
        file.write("Compressed Data:\n")
        file.write(f"{compressed_data}\n\n")

        file.write("Code Table:\n")
        for symbol, code in code_table.items():
            file.write(f"{symbol}: {code}\n")

def build_huffman_tree(frequency_table):
    heap = [[weight, [symbol, ""]] for symbol, weight in frequency_table.items()]
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

def huffman_compress(image_data):
    frequency_table = dict.fromkeys(image_data, 0)
    for symbol in image_data:
        frequency_table[symbol] += 1

    huffman_tree = build_huffman_tree(frequency_table)
    
    code_table = {symbol: code for symbol, code in huffman_tree}

    compressed_data = ''.join(code_table[symbol] for symbol in image_data)

    return compressed_data, code_table

if __name__ == "__main__":
    image_file_path = "/workspaces/Research-2/image/sample3.jpg"
    output_file_path = "/workspaces/Research-2/image/compressed_output.txt"

    image_data = read_image_from_file(image_file_path)
    compressed_data, code_table = huffman_compress(image_data)

    write_compressed_data_to_file(output_file_path, compressed_data, code_table)

    original_size_bits = len(image_data) * 8
    compressed_size_bits = len(compressed_data)
    compression_factor = original_size_bits / compressed_size_bits

    print(f"Huffman Compression:")
    print(f"Original Size: {original_size_bits} bits")
    print(f"Compressed Size: {compressed_size_bits} bits")
    print(f"Compression Factor: {compression_factor}")
