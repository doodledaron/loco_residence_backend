#this is just a playground to call the APIs
import requests

endpoint = "https://httpbin.org/anything"

get_res = requests.get(endpoint)

print(get_res.text)