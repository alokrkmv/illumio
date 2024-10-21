import sys
import os
import pytest
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get current file directory
project_root = os.path.dirname(current_dir)  # Get the parent directory (project root)
sys.path.append(project_root)


from processor.log_processor import FlowLogProcessor

class TestFlowLogProcessor:
    # Arrange
    def setup_method(self):
        # Arrange
        self.expected_count_with_tag = {'dhcp': 1, 'ftp': 1, 'Untagged': 5, 'security': 1}
        self.expected_count_with_pair = {('143', 'tcp'): 1, ('993', 'tcp'): 1, ('49155', 'tcp'): 1, ('49156', 'icmp'): 1, ('49157', 'icmp'): 1, ('49158', 'tcp'): 1, ('53', 'udp'): 1, ('1024', 'tcp'): 1}
        self.protocol_dict = {'0': 'hopopt', '1': 'icmp', '2': 'igmp', '3': 'ggp', '4': 'ipv4', '5': 'st', '6': 'tcp', '17': 'udp'}
        self.lookup_table_dict = {('143', 'tcp'): 'dhcp', ('53', 'udp'): 'security', ('443', 'dns'): 'sv_P4', 
        ('143', 'imap'): 'sv_P4', ('67', 'dhcp'): 'sv_P1', ('161', 'snmp'): 'snmp', 
        ('68', 'dhcp'): 'load_balancer', ('123', 'ntp'): 'snmp', ('993', 'tcp'): 
        'ftp', ('110', 'pop3'): 'dhcp', ('443', 'https'): 'vpn', ('25', 'smtp'): 
        'monitor', ('128', 'icmp'): 'sv_P1'}
        self.temp_file_path = "unit_tests/dummy_data_generators/sample_log.log"
        self.processor_object = FlowLogProcessor(self.protocol_dict, self.lookup_table_dict, self.temp_file_path)
    
    
    # execute and assert
    def test_process_logs(self):
        count_with_tag, count_with_pairs = self.processor_object.process_logs()
        assert(self.expected_count_with_tag == count_with_tag)
        assert(self.expected_count_with_pair == count_with_pairs)

    # execute and assert
    def test_version_2_parser(self):
        raw_log = "2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 993 6 15 12000 1620140761 1620140821 REJECT OK".split(" ")
        excepted_dstport = "993"
        expected_protocol = "tcp"
        expected_tag = "ftp"
        actual_dstport, actual_protocol, actual_tag = self.processor_object.version_2_parser(raw_log)
        assert(excepted_dstport == actual_dstport)
        assert(expected_protocol == actual_protocol)
        assert(expected_tag == actual_tag)

