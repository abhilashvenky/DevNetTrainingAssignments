import unittest
from db_parser import Parser

class TestParserMethods(unittest.TestCase):
    def test_json_parse(self):
        test_input_val = "../data/test_input.json"
        expected_return_val = {"ACCT<NUM1>":{"paid":0,"due":1},"ACCT<NUM2>":{"paid":2,"due":3}}
        self.assertEqual(Parser(test_input_val).get_parsed_data(), expected_return_val)

    def test_xml_parse(self):
        test_input_val = "../data/test_input.xml"
        expected_return_val = {"ACCTNUM1":{"paid":'0',"due":'1'},"ACCTNUM2":{"paid":'2',"due":'3'}}
        self.assertEqual(Parser(test_input_val).get_parsed_data(), expected_return_val)

    def test_yaml_parse(self):
        test_input_val = "../data/test_input.yml"
        expected_return_val = {"ACCTNUM1":{"paid":0,"due":1},"ACCTNUM2":{"paid":2,"due":3}}
        self.assertEqual(Parser(test_input_val).get_parsed_data(), expected_return_val)

if __name__ == '__main__':
    unittest.main()