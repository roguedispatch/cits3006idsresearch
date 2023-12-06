import copy
import csv
import sys
from collections import defaultdict
import os

PROTOCOL_MAP = {
    'tcp': '6',
    'udp': '17',
    'other': '0'
}

def delete_file_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)

def collapse_flows(filename):
    collapsed = defaultdict(list)
    
    # Reading the CSV file
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Extracting headers
        for row in reader:
            # Using Flow ID and Timestamp as a key for collapsing
            key = (row[0], row[6])
            if not collapsed[key]:
                collapsed[key] = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[-1]]
            else:
                # If any row with this key has a label other than 'BENIGN', label it 'ATTACK'
                if row[-1] != 'BENIGN':
                    collapsed[key][-1] = 'ATTACK'
    
    # Create the new filename with "_collapsed" suffix
    new_filename = filename.split(".")[0] + "_collapsed.csv"
    # Delete the file if it already exists
    delete_file_if_exists(new_filename)
    
    # Writing the collapsed rows back to the new CSV file
    with open(new_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Flow ID', 'Source IP', 'Source Port', 'Destination IP', 'Destination Port', 'Protocol', 'Timestamp', 'Label'])
        for value in collapsed.values():
            writer.writerow(value)
    return new_filename

def format_flow(src_ip, src_port, dst_ip, dst_port, proto_num):
    # Ensure the IP with the lower value is the source.
    if src_ip < dst_ip or (src_ip == dst_ip and src_port < dst_port):
        return src_ip, src_port, dst_ip, dst_port, proto_num
    return dst_ip, dst_port, src_ip, src_port, proto_num

def get_flow_tuple_for_matching(row):
    if row['tcp.srcport'] and row['tcp.dstport']:
        proto = 'tcp'
        srcport = row['tcp.srcport']
        dstport = row['tcp.dstport']
    elif row['udp.srcport'] and row['udp.dstport']:
        proto = 'udp'
        srcport = row['udp.srcport']
        dstport = row['udp.dstport']
    else:
        # Mark non-TCP/UDP traffic as protocol 0 with 0 as the source and destination port
        proto = 'other'
        srcport = '0'
        dstport = '0'
    
    proto_num = PROTOCOL_MAP.get(proto)
    return format_flow(row['ip.src'], srcport, row['ip.dst'], dstport, proto_num)

def process_files(packet_file, flow_file, output_file, print_interval, max_lines):
    flows = {}
    
    with open(flow_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            flow_tuple = format_flow(row['Source IP'], row['Source Port'], row['Destination IP'], row['Destination Port'], row['Protocol'])
            label = 'ATTACK' if row['Label'] != 'BENIGN' else 'BENIGN'
            flows[flow_tuple] = (row['Flow ID'], label)

    # Delete the output file if it already exists
    delete_file_if_exists(output_file)
    
    with open(packet_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        fieldnames.append('Flow ID')
        fieldnames.append('Label')

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for idx, row in enumerate(reader, 1):
            if max_lines and idx > max_lines:
                break
                
            working_row = copy.deepcopy(row)  # Work on a copy of the row
            
            formatted_flow_tuple = get_flow_tuple_for_matching(working_row)
            
            flow_data = flows.get(formatted_flow_tuple, (None, 'unknown'))
            #print(f"Flow data: {flow_data}")
            row['Flow ID'] = flow_data[0] if flow_data[0] else 'unknown'
            row['Label'] = flow_data[1]

            writer.writerow(row) 

            #writer.writerow(working_row)
            
            if idx % print_interval == 0:
                print(f"Processed {idx} lines")
        
        outfile.flush()

    print("Processing complete.")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: script.py <packet_file> <flow_file> <output_file> <print_interval> [max_lines]")
        sys.exit(1)

    packet_file = sys.argv[1]
    flow_file = sys.argv[2]
    output_file = sys.argv[3]
    print_interval = int(sys.argv[4])
    max_lines = int(sys.argv[5]) if len(sys.argv) > 5 else None

    # Collapse the input flows first
    collapsed_flow_file = collapse_flows(flow_file)

    # Process the packet file using the collapsed flow file
    process_files(packet_file, collapsed_flow_file, output_file, print_interval, max_lines)
