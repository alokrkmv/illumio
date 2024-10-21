## Problem statement

Write a program that can parse a file containing flow log data and maps each row to a tag based on a lookup table. The lookup table is defined as a csv file, and it has 3 columns, dstport,protocol,tag. The dstport and protocol combination decide what tag can be applied.

###  Steps to run the project.
1. Clone the repo into the local machine.
2. Make sure your current branch is **Main**.
3. cd into the root illumio folder
4. To run the program and generate output run ````bash run.sh <lookup_table_path> <log_file_path> <output_file_path>````. The command line arguments are optional and if not provided then default paths will be used.
5. The results will be stored in a txt file and the location of the file can be retrieved from console output. By default it is ````data/output/output.txt````

###  Testing and evaluation
#### Unit testing:
1. you can run the entire test suit using the bash file ````bash run_unit_tests.sh````
2. Test results can be viewed in the console

#### Loading testing:

Entire load testing was performed on a machine with a 2-core CPU and 8 GB RAM machine and with a **lookup table of size 10000 mappings**
#### Scenario 1: Log file size 10 MB (100k logs)

| Number of Processes |Execution time(in sec) | 
|----------|----------|
| 1   | 0.56   | 
| 2   | 0.46   | 
| 3   | 0.43   |
| 4   | 0.44   |

#### Scenario 2: Log file size 1.2 GB (10 million logs)

| Number of Processes |Execution time(in sec) | 
|----------|----------|
| 1   | 33   | 
| 2   | 22   | 
| 3   | 22   |
| 4   |  22  |

#### Analysis

1. In scenario 1 when the log file is small (~10MB) we don't see any significant improvement in time on increasing the number of processes from 1 to 2. This can be attributed to the fact that the overhead of multiprocessing (creating and managing processes) might overshadow any performance gain.
2. In scenario 2 when we increased the file size to 1.2 GB we can see a significant performance gain of ~11 seconds after increasing the number of processes from 1 to 2 as for large files with higher processing time the overhead of multiprocessing is significantly negligible compared to actual processing time. Any further increase in the number of worker processes isn't attributed to performance gain due to hardware limitations.

#### Steps for performing load testing
1. Checkout to **load_testing** branch.
2. ````cd unit_tests/dummy_data_generators````
3. Set the number of key mappings you want in lookup_tables  in **number_of_items** variable in **lookup_table_generator.py**. The default value is 10000
4. Execute ````python lookup_table_generator.py``` to generate the lookup table
5. Set the number of logs you want  to generate  in **number_of_items** variable in **sample_log_generator.py**. The default value is 100000
6. Execute ````python sample_log_generator.py``` to generate the log data
7. Once the lookup table and log data are generated, you can perform load testing by running the command ````bash run.sh unit_tests/dummy_data_generators/generated_lookup_table.csv unit_tests/dummy_data_generators/generated_data.log unit_tests/test_output.txt 4````
8. Where ````unit_tests/dummy_data_generators/generated_lookup_table.csv```` is path to the generated lookup table, ````dummy_data_generators/generated_data.log```` is path to the generated logs, ````unit_tests/test_output.txt```` path to the load testing output file and  ````4```` is number of worker process you want to spin.
9. The maximum number of worker processes that can be spun has been limited to 10 to prevent resource overuse.
10. The execution time in seconds will be printed on the console once the execution finishes. 

#### Time and Space complexity analysis
1. The time complexity of the code is O(N) where N is the number of log lines in each chunk for a particular process
2. As the entire lookup table is stored in memory space complexity is O(N) where N is the size of the lookup table. In the current implementation, I am not loading logs into memory and each process is reading and processing the logs one line at a time hence the space complexity of log processing is O(1).
#### Scope of Improvement

1. Fault tolerance can be added to respin a new worker process in case an existing one dies.
2. Instead of spinning a default number of worker process we can have a logic in place to spin the number of workers based on job size.

