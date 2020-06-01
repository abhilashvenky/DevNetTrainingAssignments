import json
import xml.etree.ElementTree as ET 
import yaml
import os

# Create a parser class that can parse any input file (json/xml/yaml)
class Parser():

    def __init__(self, filepath):
        # Class variable initializations
        self.filepath = filepath
        self.parsed_data = None

        # Calling specific methods within class as per file extension
        if '.json' in filepath:
            self.parse_json()
        elif '.xml' in filepath:
            self.parse_xml()
        elif '.yml' in filepath:
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

    def get_parsed_data(self):
        # Getter function for Parser objects
        return self.parsed_data

# Testing the parser class
if __name__ =='__main__':
    # Iterating through all files in data directory
    for filename in os.listdir('../data/'):
        if 'db' in filename:
            parser = Parser('../data/' + filename)
            parsed_data = parser.get_parsed_data()
            print('Parsed dictionary : ', parsed_data)
            print('\nAccount Details : ')
            print('-------------------\n')
            for account in parsed_data:
                print('ACCT NUMBER :', account[4:])
                print('Paid : ', parsed_data[account]['paid'])
                print('Due : ', parsed_data[account]['due'],"\n")