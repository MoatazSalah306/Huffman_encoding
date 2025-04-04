import heapq
import ast
from collections import Counter

class HuffmanNode:
    """Node structure for Huffman Tree"""
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq  # For min-heap comparison

def build_huffman_tree(text):
    freq = Counter(text)
    heap = [HuffmanNode(char, f) for char, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        new_node = HuffmanNode(None, left.freq + right.freq)
        new_node.left = left
        new_node.right = right
        heapq.heappush(heap, new_node)

    return heap[0]

def generate_huffman_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}

    if node:
        if node.char is not None:
            code_map[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", code_map)
        generate_huffman_codes(node.right, prefix + "1", code_map)
    return code_map

def huffman_encode(text):
    root = build_huffman_tree(text)
    huffman_codes = generate_huffman_codes(root)
    encoded_text = "".join(huffman_codes[char] for char in text)
    return encoded_text, huffman_codes

def huffman_decode(encoded_text, huffman_codes):
    reverse_codes = {code: char for char, code in huffman_codes.items()}
    decoded_text = ""
    current_code = ""

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ""
    return decoded_text

def main_menu():
    encoded_text = None
    codes = None

    while True:
        print("\n--- Huffman Coding Menu ---")
        print("1. Encode text")
        print("2. Decode text")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            text = input("Enter text to encode: ")
            encoded_text, codes = huffman_encode(text)
            print(f"\nEncoded Text: {encoded_text}")
            print(f"Huffman Codes: {codes}")

        elif choice == "2":
            print("\n--- Decode Options ---")
            use_existing = input("Use previously encoded data? (y/n): ").lower().strip()

            if use_existing == "y":
                if encoded_text and codes:
                    decoded_text = huffman_decode(encoded_text, codes)
                    print(f"\nDecoded Text: {decoded_text}")
                else:
                    print("No previously encoded data found. Please encode text first or decode manually.")
            else:
                binary_input = input("Enter binary encoded string: ").strip()
                codes_input = input("Enter Huffman code map (as Python dict, e.g., {'a': '0', 'b': '10'}): ").strip()

                try:
                    codes_dict = ast.literal_eval(codes_input)
                    if not isinstance(codes_dict, dict):
                        raise ValueError("Code map must be a dictionary.")
                    decoded_text = huffman_decode(binary_input, codes_dict)
                    print(f"\nDecoded Text: {decoded_text}")
                except Exception as e:
                    print(f"Invalid input. Error: {e}")

        elif choice == "3":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
