import numpy as np
import egcd

padding_count = 0  # Counter for padding added during encryption

# Define the full alphabet
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:',.<>/?`~"

# Create dictionary mapping each character to an index and vice versa
letter_to_index = {}
index_to_letter = {}

# add to the dictionaries
for i, char in enumerate(alphabet):
    letter_to_index[char] = i
    index_to_letter[i] = char

#Function to calculate the modulus inverse of a matrix
def matrix_modulus_inverse(mat):
    determinant = int(np.round(np.linalg.det(mat)))  # Calculate the determinant of the matrix
    inverse_determinant = egcd.egcd(determinant, len(alphabet))[1] % len(alphabet)  # Calculate the inverse determinant
    inverse_mat = np.linalg.inv(mat)  # Calculate the inverse of the matrix
    rounded_result = np.round(determinant * inverse_mat).astype(int)  # Round the product of the determinant and the inverse of the matrix to an integer
    matrix_modulus_inverse = inverse_determinant * rounded_result % len(alphabet)  # calculate the modulus inverse
    return matrix_modulus_inverse

# Function to encrypt a message using Hill cipher
def hill_cipher_encrypt(message, key):
    global padding_count
    message_in_nums = []  # List to store numerical equiv of characters in the message
    encrypted = ""  # String to store the encrypted message

    # Convert message characters to numbers
    for char in message:
        message_in_nums.append(letter_to_index[char])

    # Split message into blocks of size equal to the key matrix dimension
    block_size = int(key.shape[0])
    split = [message_in_nums[i:i + block_size] for i in range(0, len(message_in_nums), block_size)]

    # Encrypt each block
    for p in split:
        p_array = np.asarray(p)
        p_transposed = np.transpose(p_array)  # Transpose the array
        p_with_new_axis = p_transposed[:, np.newaxis]
        p = p_with_new_axis

        # Pad block with random letter or char (in this case z) for unknown characters
        while p.shape[0] != key.shape[0]:
            padding_count += 1
            p = np.append(p, letter_to_index["z"])[:, np.newaxis]

        #Perform matrix multiplication with the key and calculate encrypted nums
        numbers = np.dot(key, p) % len(alphabet)

        # Map numbers back to chars
        for indx in range(numbers.shape[0]):
            number = int(numbers[indx, 0])
            encrypted += index_to_letter[number]

    return encrypted

# Function to decrypt a message encrypted with Hill cipher
def hill_cipher_decrypt(ciphered_text, key_inverse):
    global padding_count
    ciphered_text_in_nums = []  # List to store numerical representation of characters in the ciphered text
    decrypted = ""  # String to store the decrypted message

    # Convert ciphered text characters to numerical representation
    for char in ciphered_text:
        index_val = letter_to_index[char]
        ciphered_text_in_nums.append(index_val)

    # Split ciphered text into blocks of size equal to the inverse key matrix size/shape
    block_size = int(key_inverse.shape[0])
    split_text = [ciphered_text_in_nums[i:i + block_size] for i in range(0, len(ciphered_text_in_nums), block_size)]

    # Decrypt each block
    for t in split_text:
        t_array = np.asarray(t)
        t_transposed = np.transpose(t_array)  # Transpose array
        t_with_new_axis = t_transposed[:, np.newaxis]  # Add a new axis to the transposed array
        t = t_with_new_axis

        # Perform matrix multiplication with the inverse key and calculate decrypted numbers
        numbers = np.dot(key_inverse, t) % len(alphabet)

        # Map numbers back to characters
        for indx in range(numbers.shape[0]):
            number = int(numbers[indx, 0])
            decrypted += index_to_letter[number]

    # Remove padding (if any)
    while padding_count != 0:
        padding_count -= 1
        decrypted = decrypted[:-1]

    return decrypted

#Function to encrypt a message using a backwards Caesar cipher
def backwards_caeser_encrypt(text, shift):
    new_text = ''
    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            new_index = (index - shift) % len(alphabet)
            new_char = alphabet[new_index]
            new_text += new_char
    return new_text

# Function to decrypt a message encrypted with a backwards Caesar cipher
def backwards_caeser_decrypt(text, shift):
    return backwards_caeser_encrypt(text, -shift) #Simply using the inverse shift for the encrypt function 

# Function to encrypt a message that's gone through both ciphers
def encrypt(text):
    key = np.array([[3, 2], [5, 7]])  # instantiate key matrix
    caeser = backwards_caeser_encrypt(text, 7)  # Encrypt the text using backwards Caesar cipher
    return hill_cipher_encrypt(caeser, key)  # Encrypt the Caesar cipher output using Hill cipher

# Function to decrypt a message that's gone through both ciphers (opposite order as encrypt)
def decrypt(encrypted_text):
    keyinv = matrix_modulus_inverse(np.array([[3, 2], [5, 7]]))  # Calculate the inverse key matrix
    hill = hill_cipher_decrypt(encrypted_text, keyinv)  #Decrypt the text using Hill cipher
    return backwards_caeser_decrypt(hill, 7)  # Decrypt the Hill cipher output using backwards Caesar cipher
