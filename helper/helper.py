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
                port_number, port_name = row[:2]
                protocol_table[port_number] = port_name
        return protocol_table

    

        



