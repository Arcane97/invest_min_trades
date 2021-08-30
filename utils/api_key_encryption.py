from cryptography.fernet import Fernet
from traceback import format_exc

key = b'lRbF2NOa-1-3Bhv7mow_oqyYz0iw0mHYz89N7RIRK-s='


def encrypt(text):
    utf8_text = text.encode('utf-8')

    cipher = Fernet(key)
    try:
        encrypted_text = cipher.encrypt(utf8_text)
    except:
        print('decrypt', format_exc())
        return ''

    str_encrypted_text = encrypted_text.decode()

    return str_encrypted_text


def decrypt(encrypted_text):
    utf8_text = encrypted_text.encode('utf-8')

    decipher = Fernet(key)
    try:
        decrypted_text = decipher.decrypt(utf8_text)

        str_decrypted_text = decrypted_text.decode()
    except:
        print('decrypt', format_exc())
        return ''
    return str_decrypted_text


if __name__ == "__main__":
    encrypted_text = encrypt('meme')
    print(encrypted_text)

    decrypted_text = decrypt(encrypted_text)
    print(decrypted_text)
