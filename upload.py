"""
To run the script, install requests module (using pip - pip install requests)
python realmole.py --file <path_to_image_file>
"""

# Import modules
import requests
import argparse
import imghdr
import json
import pprint


def get_file_signature(content_type):
    """
    This functions gets the S3 presigned URL used to upload the photo from users's computer, also generates a unique uuid to identify the photo
    """
    headers = {
        'origin': 'https://molebrity.io',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'authority': 'api.molebrity.io'
    }
   
    (parameter_list):
        pass(self, parameter_list):
        pass
    url = 'https://api.molebrity.io/s3'
    data = {"contentType": content_type}
    data = json.dumps(data)
    
    response = requests.post(url, data=data, headers=headers).json()
    return response


def find_match(uuid):
    """
    Once the photo has been uploaded, we call the match API with the uuid.
    """
    url = 'https://api.molebrity.io/match'
    headers = {
        'origin': 'https://molebrity.io',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'content-type': 'text/plain;charset=UTF-8',
        'accept': '*/*',
        'authority': 'api.molebrity.io'
    }
    data = {"uuid": uuid}
    data = json.dumps(data)
    response = requests.post(url, data=data, headers=headers).json()
    return response


def run():

    # Get the file path passed in as an argument to the script
    parser = argparse.ArgumentParser(description='Molebrity CLI')
    parser.add_argument('--file', dest='file', help='Input image file', action='store', required=True)
    args = parser.parse_args()
    img_file = args.file

    # Find the image file type, currently the API only accepts JPG/PNG files
    file_type = imghdr.what(img_file)
    if file_type == 'png':
        content_type = 'image/png'
    elif file_type == 'jpeg':
        content_type = 'image/jpeg'
    else:
        print("Only jpeg/png files are supported")
        return

    # Get the presigned S3 url and the uuid
    response = get_file_signature(content_type)
    upload_url = response['url']
    uuid = response['uuid']
    
    # Upload the image to S3
    with open(img_file, 'rb') as data:
        requests.put(upload_url, data=data, headers = {'Content-Type': content_type})

    # Call the match API
    results = find_match(uuid)
    pprint.pprint(results)

    
if __name__ == "__main__":
    run()
