from db_parser import Parser
import json
import requests

# Specify API endpoint
url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/network-device"

payload = {}

# Specify the auth token within header with key 'x-auth-token'
headers = {
  'x-auth-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1ZWNlNTc5ODc1MTYxMjAwY2M1NzA2M2QiLCJhdXRoU291cmNlIjoiaW50ZXJuYWwiLCJ0ZW5hbnROYW1lIjoiVE5UMCIsInJvbGVzIjpbIjVlNWE0MzI1NzUxNjEyMDBjYzRhYzk1ZSJdLCJ0ZW5hbnRJZCI6IjVlNWE0MzI1NzUxNjEyMDBjYzRhYzk1YyIsImV4cCI6MTU5MTA4ODEyMCwiaWF0IjoxNTkxMDg0NTIwLCJqdGkiOiJhOTZhZmE2Ni0yYTBlLTQ0NDMtOGJmYi00YjM0OGEwNWRkMDgiLCJ1c2VybmFtZSI6ImRuYWNkZXYifQ.XlgSlJnezIByuszKLU0-Qcko3WZYPxhOJwXLAq6HVaaAhS8YZBjIR5LwMmIkKAjvmqQgsEVUbRO1htzF6D1WlvaNgrOpiHPc3OWnT46s1uSUIAeRt92Xdv3fIAc79jewvTsMQffcPNIbsR1YsT5k1qGR0qJ9R5Rhauh-VfgfIrgUfkrScEBEjnW5KQZaTboXf7jM9rktAtXpb7FULYK6uhPevUGcGvS9VlmszokCbEeOA-ofRru8a_Icmqa5Uxik0qQdJyfBfSfzDUGhYCgmJ3NbxkvyUrTpNWsFJhQ9ia4rTrsBHMdxd8ASWdT3wEUBR9_VYhrA6oq4-KnXfljlwA'
}

# Use the requests module to query the sandboxdnac2 api of network device details
response = requests.request("GET", url, headers=headers, data = payload)

# Dump the reponse as JSON to data file store
json.dump(response.json(), open('../data/sandboxdnac2_devices.json', 'w'))

# Use the class written in the db_parser script to parse the JSON
parser = Parser('../data/sandboxdnac2_devices.json')
parsed_data = parser.get_parsed_data()

# Iterate through the parsed JSON.
for device in parsed_data['response']:
    # Print Device ID, type, family, softwareType, managementIpAddress
    print('Device ID :', device['id'])
    print('Device Type :', device['type'])
    print('Device Family :', device['family'])
    print('Software Type :', device['softwareType'])
    print('Management IP Address :', device['managementIpAddress'],'\n')