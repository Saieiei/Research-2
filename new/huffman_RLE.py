import heapq
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

class HuffmanNode:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(freq_table):
    heap = [HuffmanNode(symbol, frequency) for symbol, frequency in freq_table.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left_node = heapq.heappop(heap)
        right_node = heapq.heappop(heap)
        
        combined_frequency = left_node.frequency + right_node.frequency
        combined_node = HuffmanNode(None, combined_frequency)
        combined_node.left = left_node
        combined_node.right = right_node
        
        heapq.heappush(heap, combined_node)
    
    return heap[0]

def build_code_table(huffman_tree):
    code_table = {}
    
    def traverse_tree(node, code, code_table):
        if node is None:
            return

        if node.symbol is not None:
            code_table[node.symbol] = code

        traverse_tree(node.left, code + "0", code_table)
        traverse_tree(node.right, code + "1", code_table)
    
    traverse_tree(huffman_tree, "", code_table)
    
    return code_table

def compress_image_huffman_rle(image_path, output_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()

    encoded_data = run_length_encode(image_data)

    freq_table = dict(encoded_data)
    huffman_tree = build_huffman_tree(freq_table)
    code_table = build_code_table(huffman_tree)

    compressed_data = ''.join(code_table[symbol] + count.to_bytes(2, byteorder='big').decode('latin-1') for symbol, count in encoded_data)

    with open(output_path, 'w') as f:
        f.write(compressed_data)

def calculate_compression_factor(original_size, compressed_size):
    return original_size / compressed_size

def main():
    # Specify the image file path
    image_path = "image/sample3.jpg"

    # Specify the output path for the compressed image
    output_path = "image/compressed_image_huffman_rle.jpg"

    # Perform Huffman + RLE-based compression
    compress_image_huffman_rle(image_path, output_path)

    # Calculate and display compression information
    original_image_size_bits = os.path.getsize(image_path) * 8       # 8 bits per byte
    compressed_size = os.path.getsize(output_path) * 8
    compression_factor = calculate_compression_factor(original_image_size_bits, compressed_size)

    print("Huffman + RLE-based compression:")
    print("Original Size:", original_image_size_bits, "bits")
    print("Compressed Size:", compressed_size, "bits")
    print("Compression Factor:", compression_factor)

if __name__ == "__main__":
    main()
