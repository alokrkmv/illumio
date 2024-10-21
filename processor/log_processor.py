import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get current file directory
project_root = os.path.dirname(current_dir)  # Get the parent directory (project root)
sys.path.append(project_root)

import csv

from helper.logger import Logger


class FlowLogProcessor:
    def __init__(self, protocol_dict : dict, lookup_table_dict : dict, 
                temp_file_path : str):
        self.log = Logger().get_logger()
        self.protocol_dict = protocol_dict
        self.lookup_table_dict = lookup_table_dict
        self.temp_file_path = temp_file_path
      
    def process_logs(self):
        """
        Process the flow log and writes the result into a thread-safe shared dict.
        """
        count_with_tag = {}
        count_with_pair = {}

        try:
            with open(self.temp_file_path, mode='r') as file:
                reader = csv.reader(file, delimiter=' ')
                for log in reader:
                    if not log:
                        continue
                    
                    parser = self.parser(log[0])
                    dstport, protocol, tag = parser(log)
                    
                    if not dstport or not protocol or not tag:
                        raise Exception("Unable to fetch relevant data from the logs")
                    
                
                    if tag not in count_with_tag:
                        count_with_tag[tag] = 1
                    else:
                        count_with_tag[tag] += 1
                    
            
                    if (dstport, protocol) not in count_with_pair:
                        count_with_pair[(dstport, protocol)] = 1
                    else:
                        count_with_pair[(dstport, protocol)] += 1  

        except FileNotFoundError:
            self.log.error("File not found!")
        except PermissionError:
            self.log.error("You don't have permission to access this file.")
        except Exception as e:
            self.log.error(f"Reading the file {self.temp_file_path} failed with error: {e}")
        finally:
            return count_with_tag, count_with_pair


    def parser(self, version):
        if version == "2":
            return self.version_2_parser
        else:
            return None
    def version_2_parser(self, raw_log):
        try:
            # Extract necessary columns from the flow log
            dstport = raw_log[6]
            protocol_num = raw_log[7]
            protocol = self.protocol_dict[protocol_num]
            
            
            # Check if the (dstport, protocol) combination is in the lookup table
            tag = self.lookup_table_dict.get((dstport, protocol), 'Untagged')
            return dstport, protocol, tag
        except Exception as e:
            self.log.exception("Something went wrong in parsing version 2 logs")

        
        

