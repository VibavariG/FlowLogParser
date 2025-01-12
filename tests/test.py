import unittest
from unittest.mock import patch
import os
from FlowLogParser import load_lookup_table, parse_flow_logs, map_logs_to_tags, write_output,load_ip_numbers_to_hashmap


class TestFlowLogParser(unittest.TestCase):
    def setUp(self):
        self.test_cases = [
            {
                "flow_log_file": "tests/flow_logs_test_1.txt",
                "lookup_table_file": "tests/lookup_table_test_1.csv",
                "number_ip_map_file": "data/number_ip_map.txt",     #using the map file unser data/
                "expected_output_file": "tests/expected_output_1.txt",
                "actual_output_file": "tests/test_actual_output_1.txt",
            },
            {
                "flow_log_file": "tests/flow_logs_test_2.txt",
                "lookup_table_file": "tests/lookup_table_test_2.csv",
                "number_ip_map_file": "data/number_ip_map.txt",        #using the map file unser data/  
                "expected_output_file": "tests/expected_output_2.txt",
                "actual_output_file": "tests/test_actual_output_2.txt",
            },
            # Add more cases as needed
        ]

    def run_test_case(self, test_case):
        with patch("FlowLogParser.FLOW_LOG_FILE", test_case["flow_log_file"]), \
             patch("FlowLogParser.LOOKUP_TABLE_FILE", test_case["lookup_table_file"]), \
             patch("FlowLogParser.NUMBER_IP_MAP", test_case["number_ip_map_file"]), \
             patch("FlowLogParser.OUTPUT_FILE", test_case["actual_output_file"]):

            if os.path.exists(test_case["actual_output_file"]):
                os.remove(test_case["actual_output_file"])

            # Loading test data
            lookup_table = load_lookup_table(test_case["lookup_table_file"])
            logs = parse_flow_logs(test_case["flow_log_file"])
            number_ip_mapping = load_ip_numbers_to_hashmap(test_case["number_ip_map_file"])

            # Running the main processing functions
            tag_counter, port_protocol_counter, untagged_count = map_logs_to_tags(
                logs, lookup_table, number_ip_mapping
            )
            write_output(tag_counter, port_protocol_counter, untagged_count, test_case["actual_output_file"])

            # Compare the generated output with the expected output
            with open(test_case["actual_output_file"], 'r') as actual, \
                 open(test_case["expected_output_file"], 'r') as expected:
                actual_content = actual.read().strip()
                expected_content = expected.read().strip()
                self.assertEqual(actual_content, expected_content, f"Test failed for case: {test_case}")
    
    # for more than 2 test cases
    # def test_flow_log_parser_cases(self):
    #     for test_case in self.test_cases:
    #         with self.subTest(test_case=test_case):
    #             self.run_test_case(test_case)

    def test_case_1(self):
        test_case = self.test_cases[0]
        self.run_test_case(test_case)
    
    def test_case_2(self):
        test_case = self.test_cases[1]
        self.run_test_case(test_case)


if __name__ == "__main__":
    unittest.main(verbosity=2)
