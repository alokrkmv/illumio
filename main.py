import os
import sys
import multiprocessing
import threading

from helper.helper import Helper
from helper.logger import Logger
from processor.log_processor import FlowLogProcessor
from helper import constants

def process_task(protocol_table_data, lookup_table_data, temp_file_path, result_queue):
    log_parser = FlowLogProcessor(protocol_table_data, lookup_table_data, temp_file_path)
    count_with_tag, count_with_pair = log_parser.process_logs()
    result_queue.put((count_with_tag, count_with_pair))

def merge_dictionaries(dict_list):
    """
    Merges a list of dictionaries by summing values for matching keys.
    """
    merged_dict = {}
    for d in dict_list:
        for key, value in d.items():
            if key in merged_dict:
                merged_dict[key] += value
            else:
                merged_dict[key] = value
    return merged_dict

log = Logger().get_logger()
if __name__ == '__main__':
    
    # Default file paths
    default_lookup_table_file = constants.LOOKUP_TABLE_FILE_PATH
    default_log_file_path = constants.FLOW_LOG_FILE_PATH
    default_output_file = constants.OUTPUT_FILE_PATH
    

    # Check if command-line arguments are passed, otherwise use default paths
    lookup_table_file = sys.argv[1] if len(sys.argv) > 1 else default_lookup_table_file
    log_file_path = sys.argv[2] if len(sys.argv) > 2 else default_log_file_path
    output_file = sys.argv[3] if len(sys.argv) > 3 else default_output_file

    helper_object = Helper(lookup_table_file, constants.PROTOCOL_MAPPING_FILE_PATH, output_file)
    lookup_table_data = helper_object.load_lookup_table_data()
    protocol_table_data = helper_object.load_protocol_data()

    # Create temp directory if it doesn't exist
    os.makedirs(constants.TEMP_DIRECTORY_PATH, exist_ok=True)

    processes = []
    result_queues = []


    # Split the original file into temporary files
    temp_files = helper_object.generate_temp_files(log_file_path, constants.TEMP_DIRECTORY_PATH, constants.NUMBER_OF_WORKERS)

    for temp_file in temp_files:
        result_queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=process_task, args=(protocol_table_data, lookup_table_data, temp_file, result_queue))
        processes.append(p)
        result_queues.append(result_queue)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    count_with_tag_results = []
    count_with_pair_results = []
    for q in result_queues:
        
        count_with_tag, count_with_pairs = q.get()  # Retrieve the result
        count_with_tag_results.append(count_with_tag)
        count_with_pair_results.append(count_with_pairs)

    # Merge the dictionaries from each process
    final_count_with_tag = merge_dictionaries(count_with_tag_results)
    final_count_with_pair = merge_dictionaries(count_with_pair_results)

    # Remove the temporary files
    for temp_file in temp_files:
        os.remove(temp_file)   

    
    # Generate the output file
    helper_object.write_output_to_file(final_count_with_tag, final_count_with_pair)

    print(f"Process completed successfully !!! Please find the output file at {output_file}")