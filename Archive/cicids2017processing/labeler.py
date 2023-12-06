import copy
import csv
import sys
from collections import defaultdict
import os
import datetime

PROTOCOL_MAP = {
    'tcp': '6',
    'udp': '17',
    'ICMP': '1',
    'ARP': '0', 
    'IPv6': '41',
    'UDP/IPv6': '17',
    'other': '0'
}

def flow_tuple_to_string(flow_tuple):
    """Convert a flow tuple to the string format."""
    return f"{flow_tuple[0]}-{flow_tuple[2]}-{flow_tuple[1]}-{flow_tuple[3]}-{flow_tuple[4]}"

def timestamp_to_epoch(ts):
    formats = [
        '%d/%m/%Y %H:%M:%S',
        '%d/%m/%Y %H:%M'
    ]
    
    for fmt in formats:
        try:
            dt_obj = datetime.datetime.strptime(ts, fmt)
            millisec = dt_obj.timestamp()
            return millisec
        except ValueError:
            continue
    
    raise ValueError(f"Timestamp {ts} doesn't match any known formats.")

def delete_file_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)

def collapse_flows(filename):
    collapsed = defaultdict(lambda: {"start_time": float('inf'), "end_time": -float('inf'), "label": "BENIGN"})
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = [header.strip() for header in next(reader)]
        for row in reader:
            # Timestamp to epoch
            timestamp_epoch = timestamp_to_epoch(row[6])
            duration = float(row[7])
            end_time = timestamp_epoch + duration

            # Based on the 5-tuple (Flow ID, Source IP, Source Port, Destination IP, Destination Port, Protocol)
            key = tuple(row[:6])
            if timestamp_epoch < collapsed[key]["start_time"]:
                collapsed[key]["start_time"] = timestamp_epoch
            if end_time > collapsed[key]["end_time"]:
                collapsed[key]["end_time"] = end_time
            if row[-1] != 'BENIGN':
                collapsed[key]["label"] = 'ATTACK'
    
    new_filename = filename.split(".")[0] + "_collapsed.csv"
    delete_file_if_exists(new_filename)

    with open(new_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Flow ID', 'Source IP', 'Source Port', 'Destination IP', 'Destination Port', 'Protocol', 'Start Time', 'End Time', 'Label'])
        for key, data in collapsed.items():
            new_row = list(key) + [data["start_time"], data["end_time"], data["label"]]
            writer.writerow(new_row)
    return new_filename

def get_flow_tuple_for_matching(row):
    src_ip, dst_ip = '0.0.0.0', '0.0.0.0'
    src_port, dst_port = '0', '0'
    proto = 'other'
    
    # TCP
    if row['tcp.srcport'] and row['tcp.dstport']:
        proto = 'tcp'
        src_ip, dst_ip = row['ip.src'], row['ip.dst']
        src_port, dst_port = row['tcp.srcport'], row['tcp.dstport']
    
    # UDP
    elif row['udp.srcport'] and row['udp.dstport']:
        proto = 'udp'
        src_ip, dst_ip = row['ip.src'], row['ip.dst']
        src_port, dst_port = row['udp.srcport'], row['udp.dstport']
    
    # ICMP
    elif row['icmp.type'] and row['icmp.code']:
        proto = 'ICMP'
        src_ip, dst_ip = row['ip.src'], row['ip.dst']
        src_port, dst_port = row['icmp.type'], row['icmp.code']
    
    # ARP
    elif row['arp.opcode']:
        proto = 'ARP'
        src_ip, dst_ip = row['arp.src.proto_ipv4'], row['arp.dst.proto_ipv4']
        # Use opcode as both source and destination port for ARP
        src_port, dst_port = row['arp.opcode'], row['arp.opcode']
    
    # IPv6
    elif row['ipv6.src'] and row['ipv6.dst']:
        src_ip, dst_ip = row['ipv6.src'], row['ipv6.dst']
        if row['udp.srcport'] and row['udp.dstport']:
            src_port, dst_port = row['udp.srcport'], row['udp.dstport']
            proto = 'UDP/IPv6'
        else:
            proto = 'IPv6'

    timestamp = row['frame.time_epoch']
    proto_num = PROTOCOL_MAP.get(proto, 0)

    flow_forward = (src_ip, src_port, dst_ip, dst_port, proto_num, timestamp)
    flow_backward = (dst_ip, dst_port, src_ip, src_port, proto_num, timestamp)
    
    return flow_forward, flow_backward

def process_files(packet_file, flow_file, output_file, print_interval, max_lines):
    flows = {}
    
    with open(flow_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            try:
                flow_tuple_string = row['Flow ID']
                label = 'ATTACK' if row['Label'] != 'BENIGN' else 'BENIGN'
                start_time = float(row['Start Time'])
                end_time = float(row['End Time'])
                flows[flow_tuple_string] = (label, start_time, end_time)
            except ValueError as ve:
                print(f"Error parsing line: {row}")
                print(f"Error message: {ve}")
                continue

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
                
            working_row = copy.deepcopy(row) 
            
            formatted_flow_tuple_forward, formatted_flow_tuple_backward = get_flow_tuple_for_matching(working_row)
            packet_time = float(working_row['frame.time_epoch'])

            flow_id_forward = flow_tuple_to_string(formatted_flow_tuple_forward[:-1]) 
            flow_id_backward = flow_tuple_to_string(formatted_flow_tuple_backward[:-1])
            
            flow_data_forward = flows.get(flow_id_forward, ('unknown', None, None))
            flow_data_backward = flows.get(flow_id_backward, ('unknown', None, None))

            # Forward flow time matches
            if flow_data_forward[1] and flow_data_forward[2] and flow_data_forward[1] <= packet_time <= flow_data_forward[2]:
                row['Flow ID'] = flow_id_forward
                row['Label'] = flow_data_forward[0]
            # Backward flow time matches
            elif flow_data_backward[1] and flow_data_backward[2] and flow_data_backward[1] <= packet_time <= flow_data_backward[2]:
                row['Flow ID'] = flow_id_backward
                row['Label'] = flow_data_backward[0]
            # No match found
            else:
                row['Flow ID'] = 'unknown'
                row['Label'] = 'unknown'
            
            '''
            if row['Label'] == 'unknown':
                print(f"Unmatched Packet at line {idx}:")
                print(f"Forward Tuple: {flow_id_forward}")
                print(f"Backward Tuple: {flow_id_backward}")
            '''
            writer.writerow(row) 
            
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

    # Collapse the input flows
    collapsed_flow_file = collapse_flows(flow_file)

    # Process the packet file using the collapsed flow file
    process_files(packet_file, collapsed_flow_file, output_file, print_interval, max_lines)
