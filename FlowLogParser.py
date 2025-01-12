import csv
import os
from collections import Counter, defaultdict

# Constants for file names
FLOW_LOG_FILE = "data/flow_logs.txt"
LOOKUP_TABLE_FILE = "data/lookup_table.csv"
NUMBER_IP_MAP = "data/number_ip_map.txt"
OUTPUT_FILE = "data/output.txt"

def load_ip_numbers_to_hashmap(file_path):
    number_ip_map = {}
    with open(file_path, mode='r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                number_id = parts[0].strip()
                protocol_code = parts[1].strip()
                if protocol_code:  # Add to map only if protocol code is non-empty
                    number_ip_map[number_id] = protocol_code
    return number_ip_map

# Function to load the lookup table
def load_lookup_table(file_path):
    lookup_table = {}
    with open(file_path, mode='r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 3:
                dstport = parts[0].strip()
                protocol = parts[1].strip().lower()
                tag = parts[2].strip()
                lookup_table[(dstport, protocol)] = tag
    return lookup_table

# Function to parse the flow log file
def parse_flow_logs(file_path):
    logs = []
    with open(file_path, mode='r') as file:
        for line in file:
            fields = line.split()
            if len(fields) >= 12:
                dstport = fields[6]
                protocol = fields[7]
                logs.append((dstport, protocol))
    return logs

# Function to map logs to tags and calculate count
def map_logs_to_tags(logs, lookup_table, number_ip_mapping):
    tag_counter = Counter()
    port_protocol_counter = Counter()
    untagged_count = 0

    for dstport, protocol_num in logs:
        protocol = number_ip_mapping.get(protocol_num, "").lower()
        key = (dstport, protocol)
        if key in lookup_table:
            tag = lookup_table[key]
            tag_counter[tag] += 1
        else:
            untagged_count += 1
        port_protocol_counter[key] += 1
    return tag_counter, port_protocol_counter, untagged_count

# Function to write output to file
def write_output(tag_counter, port_protocol_counter, untagged_count, output_file):
    with open(output_file, mode='w') as file:
        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")
        for tag, count in tag_counter.items():
            file.write(f"{tag},{count}\n")
        file.write(f"Untagged,{untagged_count}\n\n")

        file.write("Port/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counter.items():
            file.write(f"{port},{protocol},{count}\n")

# Main function
def main():
    if not os.path.exists(FLOW_LOG_FILE):
        print(f"Error: Flow log file '{FLOW_LOG_FILE}' not found.")
        return

    if not os.path.exists(LOOKUP_TABLE_FILE):
        print(f"Error: Lookup table file '{LOOKUP_TABLE_FILE}' not found.")
        return

    lookup_table = load_lookup_table(LOOKUP_TABLE_FILE)
    logs = parse_flow_logs(FLOW_LOG_FILE)
    number_ip_mapping = load_ip_numbers_to_hashmap(NUMBER_IP_MAP)
    tag_counter, port_protocol_counter, untagged_count = map_logs_to_tags(logs, lookup_table, number_ip_mapping)
    write_output(tag_counter, port_protocol_counter, untagged_count, OUTPUT_FILE)
    print(f"Output written to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
