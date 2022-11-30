from flask import Flask, request
from werkzeug.utils import secure_filename
import os
import subprocess
import json

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def index():
    file = request.files['file'] #Retrieve File
    file_name = secure_filename(file.filename) #Security
    file.save(os.path.join('/var/www/html/flaskAPI/barcode_decoder/', file_name))#Move file to docker folder

    decode_command = "cd /var/www/html/flaskAPI/barcode_decoder/ && sudo /bin/bash decode.sh {}".format(file_name) #Decode

    image_binary_output = subprocess.check_output(decode_command, shell=True)
    photo_binary = image_binary_output.decode("utf-8")

    token_command = "curl  -d \"grant_type=client_credentials\" -d \"client_id=67677iepfii89k0milui2i5moa\" -d \"client_secret=foeos1u1a8gu11bs6gjfcvmgf3bq0gj65ara1eiao2bblr7gq9b\" -d \"scope=misc/decoder\" -H 'Content-Type:application/x-www-form-urlencoded' -X POST https://auth-preprod.pbtrack-test.com/oauth2/token"
    output = subprocess.check_output(token_command, shell=True) #Run in terminal
    outputJSON = json.loads(output) #Binary to JSON
    token = outputJSON['access_token'] #Get Token from JSON

    shipping_info_command = "curl -G --data-urlencode \"data={}\" -d \"b64encoded=true\" -H \'x-api-key: Raqp2gTzJJ6JUQwPMAFa59BEPg9nofnN7V9nzCxf\' -H \"Authorization: Bearer {}\" \"https://preprod.pbtrack-test.com/decoder/v1/decode\"".format(photo_binary, token)
    shippingData = subprocess.check_output(shipping_info_command, shell=True)
    return json.loads(shippingData)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, threaded=True)

