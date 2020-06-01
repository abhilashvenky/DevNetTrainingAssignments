from db_parser import Parser

# Use the class written in the db_parser script to parse the JSON
parser = Parser('../data/dnac_devices.json')
parsed_data = parser.get_parsed_data()

# Iterate through the parsed JSON.
for device in parsed_data['response']:
    # Printing Device ID, type, family, softwareType, managementIpAddress
    print('Device ID :', device['id'])
    print('Device Type :', device['type'])
    print('Device Family :', device['family'])
    print('Software Type :', device['softwareType'])
    print('Management IP Address :', device['managementIpAddress'],'\n')