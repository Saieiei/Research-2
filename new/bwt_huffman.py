
#21 
import heapq
import os

class HuffmanNode:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

class BWT:
    @staticmethod
    def transform(text):
        rotations = [text[i:] + text[:i] for i in range(len(text))]
        rotations.sort()
        transformed_text = ''.join(rotation[-1] for rotation in rotations)
        return transformed_text

def build_frequency_table(data):
    freq_table = {}
    for symbol in data:
        freq_table[symbol] = freq_table.get(symbol, 0) + 1
    return freq_table

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

def compress_image(data, code_table):
    compressed_data = ""
    for symbol in data:
        compressed_data += code_table[symbol]
    return compressed_data

def calculate_compression_size(compressed_data):
    return len(compressed_data)

def calculate_compression_factor(original_size, compressed_size):
    return original_size / compressed_size

def dynamic_bwt_huffman_compression(image_path, chunk_size=1024, bwt_chunk_size=50):
    # Load the image
    image = Image.open(image_path)
    image_data = list(image.tobytes())
    
    # Perform BWT in chunks
    compressed_bwt_data = ""
    with open(image_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            image_data_str = chunk.decode("latin-1")
            bwt_transform = BWT.transform(image_data_str)
            compressed_bwt_data += bwt_transform[:bwt_chunk_size]
    
    # Build Huffman tree and code table
    freq_table = build_frequency_table(compressed_bwt_data)
    huffman_tree = build_huffman_tree(freq_table)
    code_table = build_code_table(huffman_tree)
    
    # Compress the BWT data using Huffman coding
    compressed_huffman_data = compress_image(compressed_bwt_data, code_table)
    
    return compressed_huffman_data

def main():
    # Specify the image file path
    image_path = "image/sample3.jpg"
    
    # Set the chunk size for processing the image
    chunk_size = 1024
    
    # Set the BWT chunk size
    bwt_chunk_size = 50
    
    # Perform dynamic BWT and Huffman compression
    compressed_data = dynamic_bwt_huffman_compression(image_path, chunk_size, bwt_chunk_size)
    
    # Calculate and display compression information
    original_image_size_bits = os.path.getsize(image_path) * 8       # 8 bits per byte
    compressed_size = calculate_compression_size(compressed_data)
    compression_factor = calculate_compression_factor(original_image_size_bits, compressed_size)

    print("Huffman + BWT compression:")
    print("Original Size:", original_image_size_bits, "bits")
    print("Compressed Size:", compressed_size, "bits")
    print("Compression Factor:", compression_factor)

if __name__ == "__main__":
    main()
