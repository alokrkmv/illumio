import csv

from helper.logger import Logger


class FlowLogParser:
    def __init__(self, protocol_dict : dict, lookup_table_dict : dict, 
                temp_file_path : str, count_with_tag : dict, count_with_pair : dict,
                tag_dict_lock, pair_dict_lock):
        # Initializing the logger
        self.log = Logger().get_logger()
        self.protocol_dict = protocol_dict
        self.lookup_table_dict = lookup_table_dict
        self.temp_file_path = temp_file_path
        self.count_with_tag = count_with_tag
        self.count_with_pair = count_with_pair
        self.tag_dict_lock = tag_dict_lock
        self.pair_dict_lock = pair_dict_lock
    


    def process_logs(self):
        """
            Process the flow log and writes the result into thread safe shared dict.
        """
        
        try:
            with open(self.temp_file_path, mode='r') as file:
                reader = csv.reader(file, delimiter=' ')
                flow_logs = list(reader)
                for log in flow_logs:
                    parser = self.parser(log[0])
                    dstport, protocol, tag = parser(log)
                    if not dstport or not protocol or not tag:
                        raise Exception("Unable to fetch relevant data from the logs")
                    if tag not in self.count_with_tag:
                        with self.tag_dict_lock:
                            self.count_with_tag[tag] = 1
                    else:
                        with self.tag_dict_lock:
                            self.count_with_tag[tag]+=1
                    if (dstport, protocol) not in self.count_with_tag:
                        with self.pair_dict_lock:
                            self.count_with_pair[(dstport, protocol)] = 1
                    else:
                        with self.pair_dict_lock:
                            self.count_with_pair[(dstport, protocol)]+=1  
        except FileNotFoundError:
            self.log.error("File not found!")
        except PermissionError:
            self.log.error("You don't have permission to access this file.")
        except Exception as e:
            self.log.error(f"Reading the file {self.temp_file_path} failed with error: {e}")
    
    def parser(self, version):
        match version:
            case "2":
                return self.version_2_parser
            case _:
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

        
        

