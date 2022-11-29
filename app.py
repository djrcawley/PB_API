from flask import Flask
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def index():
    token_command = "curl  -d \"grant_type=client_credentials\" -d \"client_id=67677iepfii89k0milui2i5moa\" -d \"client_secret=foeos1u1a8gu11bs6gjfcvmgf3bq0gj65ara1eiao2bblr7gq9b\" -d \"scope=misc/decoder\" -H 'Content-Type:application/x-www-form-urlencoded' -X POST https://auth-preprod.pbtrack-test.com/oauth2/token"
    output = subprocess.check_output(token_command, shell=True) #Run in terminal
    outputJSON = json.loads(output) #Binary to JSON
    token = outputJSON['access_token'] #Get Token from JSON

    photoData = "/7rTZgCBNA0QywEAAACAYp5y/Qw=" #Photo Data
    shipping_info_command = "curl -G --data-urlencode \"data={}\" -d \"b64encoded=true\" -H \'x-api-key: Raqp2gTzJJ6JUQwPMAFa59BEPg9nofnN7V9nzCxf\' -H \"Authorization: Bearer {}\" \"https://preprod.pbtrack-test.com/decoder/v1/decode\"".format(photoData, token)
    shippingData = subprocess.check_output(shipping_info_command, shell=True)
    return json.loads(shippingData)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, debug=True)
