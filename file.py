
'''
This program implements the RSA encryption algorithm.

'''


def convert_decimal_to_binary(decimal_number):
    binary_number = ''
    while decimal_number > 0:
        binary_number = str(decimal_number & 1) + binary_number
        decimal_number >>= 1
        
    return binary_number


def find_greatest_common_divisor(a, b):
    if b == 0:
        return a
    else:
        return find_greatest_common_divisor(b, a % b)


def check_coprimality(a, b):
    return find_greatest_common_divisor(a, b) == 1


def find_modular_multiplicative_inverse_of_public_exponent_with_respect_to_phi_of_modulus(phi_of_modulus, public_exponent):
    k = 0
    equation = lambda k : (1 + (k * phi_of_modulus)) / (public_exponent)
    modular_multiplicative_inverse = equation(k)

    while(modular_multiplicative_inverse % 1 != 0):
        modular_multiplicative_inverse = equation(k)
        k += 1
        
    return modular_multiplicative_inverse
    

def exponentiate(base, index):
    if index == 0:
        return 1
    elif index == 1:
        return base
    else:
        power = base
        
        while(index > 1):
            power *= base
            index -= 1
            
        return power


def encipher(message, public_key):
    public_exponent, modulus = public_key
    
    cipher = exponentiate(message, public_exponent) % modulus
    
    return cipher
    
    
def decipher(cipher, private_key):
    private_exponent, modulus = private_key
    
    message = exponentiate(cipher, private_exponent) % modulus
    
    return message


def encode(plain_text):
    encoded_text = []

    while(len(plain_text) > 0):
        character = plain_text[-1]
        encoded_character = ord(character)
        encoded_text.append(str(encoded_character))
        plain_text = plain_text[:-1]
        
    return encoded_text


def decode(encoded_text):
    decoded_text = []
    
    while(len(encoded_text) > 0):
        character = chr(int(encoded_text[-1]))
        decoded_text.append(character)
        encoded_text.pop(-1)
        
    return decoded_text
    
    
def encrypt(plain_text, public_key):
    cipher_text = []    

    initial_length = len(plain_text)
    current_length = initial_length
    
    while (current_length > 0):
        message = int(plain_text[-1])
        cipher = encipher(message, public_key)
        cipher_text.append(str(cipher))
        print_progress(initial_length - current_length, initial_length)
        plain_text.pop(-1)
        current_length = len(plain_text)
        
    print_progress(initial_length, initial_length)

    return cipher_text
        

def decrypt(cipher_text, private_key):
    plain_text = []
    
    while (len(cipher_text) > 0):
        cipher = int(cipher_text[-1])
        plain_text.append(str(decipher(cipher, private_key)))
        cipher_text.pop(-1)
        
    return plain_text


def print_progress(current, total):
    fraction = (current / total)
    percentage = int(fraction * 100)
    
    status_message = "Encrypting message... " + str(percentage) + "% complete."

    if current == total:
        print('\r' + status_message, end='\n\n')
    else:
        print(status_message, end='\r')
        

def main():
    while(True):
        # unlike prime numbers p, q
        p = 7
        q = 19
    
        # n
        modulus = p * q
        
        # φ(modulus) (φ(n))
        phi_of_modulus = (p - 1) * (q - 1)
    
        # public/decryption exponent (e)
        # e = 2¹⁶ + 1 = 65537
        public_exponent = 65537
        
        # e must be coprime to φ(modulus)
        if check_coprimality(public_exponent, phi_of_modulus) == False:
            raise ValueError("e is not coprime to φ(modulus).")
            
        # private/encryption exponent (d)
        private_exponent = find_modular_multiplicative_inverse_of_public_exponent_with_respect_to_phi_of_modulus(phi_of_modulus, public_exponent)
        
        public_key = [public_exponent, modulus]
        private_key = [private_exponent, modulus]
    
        # message must be greater than or equal to zero and less than modulus
        message = int(input("Enter integer message → "))
        if message < 0 or message >= modulus:
            raise ValueError("Message must be an integer not greater than or equal to zero and less than modulus.")
            
        print()
        
        cipher = encipher(message, public_key)
        message = decipher(cipher, private_key)
        
        print("Enciphered message → " + str(cipher))
        print("Deciphered message → " + str(message))
        
        print()
        
        # message = "«In the beginning, God created the heavens and the earth.»"
        message = input("Enter text message → ")
    
        print()
        
        encoded_text = encode(message)
        print("Encoded message → " + ''.join(encoded_text))
        
        print()
        
        encrypted_text = encrypt(encoded_text, public_key)
        print("Encrypted message → " + ''.join(encrypted_text))
        
        decrypted_text = decrypt(encrypted_text, private_key)
        print("Decrypted message → " + ''.join(decrypted_text))
        
        print()
        
        decoded_text = decode(decrypted_text)
        print("Decoded message → " + ''.join(decoded_text))
    
        print("\n◇◇◇\n")


main()
