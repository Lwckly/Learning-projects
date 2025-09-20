import requests

url="https://pokeapi.co/api/v2/"

def api_call(name):
    new_url= f"{url}/pokemon/{name}"
    call=requests.get(new_url)
    if call.status_code==200:
        return call.json()  # up to here, retrieves hash, put in variable to make it usable
    else:
        print(f"Failed to retrieve data {call.status_code}")


name="ditto"
info=api_call(name)

if info:
    print(f"{info["name"]}")
    print(f"{info["height"]}")
    print(f"{info["moves"]}")
