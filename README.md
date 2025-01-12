# Flow Log Parser

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

### Assumptions:
1. User will upload the flow logs in a text file with the name "flow_logs.txt" under the data/ folder
2. User will upload the lookup table as a csv file with the name "lookup_table.csv" under the data/ folder
3. Every flow log is in a new line in the flow_logs.txt file. There are no empty lines in between
4. One flow log has multiple space separated values. 
5. The column names corresponding to the flow log space separated values are inferred from the https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html for version 2 logs. The column names are - version,account-id,interface-id,srcaddr,dstaddr,srcport,dstport,protocol,packets,bytes,start,end,action,log-status
6. File "number_ip_map.txt" under the data/ folder was created to map the protocol numbers to the internet protocol codes according to https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
7. The first line of the lookup_table input has comma sparated column names
8. All the other lines in the lookup_table are comma separated values for the respective columns (dstport, protocol and tag)
9. The given flow_log and lookup_table have been used in the code, but the given output is only considered as a reference and not considered as the actual output corresponding to the given flow logs and lookup table
10. The output.txt file will be generated under the data/ folder when FlowLogParser.py is run. The first line will contain the title "Tag Counts:" followed by 1 line of column names (Tag, Count), and then several lines of tag, column corresponding to the given input flow_logs and lookup table. The there will be an empty line, followed by the title "Port/Protocol Combination Counts:", the column names (Port,Protocol,Count) followed by several lines mentioning the count of a particular (port,protocol) combination in the prvided flow logs
11. In the output, Port/Protocol Combination Counts show up in the order they are first seen in the flow logs
12. In the output, in Tag Counts, the tags are ordered in the order they are first seen in the Port/Protocol Combination, except for the "Untagged" tag, which always appears last
13. It is expected that input flow logs are always version 2, and the values align with the column list - version,account-id,interface-id,srcaddr,dstaddr,srcport,dstport,protocol,packets,bytes,start,end,action,log-status
14. If number in the flow_logs protocol column doesn't have a corresponding protocol code mentioned in the number_ip_mapping.txt key-value pairs, protocol code is considered an empty string, and will show up as such in the output (in Port/Protocol Combination Counts) - this case has been tested in test_case_2

#### output.txt Format:
```
Tag Counts:
Tag,Count
tag1,count
tag2,count
.
.
.

Port/Protocol Combination Counts:
Port,Protocol,Count
port1,protocol1,count
port1,protocol2,count
port2,protocol1,count
.
.
.
```

### Testing
1. I have developed 2 test cases under tests/ with lookup_table_test_<number>.csv, flow_logs_test_<number>.txt and expected_output_<number>.txt. The test_actual_output_<number>.txt will be generated on running test.py, and it will be compared against the expected output.
2. To run test.py, from the root directory FlowLogParser, run the command
```
python3 -m tests.test
```