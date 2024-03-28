# Swaps bits located at i and j
# swaps bits (most significant bit has index 0, least significant has index n)
def swap_bits(num: int, i: int, j: int, n: int):
    # Extract the bits at positions i and j
    bit_i = (num >> (n - 1 - i)) & 1
    bit_j = (num >> (n - 1 - j)) & 1
    # XOR the bits to swap them
    xor_result = bit_i ^ bit_j
    # Use XOR to flip the bits at positions i and j
    num ^= (xor_result << (n - 1 - i)) | (xor_result << (n - 1 - j))
    return num

def insert_bit(binary_num, bit, n):
    # Shift the number to the right by n bits
    mask = 1 << n
    # Create a mask to clear the bit at position n
    cleared_bit = binary_num & ~mask
    # Set the bit at position n to the desired value
    result = cleared_bit | ((bit & 1) << n)
    return result