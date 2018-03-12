# This is a python code
import kilo
import json
import requests

api_token = 'your_api_token'
api_url_base = 'https://api.digitalocean.com/v2/'

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}

def add_ssh_key(name, filename):

    api_url = '{0}accounts/keys'.format(api_url_base)

    with open(filename, 'r') as f:
        ssh_key = f.readline()

    ssh_key = {'name': name, 'public_key': ssh_key}

    response = requests.post(api_url, headers=headers, json=ssh_key)

    if response.status_code >= 500:
        print ('[!] [{0}] Server Error'.format(response.status_code))
        return None
    elif response.status_code == 404:
        print ('[!] [{0}] URL not found'.format(response.status_code, api_url))
        return None
    elif response.status_code == 401:
        print ('[!] [{0}] Authentication Failed'.format(response.status_code))
        return None
    elif response.status_code == 400:
        print ('[!] [{0}] Bad Request'.format(response.status_code))
        print (ssh_key)
        print (response.content)
        return None
    elif response.status_code == 300:
        print ('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        return None
    elif response.status_code == 201:
        added_key = json.loads(response.content)
        return added_key
    else:
        print ('[!] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None


# Calling above function and assign value to variable add_response:
add_response = add_ssh_key('tutorial_key', 'home/ntuser/.ssh/ntuser.pub')

if add_response is not None:
    print ('Your jey was added :')
    for k, v in add_response.items():
        print ('  {0}:{1}'.format(k, v))
else:
    print ('[!] Request Failed')
