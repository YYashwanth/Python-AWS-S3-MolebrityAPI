"""
To run the script, install requests module (using pip - pip install requests)
python upload.py --file <path_to_image_file>
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
	url = 'https://api.molebrity.io/s3'
	data = {"contentType": content_type}
	data = json.dumps(data)
	
	response = requests.post(url, data=data, headers=headers).json()
	return response

