import requests

def Request(text):
    url = 'https://magicloops.dev/api/loop/run/450ea510-e8e7-40c9-84d3-d1c411ddf3ba'
    payload = {"consulta": text}

    response = requests.get(url, json=payload)
    responseJson = response.json()
    print(f"STATUS: {responseJson['status']}")
    print(f"OUTPUT: {responseJson['loopOutput']}")
    return responseJson['loopOutput']