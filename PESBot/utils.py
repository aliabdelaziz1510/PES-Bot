from cryptography.fernet import Fernet

def encrypt():
    key = Fernet.generate_key()
    print(f"Generated key: {key}")

    # Optionally, save the key to a .env file
    with open('.env', 'a') as f:
        f.write(f'\nKEY={key}\n')

    with open('RAScloud.json', 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open('encryptedSecret.json', 'wb') as f:
        f.write(encrypted)
    return key.decode('utf-8')


def decrypt(key):
    with open('encryptedSecret.json', 'rb') as f:
        encrypted_data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data)

    return decrypted

if __name__ == '__main__':
    print(encrypt())
    # pass
