import heapq
from collections import Counter

class HuffmanNode:
    """Node structure for Huffman Tree"""
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq  # Min-heap comparison

def build_huffman_tree(text):
    """Builds Huffman Tree and returns root node"""
    freq = Counter(text)
    heap = [HuffmanNode(char, f) for char, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        new_node = HuffmanNode(None, left.freq + right.freq)
        new_node.left, new_node.right = left, right
        heapq.heappush(heap, new_node)

    return heap[0]  # Root of Huffman Tree

def generate_huffman_codes(node, prefix="", code_map={}):
    """Generates Huffman codes for each character"""
    if node:
        if node.char is not None:  # Leaf node
            code_map[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", code_map)
        generate_huffman_codes(node.right, prefix + "1", code_map)

    return code_map

def huffman_encode(text):
    """Encodes text using Huffman Coding"""
    root = build_huffman_tree(text)
    huffman_codes = generate_huffman_codes(root)
    encoded_text = "".join(huffman_codes[char] for char in text)
    return encoded_text, huffman_codes

def huffman_decode(encoded_text, huffman_codes):
    """Decodes Huffman encoded text back to original text"""
    # Reverse the Huffman Code Map (binary codes → characters)
    reverse_codes = {code: char for char, code in huffman_codes.items()}
    
    decoded_text = ""
    current_code = ""
    
    # Traverse through the encoded text
    for bit in encoded_text:
        current_code += bit  # Build binary code sequence
        
        # If current_code is in reverse mapping, we found a character
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ""  # Reset for next character

    return decoded_text

# Example usage
text = "abcdefg"
encoded_text, codes = huffman_encode(text)
decoded_text = huffman_decode(encoded_text,codes)

print(f"Original Text: {text}")
print(f"Encoded Text: {encoded_text}")
print(f"Huffman Codes: {codes}")
print(f"Decoded text : {decoded_text}")
