# Flow Log Parser 
### Description
Flow Log Parser is a program that can parse a file containing flow log data and maps each row to a tag based on a lookup table. The lookup table is defined as a csv file, and it has 3 columns, dstport,protocol,tag. The dstport and protocol combination decide what tag can be applied.   

### Run
1. The FlowLogParser.py contains the program to parse a file containing flow log data and map each row to a tag based on a lookup table.
2. User can overwrite the data in data/flow_logs.txt and data/lookup_table.csv
3. On running FlowLogParser.py, output.txt will be generated under the data/ folder
4. Local Build
```
git clone https://github.com/VibavariG/FlowLogParser.git
cd FlowLogParser
python3 -m FlowLogParser
```

### Folder Structure
```
FlowLogParser/
├── data/
│   ├── flow_logs.txt
│   ├── lookup_table.csv
│   ├── number_ip_map.txt
├── tests/
│   ├── flow_logs_test_<number>.txt
│   ├── lookup_table_test_<number>.csv
│   ├── expected_output_<number>.txt
│   ├── test.py
├── FlowLogParser.py
```
### Assumptions:
#### Input Requirements
1. Flow Logs
    - File name: ```flow_logs.txt```
    - Location: Must be placed in the data/ folder.
    - Format:
        - Each flow log entry is a new line.
        - There are no empty lines in the file.
        - Each flow log consists of space-separated values.
        - Column Mapping: The space-separated values correspond to the following columns (Version 2 logs): version, account-id, interface-id, srcaddr, dstaddr, srcport, dstport, protocol, packets, bytes, start, end, action, log-status
        - (Source: https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html).
2. Lookup Table
    - File Name: ```lookup_table.csv```
    - Location: Must be placed in the data/ folder.
    - Format:
        - The first line contains comma-separated column names.
        - Subsequent lines contain comma-separated values corresponding to the columns: dstport, protocol, and tag.
3. Protocol Mapping
    - File Name: ```number_ip_map.txt```
    - Location: Placed in the data/ folder. User doesn't need to provide this as an input. This should be a part of the program.
    - Format: Each line contains a mapping of protocol numbers to protocol codes, separated by a comma.
    - Source (https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml).
    - Example:
        ```
        6,tcp  
        17,udp  
        ```

#### Output Details
1. File Name: ```output.txt```
2. Location: Generated under the data/ folder after running FlowLogParser.py.
3. Format:
    - Section 1: Tag Counts
        ```
        Tag Counts:  
        Tag,Count  
        tag1,count  
        tag2,count  
        ... 
        Untagged,count  
        ```
        - Tags are ordered based on their first occurrence in the flow logs' port/protocol combinations.
        - The "Untagged" tag always appears last.
    - Section 2: Port/Protocol Combination Counts
        ```
        Port/Protocol Combination Counts:  
        Port,Protocol,Count  
        port1,protocol1,count  
        port1,protocol2,count  
        ...  
        ```
        - Port/protocol combinations are listed in the order they first appear in the flow logs.

#### Additional Assumptions
1. The given flow_log and lookup_table have been used in the code, but the given output is only considered as a reference and not considered as the actual output corresponding to the given flow logs and lookup table
2. Input flow logs are always in Version 2 format, with values aligning with the specified columns.
3. If a protocol number in the flow logs does not have a corresponding entry in number_ip_map.txt, its protocol code is considered an empty string and will appear as such in the output under "Port/Protocol Combination Counts." (This scenario is tested in test_case_2.)
4. Case Insensitivity:
    - All tags and protocols in the output are converted to lowercase for consistency.
    - During test assertions, comparisons are case-insensitive, even if the expected output includes capitalized tags.

### Testing
1. I have developed 2 test cases under tests/ with lookup_table_test_<number>.csv, flow_logs_test_<number>.txt and expected_output_<number>.txt. The test_actual_output_<number>.txt will be generated on running test.py, and it will be compared against the expected output.
2. To run test.py, from the root directory FlowLogParser, run the command
```
python3 -m tests.test
```