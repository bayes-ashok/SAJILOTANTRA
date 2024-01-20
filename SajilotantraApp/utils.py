import heapq
from collections import defaultdict

from bitarray import bitarray


# Text Compression using Huffman's TREE
def build_huffman_tree(data):
    frequency = defaultdict(int)
    for char in data:
        frequency[char] += 1

    heap = [[weight, [char, ""]] for char, weight in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def huffman_encode(data):
    tree = build_huffman_tree(data)
    encoding_dict = {char: code for char, code in tree}
    encoded_data = ''.join(encoding_dict[char] for char in data)

    print(f"Original data: {data}")
    print(f"Encoded data: {encoded_data}")

    return encoded_data, encoding_dict


# Decompress
def huffman_decode(encoded_data, encoding_dict):
    decoded_data = ''
    current_code = ''
    for bit in encoded_data:
        current_code += bit
        for char, code in encoding_dict.items():
            if current_code == code:
                decoded_data += char
                current_code = ''
                break
    return decoded_data