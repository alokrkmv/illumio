import csv
from .logger import Logger


class Helper:
    def __init__(self, lookup_file_path : str = None, protocol_mapping_file_path : str = None, output_file_path : str = None):
        self.output_file_path = output_file_path
        self.lookup_table_file_path = lookup_file_path
        self.protocol_mapping_file_path = protocol_mapping_file_path
        self.log = Logger().get_logger()
    
    def __read_from_csv(self, csv_file_path : str) -> object:
        """
            Args:
                csv_file_path: Path to the csv file.

            Returns:
                float: iterable reader object.
        """
        try:
            reader_object = open(csv_file_path, mode='r')
            return reader_object
        except FileNotFoundError:
            self.log.error("File not found!")
        except PermissionError:
            self.log.error("You don't have permission to access this file.")
        except Exception as e:
            self.log.error(f"Reading the file {csv_file_path} failed with error: {e}")


    
    def load_lookup_table_data(self, lookup_table_file_path : str = None) -> dict:
        """
            Loads the lookup table and creates a in memory dictionary with (dstport, protocol) as key and tag as value
            Args:
                lookup_table_file_path: Path to the lookup file.

            Returns:
                dict: An in memory dict of lookup_table.
        """
        lookup_file = lookup_table_file_path if lookup_table_file_path else self.lookup_table_file_path
        
        if not lookup_file:
            raise Exception("Looktable path cannot be none") 
        lookup_table = {}

        file_object = self.__read_from_csv(lookup_file)
        csv_reader = csv.reader(file_object)
        next(csv_reader)  
       
        for row in csv_reader:
            dstport, protocol, tag = row
            lookup_table[(dstport, protocol.lower())] = tag
        return lookup_table

    def load_protocol_data(self, protocol_mapping_file_path : str = None) -> dict:
        """
            Loads the port data and creates an in memory dictionary with port_number as key and portname as value
            Args:
                port_mapping_file_path: Path to the port mapping file.

            Returns:
                dict: An in memory dict of port mapping table.
        """
        protocol_file = protocol_mapping_file_path if protocol_mapping_file_path else self.protocol_mapping_file_path
        
        if not protocol_file:
            raise Exception("Protocol mapping file path cannot be none") 
        protocol_table = {}

        file_object = self.__read_from_csv(protocol_file)
        csv_reader = csv.reader(file_object)
        next(csv_reader)  
        
        for row in csv_reader:
            if len(row) >= 2:  # Ensure there are at least 2 columns
                protocol, port_name = row[:2]
                protocol_table[protocol] = port_name.lower()
        return protocol_table

    def generate_temp_files(self, log_file_path, temp_directory, number_of_workers):
        """
            Splits the log files into multiple chunks.
            Args:
                input_file_path: Input log file path
                num_workers: Number of worker processes
        """
        temp_files = []
        with open(log_file_path, 'r') as f:
            lines = f.readlines()
        
        # Divide the entire data into number of chunks equal to the number of workers process spawned
        chunk_size = len(lines) // number_of_workers + (len(lines) % number_of_workers > 0)
        
        for i in range(number_of_workers):
            temp_file_path = f'{temp_directory}/worker_{i}.log'
            temp_files.append(temp_file_path)
            with open(temp_file_path, 'w') as temp_file:
                for _ in range(chunk_size):
                    if lines:
                        temp_file.write(lines.pop(0))
                    else:
                        break
    
        return temp_files

    def write_output_to_file(self, count_with_tag, count_with_pairs):
        """
            Writes the data to the out file
            Args:
                tag_dict: Count for each tag
                pair_dict: Count for (port, protocol)
        """
        with open(self.output_file_path, 'w') as file:
            # Write Output 1
            file.write("------------------------------------------Output 1---------------------------------------------------\n")
            file.write("Port,Protocol,Count\n")
            for key, count in count_with_pairs.items():
                file.write(f"{key[0]},{key[1]},{count}\n")

            file.write("\n")
            
            # Write Output 2
            file.write("------------------------------------------------------Output 2------------------------------------------------\n")
            file.write("Tag,Count\n")
            
            # Sort tag_dict by tag name
            sorted_tags = sorted(count_with_tag.items())
            print(sorted_tags)

            for tag, count in sorted_tags:
                file.write(f"{tag},{count}\n")

    

        



