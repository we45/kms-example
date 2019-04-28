from flask import Flask
import boto3
from uuid import uuid4
from os import urandom
import base64
from Crypto.Cipher import AES
from flask import render_template

app = Flask(__name__)
client = boto3.client('kms')


def pad(s): return s + (32 - len(s) % 32) * ' '


cmk_id = '48e35447-0053-471c-a8c9-cb22cce6a1a7'


@app.route('/encrypt', methods=['GET'])
def encrypt():
    data_key = client.generate_data_key(
        KeyId=cmk_id,
        KeySpec="AES_256"
    )
    ciphertext_blob = base64.b64encode(data_key.get('CiphertextBlob'))
    plaintext_key = data_key.get('Plaintext')
    iv = urandom(16)
    ccode = str(uuid4())
    stuff_char = "$"
    cipher = AES.new(plaintext_key, AES.MODE_CFB, iv)
    final_ciphertext = stuff_char + iv + stuff_char + cipher.encrypt(pad(ccode))
    final_64 = base64.b64encode(final_ciphertext)
    return render_template('index.html', CMK_ID=cmk_id,
                           data_key=ciphertext_blob, ciphertext=final_64, plaintext=ccode)


if __name__ == '__main__':
    app.run(debug=True)