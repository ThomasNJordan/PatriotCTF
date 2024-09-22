import binascii
from collections import defaultdict
import sys

def hex_to_bin(hex_str):
    """Convert hexadecimal string to binary string."""
    scale = 16  # Hexadecimal
    num_of_bits = len(hex_str) * 4
    return bin(int(hex_str, scale))[2:].zfill(num_of_bits)

def load_hex_outputs(file_path):
    """Load hexadecimal outputs from a file."""
    try:
        with open(file_path, 'r') as file:
            hex_outputs = [line.strip() for line in file if line.strip()]
        return hex_outputs
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

def collect_bit_frequencies(hex_outputs):
    """Collect the frequency of '1's in each bit position across all outputs."""
    bit_freq = defaultdict(int)
    total = len(hex_outputs)
    
    for hex_str in hex_outputs:
        bin_str = hex_to_bin(hex_str)
        for i, bit in enumerate(bin_str):
            if bit == '1':
                bit_freq[i] += 1
    
    # Calculate frequency of '1's for each bit position
    for bit in bit_freq:
        bit_freq[bit] /= total
    
    return bit_freq

def reconstruct_flag(bit_freq, total_bits, threshold=0.51):
    """
    Attempt to reconstruct the flag based on bit frequencies.
    Bits with frequency > threshold are set to '1',
    bits with frequency < (1 - threshold) are set to '0',
    and uncertain bits are marked with '?'.
    """
    flag_bits = ['0'] * total_bits
    
    for bit_pos in range(total_bits):
        freq = bit_freq.get(bit_pos, 0)
        if freq > threshold:
            flag_bits[bit_pos] = '1'
        elif freq < (1 - threshold):
            flag_bits[bit_pos] = '0'
        else:
            flag_bits[bit_pos] = '?'
    
    # Group bits into bytes
    bytes_list = []
    for i in range(0, total_bits, 8):
        byte = ''.join(flag_bits[i:i+8])
        if '?' in byte:
            # Unable to determine this byte confidently
            bytes_list.append('?')
        else:
            bytes_list.append(chr(int(byte, 2)))
    
    return ''.join(bytes_list)

def main():
    if len(sys.argv) != 2:
        print("Usage: python decode_flag.py <output_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    hex_outputs = load_hex_outputs(file_path)
    
    if not hex_outputs:
        print("No hexadecimal outputs found in the file.")
        sys.exit(1)
    
    # Determine the number of bits from the first output
    first_bin = hex_to_bin(hex_outputs[0])
    total_bits = len(first_bin)
    
    # Collect bit frequencies
    bit_frequencies = collect_bit_frequencies(hex_outputs)
    
    # Reconstruct the flag
    reconstructed_flag = reconstruct_flag(bit_frequencies, total_bits)
    
    print(f"Reconstructed Flag (Uncertain bits marked as '?'):\n{reconstructed_flag}")

if __name__ == "__main__":
    main()
