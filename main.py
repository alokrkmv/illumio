import os
import sys
import multiprocessing
import threading
import time

from helper.helper import Helper
from helper.logger import Logger
from processor.log_processor import FlowLogProcessor
from helper import constants

log = Logger().get_logger()
if __name__ == '__main__':

   
    # Default file paths
    default_lookup_table_file = constants.LOOKUP_TABLE_FILE_PATH
    default_log_file_path = constants.FLOW_LOG_FILE_PATH
    default_output_file = constants.OUTPUT_FILE_PATH
    default_number_of_worker = constants.NUMBER_OF_WORKERS
    

    # Check if command-line arguments are passed, otherwise use default paths
    lookup_table_file = sys.argv[1] if len(sys.argv) > 1 else default_lookup_table_file
    log_file_path = sys.argv[2] if len(sys.argv) > 2 else default_log_file_path
    output_file = sys.argv[3] if len(sys.argv) > 3 else default_output_file
    number_of_workers = int(sys.argv[4]) if len(sys.argv) > 3 else default_number_of_worker

    # Limiting the maximum number of worker processes to 10
    print(number_of_workers)
    number_of_workers = min(number_of_workers, 10)

    helper_object = Helper(lookup_table_file, constants.PROTOCOL_MAPPING_FILE_PATH, output_file)
    lookup_table_data = helper_object.load_lookup_table_data()
    protocol_table_data = helper_object.load_protocol_data()

    # Create temp directory if it doesn't exist
    os.makedirs(constants.TEMP_DIRECTORY_PATH, exist_ok=True)

    # Create a Manager to handle the shared dictionary
    manager = multiprocessing.Manager()
    count_with_tag = manager.dict()
    count_with_pairs = manager.dict()

    # Thread lock for safe writing
    tag_dict_lock = threading.Lock()  
    pair_dict_lock = threading.Lock()

    # Split the original file into temporary files
    temp_files = helper_object.generate_temp_files(log_file_path, constants.TEMP_DIRECTORY_PATH, number_of_workers)

    def process_task(protocol_table_data, lookup_table_data, temp_file_path, count_with_tag, 
                    count_with_pairs, tag_dict_lock, pair_dict_lock):
        # Create an instance of MyObject in each process
        log_parser = FlowLogProcessor( protocol_table_data, lookup_table_data, temp_file_path, count_with_tag, count_with_pairs, tag_dict_lock, pair_dict_lock)
        log_parser.process_logs()

    # Create processes for each chunk
    start_time = time.time()
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

    end_time = time.time()
    execution_time_ms = (end_time - start_time)

    print(f"Process completed successfully in {execution_time_ms} seconds!!! Please find the output file at {output_file}")