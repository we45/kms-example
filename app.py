from flask import Flask
import boto3
from uuid import uuid4
from os import urandom
import base64
from Crypto.Cipher import AES
from flask import render_template
import os
app = Flask(__name__)
kms_client = boto3.client('kms',region_name='us-west-2')


def pad(s): return s + (32 - len(s) % 32) * ' '


cmk_id = os.getenv('cmk_id')

@app.route('/encrypt', methods=['GET'])
def encrypt():
    message=b"supersecret"    
    data_key_response = kms_client.generate_data_key(KeyId=cmk_id, KeySpec='AES_256')
    data_key_encrypted, data_key_plaintext = data_key_response['CiphertextBlob'],data_key_response['Plaintext']
    iv = os.urandom(16)
    cipher = AES.new(data_key_plaintext, AES.MODE_CFB,iv)
    encrypted_cipher= cipher.encrypt(message)
    final_64 = base64.b64encode(encrypted_cipher)
    return render_template('index.html', CMK_ID=cmk_id,
                           data_key=data_key_encrypted, ciphertext=final_64, plaintext=message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


iv = b'WmiBaaAuyX7YCSTTPj07/c=='
iv = base64.b64decode(iv)