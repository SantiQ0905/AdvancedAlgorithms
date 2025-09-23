# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 3
# Luis Salomón Flores Ugalde

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ HUFFMAN CODES ------

import heapq
from collections import defaultdict, Counter
import pickle
import os

class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCodes:
    def __init__(self):
        self.root = None
        self.codes = {}
        self.reverse_codes = {}
    
    def calculate_probabilities(self, text):
        """Calculate character frequencies and probabilities"""
        char_count = Counter(text)
        total_chars = len(text)
        probabilities = {char: count/total_chars for char, count in char_count.items()}
        return char_count, probabilities
    
    def build_huffman_tree(self, char_freq):
        """Build Huffman tree from character frequencies"""
        if not char_freq:
            return None
        
        heap = [Node(char, freq) for char, freq in char_freq.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = Node(freq=left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)
        
        self.root = heap[0]
        self._generate_codes(self.root, "")
        return self.root
    
    def _generate_codes(self, node, code):
        """Generate Huffman codes for each character"""
        if node:
            if node.char:  # Leaf node
                self.codes[node.char] = code if code else "0"
                self.reverse_codes[code if code else "0"] = node.char
            else:
                self._generate_codes(node.left, code + "0")
                self._generate_codes(node.right, code + "1")
    
    def encode(self, text):
        """Encode text using Huffman codes"""
        return ''.join(self.codes.get(char, '') for char in text)
    
    def decode(self, binary_text):
        """Decode binary text using Huffman tree"""
        decoded = []
        current = self.root
        
        for bit in binary_text:
            if bit == '0':
                current = current.left
            else:
                current = current.right
            
            if current.char:  # Leaf node
                decoded.append(current.char)
                current = self.root
        
        return ''.join(decoded)
    
    def save_tree(self, filename):
        """Save Huffman tree to file"""
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Huffman Codes:\n")
            for char, code in sorted(self.codes.items()):
                if char == '\n':
                    f.write(f"'\\n': {code}\n")
                elif char == ' ':
                    f.write(f"'space': {code}\n")
                else:
                    f.write(f"'{char}': {code}\n")

def main():
    huffman = HuffmanCodes()
    
    # Read the text file
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "TheBells_EAP.txt")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print("Error: TheBells_EAP.txt not found")
        return
    
    # Calculate probabilities
    char_freq, probabilities = huffman.calculate_probabilities(text)
    
    # Get the directory where this script is located for saving files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Save probabilities to file
    prob_file_path = os.path.join(script_dir, "probabilities.txt")
    with open(prob_file_path, 'w', encoding='utf-8') as f:
        f.write("Character Probabilities:\n")
        for char, prob in sorted(probabilities.items()):
            if char == '\n':
                f.write(f"'\\n': {prob:.6f}\n")
            elif char == ' ':
                f.write(f"'space': {prob:.6f}\n")
            else:
                f.write(f"'{char}': {prob:.6f}\n")
    
    # Build Huffman tree
    huffman.build_huffman_tree(char_freq)
    
    # Save tree to file
    huffman.save_tree("huffman_tree.txt")
    
    # Encode the text
    encoded_text = huffman.encode(text)
    
    # Save encoded text
    encoded_file_path = os.path.join(script_dir, "encoded_text.txt")
    with open(encoded_file_path, 'w') as f:
        f.write(encoded_text)
    
    print("Files created:")
    print("- probabilities.txt (character probabilities)")
    print("- huffman_tree.txt (Huffman codes)")
    print("- encoded_text.txt (encoded binary text)")
    
    # Menu for encoding/decoding user input
    while True:
        print("\n--- Huffman Encoder/Decoder Menu ---")
        print("1. Encode text")
        print("2. Decode binary")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            user_text = input("Enter text to encode: ")
            try:
                encoded = huffman.encode(user_text)
                print(f"Encoded: {encoded}")
            except KeyError as e:
                print(f"Error: Character {e} not in Huffman tree")
        
        elif choice == '2':
            binary_input = input("Enter binary to decode: ")
            try:
                decoded = huffman.decode(binary_input)
                print(f"Decoded: {decoded}")
            except:
                print("Error: Invalid binary sequence")
        
        elif choice == '3':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()