# import random

# # Define the mapping from characters to DNA bases
# # character_to_dna = {
# #     'A': '00',
# #     'C': '01',
# #     'G': '10',
# #     'T': '11'
# # }
# character_to_dna = {
#     '00': 'A',
#     '01': 'T',
#     '10': 'C',
#     '11': 'G'
# }


# # Define the mapping from DNA bases to characters
# dna_to_character = {v: k for k, v in character_to_dna.items()}

# # Function to encode the file into a DNA sequence
# def encode_file(file_path, secret_key):
#     # Read the file as binary data
#     with open(file_path, 'rb') as file:
#         file_data = file.read()

#     # Convert file data into binary sequence
#     binary_sequence = ''.join(format(byte, '08b') for byte in file_data)

#     # Insert random binary digits for obfuscation
#     obfuscated_sequence = ''
#     for bit in binary_sequence:
#         obfuscated_sequence += bit + str(random.randint(0, 1))

#     # Encrypt the sequence using XOR with the secret key
#     encrypted_sequence = ''
#     key_index = 0
#     for bit in obfuscated_sequence:
#         encrypted_bit = str(int(bit) ^ int(secret_key[key_index]))
#         encrypted_sequence += encrypted_bit
#         key_index = (key_index + 1) % len(secret_key)

#     # Convert the binary sequence into a DNA sequence
#     dna_sequence = ''
#     for i in range(0, len(encrypted_sequence), 2):
#         dna_base = dna_to_character.get(encrypted_sequence[i:i+2], '')
#         dna_sequence += dna_base

#     # Save the encoded DNA sequence to a file
#     encoded_file_path = file_path + '_encoded'
#     with open(encoded_file_path, 'w') as file:
#         file.write(dna_sequence)

#     return encoded_file_path

# # Function to decode the DNA sequence back into the original file
# def decode_dna_sequence(file_path, secret_key):
#     # Read the encoded DNA sequence file
#     with open(file_path, 'r') as file:
#         dna_sequence = file.read()

#     # Convert DNA sequence into binary sequence
#     binary_sequence = ''
#     for base in dna_sequence:
#         binary_sequence += character_to_dna.get(base, '')

#     # Decrypt the sequence using XOR with the secret key
#     decrypted_sequence = ''
#     key_index = 0
#     for bit in binary_sequence:
#         decrypted_bit = str(int(bit) ^ int(secret_key[key_index]))
#         decrypted_sequence += decrypted_bit
#         key_index = (key_index + 1) % len(secret_key)

#     # Remove the obfuscated bits
#     original_sequence = ''
#     for i in range(0, len(decrypted_sequence), 2):
#         original_sequence += decrypted_sequence[i]

#     # Convert the binary sequence into the original file data
#     file_data = bytearray()
#     for i in range(0, len(original_sequence), 8):
#         byte = int(original_sequence[i:i+8], 2)
#         file_data.append(byte)

#     # Remove the "_encoded" part from the encoded file path
#     original_file_path = file_path[:-8]

#     # Save the decoded file
#     decoded_file_path = original_file_path + '_decoded'
#     with open(decoded_file_path, 'wb') as file:
#         file.write(file_data)

#     return decoded_file_path

# # Prompt user for file path (or file name if it's in the same directory)
# file_path = input("Enter the file path or file name: ")

# # Prompt user for secret key
# secret_key = input("Enter the secret key: ")

# # Prompt user for encode or decode operation
# operation = input("Enter 'encode' to encode the file or 'decode' to decode the file: ")

# if operation.lower() == 'encode':
#     # Encode the file into a DNA sequence
#     encoded_file_path = encode_file(file_path, secret_key)
#     print(f"File encoded and saved as: {encoded_file_path}")
# elif operation.lower() == 'decode':
#     # Decode the DNA sequence back into the original file
#     decoded_file_path = decode_dna_sequence(file_path, secret_key)
#     print(f"DNA sequence decoded and saved as: {decoded_file_path}")
# else:
#     print("Invalid operation. Please enter 'encode' or 'decode'.")




























































import random

DNA_MAPPING = {
    '00': 'A',
    '01': 'T',
    '10': 'C',
    '11': 'G'
}

def dna_encode(data):
    encoded_data = ""
    for i in range(0, len(data), 2):
        bits = data[i:i+2]
        encoded_data += DNA_MAPPING.get(bits, "")
    return encoded_data

def dna_decode(encoded_data):
    decoded_data = ""
    for char in encoded_data:
        for bits, base in DNA_MAPPING.items():
            if base == char:
                decoded_data += bits
                break
    return decoded_data

# Prompt user for file name
file_name = input("Enter the name of the file to be encoded/decoded (including extension): ")

# Prompt user for encode or decode operation
operation = input("Enter 'encode' to encode the file or 'decode' to decode the file: ")

# Prompt user for secret key
secret_key = input("Enter the secret key: ")

# Generate file paths
input_file_path = file_name
if operation.lower() == 'encode':
    output_file_path = file_name.split('.')[0] + '_encoded.' + file_name.split('.')[1]
elif operation.lower() == 'decode':
    output_file_path = file_name.split('.')[0] + '_decoded.' + file_name.split('.')[1]
else:
    print("Invalid operation. Please enter 'encode' or 'decode'.")
    exit()

# Perform encoding or decoding based on user input
if operation.lower() == 'encode':
    # Read the file as binary data
    with open(input_file_path, 'rb') as file:
        file_data = file.read()

    # Convert file data into binary sequence
    binary_sequence = ''.join(format(byte, '08b') for byte in file_data)

    # Insert random binary digits for obfuscation
    obfuscated_sequence = ''
    for bit in binary_sequence:
        obfuscated_sequence += bit + str(random.randint(0, 1))

    # Encrypt the sequence using XOR with the secret key
    encrypted_sequence = ''
    key_index = 0
    for bit in obfuscated_sequence:
        encrypted_bit = str(int(bit) ^ int(secret_key[key_index]))
        encrypted_sequence += encrypted_bit
        key_index = (key_index + 1) % len(secret_key)

    # Convert the binary sequence into a DNA sequence
    dna_sequence = dna_encode(encrypted_sequence)

    # Save the encoded DNA sequence to a file
    with open(output_file_path, 'w') as file:
        file.write(dna_sequence)

    print(f"File encoded and saved as: {output_file_path}")

elif operation.lower() == 'decode':
    # Read the encoded DNA sequence file
    with open(input_file_path, 'r') as file:
        dna_sequence = file.read()

    # Convert DNA sequence into binary sequence
    binary_sequence = ""
    for base in dna_sequence:
        binary_sequence += DNA_MAPPING.get(base, "")

    # Decrypt the sequence using XOR with the secret key
    decrypted_sequence = ""
    key_index = 0
    for bit in binary_sequence:
        decrypted_bit = str(int(bit) ^ int(secret_key[key_index]))
        decrypted_sequence += decrypted_bit
        key_index = (key_index + 1) % len(secret_key)

    # Remove the obfuscated bits
    original_sequence = ""
    for i in range(0, len(decrypted_sequence), 2):
        original_sequence += decrypted_sequence[i]

    # Convert the binary sequence into the original file data
    file_data = bytearray()
    for i in range(0, len(original_sequence), 8):
        byte = int(original_sequence[i:i+8], 2)
        file_data.append(byte)

    # Save the decoded file
    with open(output_file_path, 'wb') as file:
        file.write(file_data)

    print(f"DNA sequence decoded and saved as: {output_file_path}")


















































































































DNA_MAPPING = {
    '00': 'A',
    '01': 'T',
    '10': 'C',
    '11': 'G'
}

def dna_encode(data):
    encoded_data = ""
    for i in range(0, len(data), 2):
        bits = data[i:i+2]
        encoded_data += DNA_MAPPING.get(bits, "")
    return encoded_data


def dna_decode(encoded_data):
    decoded_data = ""
    for char in encoded_data:
        for bits, base in DNA_MAPPING.items():
            if base == char:
                decoded_data += bits
                break
    return decoded_data

# Example usage
plaintext = '01001101011000010110111001100111'  # Binary representation of the message
encoded_sequence = dna_encode(plaintext)
decoded_sequence = dna_decode(encoded_sequence)

print("Plaintext:", plaintext)
print("Encoded Sequence:", encoded_sequence)
print("Decoded Sequence:", decoded_sequence)









