import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get current file directory
project_root = os.path.dirname(current_dir)  # Get the parent directory (project root)
sys.path.append(project_root)

import pytest
from helper.helper import Helper
from helper import constants

class TestHelper:
    # Arrange
    def setup_method(self):
        # Arrange
        self.expected_lookup_table_data = {('143', 'tcp'): 'dhcp', ('53', 'udp'): 'security', ('443', 'dns'): 'sv_P4', 
        ('143', 'imap'): 'sv_P4', ('67', 'dhcp'): 'sv_P1', ('161', 'snmp'): 'snmp', 
        ('68', 'dhcp'): 'load_balancer', ('123', 'ntp'): 'snmp', ('993', 'tcp'): 
        'ftp', ('110', 'pop3'): 'dhcp', ('443', 'https'): 'vpn', ('25', 'smtp'): 
        'monitor', ('128', 'icmp'): 'sv_P1'}
        self.expected_protocol_data = {'0': 'hopopt', '1': 'icmp', '2': 'igmp', '3': 'ggp', '4': 'ipv4', '5': 'st', '6': 'tcp', '17': 'udp'}
        self.sample_lookup_table_path = "unit_tests/dummy_data_generators/sample_lookup_table.csv"
        self.protocol_mapping_table_path = 'unit_tests/dummy_data_generators/protocol_mapping_sample.csv'
        self.output_file_path = 'unit_tests/test_output.txt'
        self.helper_obj = Helper(self.sample_lookup_table_path, self.protocol_mapping_table_path, self.output_file_path)
        self.number_of_workers = 4
    
    
    # execute and assert
    def test_load_lookup_table_data(self):
        actual_lookup_table_data = self.helper_obj.load_lookup_table_data()
        assert(self.expected_lookup_table_data == actual_lookup_table_data)

    def test_load_protocol_data(self):
        actual_protocol_table_data = self.helper_obj.load_protocol_data()
        assert(self.expected_protocol_data == actual_protocol_table_data)

    def test_generate_temp_files(self):
        temp_files = self.helper_obj.generate_temp_files(constants.FLOW_LOG_FILE_PATH, constants.TEMP_DIRECTORY_PATH, self.number_of_workers)
        assert(len(temp_files) == self.number_of_workers)

