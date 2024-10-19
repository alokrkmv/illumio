import os
import multiprocessing
import threading

from helper.helper import Helper
from helper.logger import Logger
from parser.log_parser import FlowLogParser
from helper import constants

log = Logger().get_logger()
if __name__=='__main__':
    helper_object = Helper(constants.LOOKUP_TABLE_FILE_PATH, constants.PROTOCOL_MAPPING_FILE_PATH, constants.OUTPUT_FILE_PATH)
    lookup_table_data = helper_object.load_lookup_table_data()
    protocol_table_data = helper_object.load_protocol_data()

    # Create temp directory if it doesn't exist
    os.makedirs(constants.TEMP_DIRECTORY_PATH, exist_ok=True)

    # Create a Manager to handle the shared dictionary
    manager = multiprocessing.Manager()
    count_with_tag = manager.dict()
    count_with_pairs = manager.dict()

    tag_dict_lock = threading.Lock()  # Lock to ensure thread safety
    pair_dict_lock = threading.Lock()

    # Split the original file into temporary files
    temp_files = helper_object.generate_temp_files(constants.FLOW_LOG_FILE_PATH, constants.TEMP_DIRECTORY_PATH, constants.NUMBER_OF_WORKERS)

    def process_task(protocol_table_data, lookup_table_data, temp_file_path, count_with_tag, 
                    count_with_pairs, tag_dict_lock, pair_dict_lock):
        # Create an instance of MyObject in each process
        log_parser = FlowLogParser( protocol_table_data, lookup_table_data, temp_file_path, count_with_tag, count_with_pairs, tag_dict_lock, pair_dict_lock)
        log_parser.process_logs()

     # Create processes for each temp file
    processes = []
    for temp_file in temp_files:
        p = multiprocessing.Process(target=process_task, args=(protocol_table_data, lookup_table_data, temp_file, count_with_tag, count_with_pairs, tag_dict_lock, pair_dict_lock))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # Remove the temporary files
    for temp_file in temp_files:
        os.remove(temp_file)   
    
    # Generate the output file
    helper_object.write_output_to_file(count_with_tag, count_with_pairs)