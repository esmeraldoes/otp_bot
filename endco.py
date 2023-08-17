import random

# Define the mapping from characters to DNA bases
character_to_dna = {
    'A': '00',
    'C': '01',
    'G': '10',
    'T': '11'
}

# Define the mapping from DNA bases to characters
dna_to_character = {v: k for k, v in character_to_dna.items()}

# Function to encode the file into a DNA sequence
def encode_file(file_path, secret_key):
    # Read the file as binary data
    with open(file_path, 'rb') as file:
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
    dna_sequence = ''
    for i in range(0, len(encrypted_sequence), 2):
        dna_base = dna_to_character.get(encrypted_sequence[i:i+2], '')
        dna_sequence += dna_base

    # Save the encoded DNA sequence to a file
    encoded_file_path = file_path + '_encoded'
    with open(encoded_file_path, 'w') as file:
        file.write(dna_sequence)

    return encoded_file_path

# Function to decode the DNA sequence back into the original file
def decode_dna_sequence(file_path, secret_key):
    # Read the encoded DNA sequence file
    with open(file_path, 'r') as file:
        dna_sequence = file.read()

    # Convert DNA sequence into binary sequence
    binary_sequence = ''
    for base in dna_sequence:
        binary_sequence += character_to_dna.get(base, '')

    # Decrypt the sequence using XOR with the secret key
    decrypted_sequence = ''
    key_index = 0
    for bit in binary_sequence:
        decrypted_bit = str(int(bit) ^ int(secret_key[key_index]))
        decrypted_sequence += decrypted_bit
        key_index = (key_index + 1) % len(secret_key)

    # Remove the obfuscated bits
    original_sequence = ''
    for i in range(0, len(decrypted_sequence), 2):
        original_sequence += decrypted_sequence[i]

    # Convert the binary sequence into the original file data
    file_data = bytearray()
    for i in range(0, len(original_sequence), 8):
        byte = int(original_sequence[i:i+8], 2)
        file_data.append(byte)

    # Remove the "_encoded" part from the encoded file path
    original_file_path = file_path[:-8]

    # Save the decoded file
    decoded_file_path = original_file_path + '_decoded'
    with open(decoded_file_path, 'wb') as file:
        file.write(file_data)

    return decoded_file_path

# Prompt user for file path (or file name if it's in the same directory)
file_path = input("Enter the file path or file name: ")

# Prompt user for secret key
secret_key = input("Enter the secret key: ")

# Prompt user for encode or decode operation
operation = input("Enter 'encode' to encode the file or 'decode' to decode the file: ")

if operation.lower() == 'encode':
    # Encode the file into a DNA sequence
    encoded_file_path = encode_file(file_path, secret_key)
    print(f"File encoded and saved as: {encoded_file_path}")
elif operation.lower() == 'decode':
    # Decode the DNA sequence back into the original file
    decoded_file_path = decode_dna_sequence(file_path, secret_key)
    print(f"DNA sequence decoded and saved as: {decoded_file_path}")
else:
    print("Invalid operation. Please enter 'encode' or 'decode'.")













# # DNA Mapping
# DNA_MAPPING = {
#     '00': 'A',
#     '01': 'T',
#     '10': 'C',
#     '11': 'G'
# }

# def dna_encode(data, key):
#     encoded_data = ""
#     for i in range(len(data)):
#         bit = data[i]
#         key_bit = key[i % len(key)]
#         encoded_data += DNA_MAPPING.get(bit + key_bit, "")
#     return encoded_data

# def dna_decode(encoded_data, key):
#     decoded_data = ""
#     for i in range(len(encoded_data)):
#         base = encoded_data[i]
#         key_bit = key[i % len(key)]
#         for bits, dna_base in DNA_MAPPING.items():
#             if dna_base == base:
#                 decoded_data += bits[:-1] if key_bit == bits[-1] else bits
#                 break
#     return decoded_data

# # Example usage
# plaintext = '01001101011000010110111001100111'  # Binary representation of the message
# key = '1234'

# encoded_sequence = dna_encode(plaintext, key)
# decoded_sequence = dna_decode(encoded_sequence, key)

# print("Plaintext:", plaintext)
# print("Encoded Sequence:", encoded_sequence)
# print("Decoded Sequence:", decoded_sequence)









# # DNA Mapping
# DNA_MAPPING = {
#     '00': 'A',
#     '01': 'T',
#     '10': 'C',
#     '11': 'G'
# }

# def dna_encode(data):
#     encoded_data = ""
#     for i in range(0, len(data), 2):
#         bits = data[i:i+2]
#         encoded_data += DNA_MAPPING.get(bits, "")
#     return encoded_data

# def dna_decode(encoded_data):
#     decoded_data = ""
#     for char in encoded_data:
#         for bits, base in DNA_MAPPING.items():
#             if base == char:
#                 decoded_data += bits
#                 break
#     return decoded_data

# # Example usage
# plaintext = '01001101011000010110111001100111'  # Binary representation of the message
# encoded_sequence = dna_encode(plaintext)
# decoded_sequence = dna_decode(encoded_sequence)

# print("Plaintext:", plaintext)
# print("Encoded Sequence:", encoded_sequence)
# print("Decoded Sequence:", decoded_sequence)

















# # Mapping of DNA bases to binary values
# DNA_MAPPING = {
#     'A': '00',
#     'T': '01',
#     'C': '10',
#     'G': '11'
# }

# # Mapping of binary values to DNA bases
# REVERSE_DNA_MAPPING = {v: k for k, v in DNA_MAPPING.items()}

# # Encryption key
# KEY = "abc"


# def dna_encode(data):
#     encoded_data = ""
#     for byte in data:
#         encoded_data += DNA_MAPPING.get(chr(byte), "")
#     return encoded_data.encode()


# def dna_decode(encoded_data):
#     decoded_data = bytearray()
#     for i in range(0, len(encoded_data), 2):
#         dna = encoded_data[i:i+2]
#         decoded_data.append(ord(REVERSE_DNA_MAPPING.get(dna, "")))
#     return bytes(decoded_data)


# def xor_encrypt(data, key):
#     encrypted_data = bytearray()
#     for i in range(len(data)):
#         byte = data[i]
#         key_byte = key[i % len(key)]
#         encrypted_byte = byte ^ ord(key_byte)
#         encrypted_data.append(encrypted_byte)
#     return bytes(encrypted_data)


# def xor_decrypt(data, key):
#     decrypted_data = bytearray()
#     for i in range(len(data)):
#         byte = data[i]
#         key_byte = key[i % len(key)]
#         decrypted_byte = byte ^ ord(key_byte)
#         decrypted_data.append(decrypted_byte)
#     return bytes(decrypted_data)


# def encrypt_file(input_file, output_file):
#     with open(input_file, 'rb') as f_in:
#         data = f_in.read()
#         encoded_data = dna_encode(data)
#         encrypted_data = xor_encrypt(encoded_data, KEY)
#         with open(output_file, 'wb') as f_out:
#             f_out.write(encrypted_data)


# def decrypt_file(input_file, output_file):
#     with open(input_file, 'rb') as f_in:
#         encrypted_data = f_in.read()
#         decrypted_data = xor_decrypt(encrypted_data, KEY)
#         decoded_data = dna_decode(decrypted_data)
#         with open(output_file, 'wb') as f_out:
#             f_out.write(decoded_data)


# # Example usage for file encryption and decryption
# input_file = "bla.txt"
# encrypted_file = "encrypted.bin"
# decrypted_file = "decrypted.txt"

# encrypt_file(input_file, encrypted_file)
# decrypt_file(encrypted_file, decrypted_file)




































# import base64

# # Encryption key
# KEY = "encryption_key"


# def encrypt_file(input_file, output_file):
#     with open(input_file, 'rb') as f_in:
#         data = f_in.read()
#         encrypted_data = xor_encrypt(data, KEY)
#         encoded_data = base64.b64encode(encrypted_data)
#         with open(output_file, 'wb') as f_out:
#             f_out.write(encoded_data)


# def decrypt_file(input_file, output_file):
#     with open(input_file, 'rb') as f_in:
#         encoded_data = f_in.read()
#         encrypted_data = base64.b64decode(encoded_data)
#         decrypted_data = xor_decrypt(encrypted_data, KEY)
#         with open(output_file, 'wb') as f_out:
#             f_out.write(decrypted_data)


# def xor_encrypt(data, key):
#     encrypted_data = bytearray()
#     for i in range(len(data)):
#         byte = data[i]
#         key_byte = key[i % len(key)]
#         encrypted_byte = byte ^ ord(key_byte)
#         encrypted_data.append(encrypted_byte)
#     return bytes(encrypted_data)


# def xor_decrypt(data, key):
#     decrypted_data = bytearray()
#     for i in range(len(data)):
#         byte = data[i]
#         key_byte = key[i % len(key)]
#         decrypted_byte = byte ^ ord(key_byte)
#         decrypted_data.append(decrypted_byte)
#     return bytes(decrypted_data)


# # Example usage for file encryption and decryption
# input_file = "bla.txt"
# encrypted_file = "encrypted.bin"
# decrypted_file = "decrypted.txt"

# encrypt_file(input_file, encrypted_file)
# decrypt_file(encrypted_file, decrypted_file)



































# # Mapping of DNA bases to binary values
# DNA_MAPPING = {
#     'A': '00',
#     'T': '01',
#     'C': '10',
#     'G': '11'
# }

# # Mapping of binary values to DNA bases
# REVERSE_DNA_MAPPING = {v: k for k, v in DNA_MAPPING.items()}


# def encode_file(input_file, output_file, key):
#     with open(input_file, 'rb') as f_in:
#         with open(output_file, 'wb') as f_out:
#             byte = f_in.read(1)
#             encoded_bytes = bytearray()
#             while byte:
#                 byte = ord(byte)
#                 for _ in range(4):
#                     encoded_bytes.append(int(DNA_MAPPING.get(chr(byte & 0x03), ''), 2))
#                     byte >>= 2
#                 byte = f_in.read(1)
#             encoded_bytes = apply_key(encoded_bytes, key)
#             f_out.write(encoded_bytes)


# def decode_file(input_file, output_file, key):
#     with open(input_file, 'rb') as f_in:
#         with open(output_file, 'wb') as f_out:
#             encoded_bytes = f_in.read()
#             encoded_bytes = apply_key(encoded_bytes, key)
#             byte = 0
#             decoded_bytes = bytearray()
#             for i, value in enumerate(encoded_bytes):
#                 byte |= (value & 0x03) << (2 * (3 - (i % 4)))
#                 if (i + 1) % 4 == 0:
#                     decoded_bytes.append(byte)
#                     byte = 0
#             f_out.write(decoded_bytes)


# def apply_key(data, key):
#     key_length = len(key)
#     for i, value in enumerate(data):
#         data[i] ^= key[i % key_length]
#     return data


# # Example usage:
# input_file = 'bla.txt'
# encoded_file = 'encoded.txt'
# decoded_file = 'decoded.txt'

# key = input("Enter the key: ")

# encode_file(input_file, encoded_file, key)
# decode_file(encoded_file, decoded_file, key)











































# import random

# # Define the mapping from characters to DNA bases
# character_to_dna = {
#     'A': '00',
#     'C': '01',
#     'G': '10',
#     'T': '11'
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