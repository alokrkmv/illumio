## Problem statement

Write a program to parse a file containing flow log data and map each row to a tag based on a lookup table. The lookup table is defined as a CSV file, and it has 3 columns, dstport, protocol, and tag. The dstport and protocol combination decide what tag can be applied.

###  Steps to run the project.
1. Requires **python version >=3.10.x**
1. Clone the repo into the local machine.
2. Make sure your current branch is **Main**.
3. cd into the root **illumio** folder
4. To run the program and generate output, run ````bash run. sh lookup_table_path> log_file_path> output_file_path>````. The command line arguments are optional, and if not provided, default paths will be used.
5. The results will be stored in a txt file and the location of the file can be retrieved from console output. By default it is ````data/output/output.txt````

###  Testing and evaluation
#### Unit testing:
1. you can run the entire test suit using the bash file ````bash run_unit_tests.sh````
2. Test results can be viewed in the console

#### Loading testing:

Conducted loading testing by generating  a lookup table containing **10,000 mappings** and generating a log file of **~10MB** in size. This approach allowed me to evaluate the system's performance  and scalability under high-load conditions, effectively assessing its performance at the upper limits of expected usage. The system was able to generate the output file in **~22** seconds running on **2 core** machine with **2 worker processes**. Increasing the number of worker node doesn't seem to have much affect on the performance which could be a result of hardware limitations.

#### Steps for performing load testing
1. Checkout to **load_testing** branch.
2. ````cd unit_tests/dummy_data_generators````
3. Set the number of key mappings you want in lookup_tables  in **number_of_items** variable in **lookup_table_generator.py**. The default value is 10000
4. Execute ````python lookup_table_generator.py``` to generate the lookup table
5. Set the number of logs you want  to generate  in **number_of_items** variable in **sample_log_generator.py**. The default value is 100000
6. Execute ````python sample_log_generator.py``` to generate the log data
7. Once the both lookup table and log data are generated you can perform load testing by running the command ````bash run.sh unit_tests/dummy_data_generators/generated_lookup_table.csv unit_tests/dummy_data_generators/generated_data.log unit_tests/test_output.txt 4````
8. Where ````unit_tests/dummy_data_generators/generated_lookup_table.csv```` is path to the generated lookup table, ````dummy_data_generators/generated_data.log```` is path to the generated logs, ````unit_tests/test_output.txt```` path to the load testing output file and  ````4```` is number of worker process you want to spin.
9. The maximum number of worker processes that can be spun has been limited to 10 to prevent resource overuse.
10. The execution time in seconds will be printed on the console once the execution finishes. 

#### Scope of Improvement

1. Fault tolerance can be added to respin a new worker process in case an existing one dies.
2. Instead of spinning a default number of worker processes we can have a logic in place to spin a number of workers process dynamically based on job size.
