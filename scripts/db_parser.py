#!/usr/bin/python3
print("Content-Type:text/html")
print("")

import cgi,cgitb
cgitb.enable() # Enable debugging
print("<h1>Below is the execution output of the script</h1>")
print("------------------------------------<br>")

import json
import xml.etree.ElementTree as ET 
import yaml
import os
import requests
# Create a parser class that can parse any input file (json/xml/yaml)
class Parser():

    def __init__(self, parse_request):
        # Class variable initializations
        self.parsed_data = None
        self.filepath = None
        self.api_end_point = None
        self.api_key = None

        # Local file path is given, directly proceed to parsing
        if 'filepath' in parse_request.keys():
            self.filepath = parse_request['filepath']
        # Remote API is given, pull file first and then parse
        else:
            self.request_api(parse_request['api_end_point'], parse_request['auth_type'], parse_request['auth_key'], parse_request['data'])

        # Calling specific methods within class as per file extension for parsing
        if '.json' in self.filepath:
            self.parse_json()
        elif '.xml' in self.filepath:
            self.parse_xml()
        elif '.yml' in self.filepath:
            self.parse_yml()

    # Method to parse JSON file
    def parse_json(self):
        # Read JSON:
        json_string = open(self.filepath).read()

        # Parse JSON:
        parsed_json = json.loads(json_string)

        # Save the parsed JSON (Python dictionary):
        self.parsed_data = parsed_json

    # Method to parse XML file of accounts with due and paid
    def parse_xml(self):
        # Create element tree object by passing filepath to ET 
        tree = ET.parse(self.filepath) 
    
        # Get root element of xml
        root = tree.getroot() 
    
        # Create a dict for all accounts
        accounts = {} 
    
        # Iterate through all accounts
        for account in root: 
    
            # Create a dict to hold payable and paid
            account_amounts = {} 

            # Iterate through child elments of each account
            for account_amount in account: 
    
                # Converting account dues and paid to dict
                account_amounts[account_amount.tag] = account_amount.text 
    
            # Adding current account to parsed accounts dict
            accounts[account.tag] = account_amounts
        
        # Save parsed dict of all accounts
        self.parsed_data = accounts

    # Method to parse YML file
    def parse_yml(self):
        # Open yaml
        yaml_file = open(self.filepath)
            
        # Parse yaml
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        
        # Save the parsed yaml dict
        self.parsed_data = data

    # Method to pull parsable file from a given API
    def request_api(self, api_end_point, auth_type, auth_key, data):
        # Use the requests module to query the given API
        response = requests.request("GET", api_end_point, headers={auth_type: auth_key}, data = data)

        # Dump the reponse as JSON to data file store using api-end-point as file name
        json.dump(response.json(), open('../data/' + api_end_point.split('/')[-1] + '.json', 'w'))

        # Save the filepath for further parsing
        self.filepath = '../data/' + api_end_point.split('/')[-1] + '.json'

    # Getter function for Parser objects
    def get_parsed_data(self):
        return self.parsed_data

# Testing the parser class
if __name__ =='__main__':
    # Iterating through all files in data directory
    for filename in os.listdir('../data/'):

        # Parse DB objects only
        if 'db' in filename:

            # Create a parse request with filepath
            parse_request = {'filepath' : '../data/' + filename}

            # Create Parser object for parsing the request and print the parsed dictionary
            parser = Parser(parse_request)
            parsed_data = parser.get_parsed_data()
            print('Parsed dictionary : ', parsed_data)

            # Format and print the parsed data
            print('\nAccount Details : ')
            print('-------------------\n')
            for account in parsed_data:
                print('ACCT NUMBER :', account[4:])
                print('Paid : ', parsed_data[account]['paid'])
                print('Due : ', parsed_data[account]['due'],"\n")

    parse_request = {
    'api_end_point' : 'https://sandboxdnac2.cisco.com/dna/intent/api/v1/network-device', 
    'auth_type' : 'x-auth-token',
    'auth_key' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1ZWNlNTc5ODc1MTYxMjAwY2M1NzA2M2QiLCJhdXRoU291cmNlIjoiaW50ZXJuYWwiLCJ0ZW5hbnROYW1lIjoiVE5UMCIsInJvbGVzIjpbIjVlNWE0MzI1NzUxNjEyMDBjYzRhYzk1ZSJdLCJ0ZW5hbnRJZCI6IjVlNWE0MzI1NzUxNjEyMDBjYzRhYzk1YyIsImV4cCI6MTU5MTIwNzY2NiwiaWF0IjoxNTkxMjA0MDY2LCJqdGkiOiI1NmE5ZTA0Ny03NjNhLTQ5MzYtYWUwOS05OTllZDA5YzQyZjUiLCJ1c2VybmFtZSI6ImRuYWNkZXYifQ.YCbGN_KlGd9mMV-wr99K-0wr6sA_g2SRq534STzRFH3-nl9t3CvnBNzI5iZEF7_1BVBi9FOa8O8dJNOl26pipDpHPJZh7GgnXXuokq5wn3EKbT5OTz5N0rxJ1S8Ga_78v4dEhvYU8d-_b739Jof8A_R7soY12tfCiujFNqt4DmOQAefNUZqWEonG60ZPTS3MKstA2wMn1mdBWG5aUA77M0EvFFTRLdniKuz3lQ7r_pZPdr7o0rMibycStJBg0HV8cIgwhNRBO7DcScPf21ovzeeuzxGezIZcd74qVafxo8VgBSzpfojD7coqg-iZajRKIurNmDV76rG1ydi23Nfy4A',
    'data' : {}
    }

    # Use the class written in the db_parser script to parse the JSON
    parser = Parser(parse_request)
    parsed_data = parser.get_parsed_data()

    # Iterate through the parsed JSON.
    for device in parsed_data['response']:
        # Print Device ID, type, family, softwareType, managementIpAddress
        print('Device ID :', device['id'])
        print('Device Type :', device['type'])
        print('Device Family :', device['family'])
        print('Software Type :', device['softwareType'])
        print('Management IP Address :', device['managementIpAddress'],'\n')