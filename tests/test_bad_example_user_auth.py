import json
import sys

import requests

# Login request
posts_response = requests.get(
    'http://127.0.0.1:8080/posts/list/my',
    headers=dict(
        User='6'
    )
)

if posts_response.status_code == 200:
    resp_data = posts_response.json()
    print(resp_data)
else:
    print('Could not authenitcate')
    sys.exit()

