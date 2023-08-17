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

# Prompt user for file path
file_path = input("Enter the file path: ")

# Prompt user for secret key
secret_key = input("Enter the secret key: ")

# Prompt user for encode or decode operation
operation = input("Enter 'encode' to encode the file or 'decode' to decode the file: ")

if operation.lower() == 'encode':
    # Read the file as binary data
    with open(file_path, 'rb') as file:
        file_data = file.read()

    # Convert file data into binary sequence
    binary_sequence = ''.join(format(byte, '08b') for byte in file_data)

    # Encode the binary sequence into a DNA sequence
    encoded_sequence = dna_encode(binary_sequence)

    # Save the encoded sequence to a file
    encoded_file_path = file_path + '_encoded.txt'
    with open(encoded_file_path, 'w') as file:
        file.write(encoded_sequence)

    print(f"File encoded and saved as: {encoded_file_path}")

elif operation.lower() == 'decode':
    # Read the encoded sequence file
    with open(file_path, 'r') as file:
        encoded_sequence = file.read()

    # Decode the DNA sequence into a binary sequence
    binary_sequence = dna_decode(encoded_sequence)

    # Convert the binary sequence into file data
    file_data = bytearray(int(binary_sequence[i:i+8], 2) for i in range(0, len(binary_sequence), 8))

    # Save the decoded file
    decoded_file_path = file_path + '_decoded.bin'
    with open(decoded_file_path, 'wb') as file:
        file.write(file_data)

    print(f"File decoded and saved as: {decoded_file_path}")

else:
    print("Invalid operation. Please enter 'encode' or 'decode'.")
