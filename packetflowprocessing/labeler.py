import copy
import csv
import sys
from collections import defaultdict
import os
import datetime

def collapse_flows(filename):
    collapsed = defaultdict(lambda: {"start_time": float('inf'), "end_time": -float('inf'), "label": "BENIGN", "attack_cat": "None"})

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = [header.strip() for header in next(reader)]
        for row in reader:
            # Extract start time and duration
            timestamp_epoch = float(row[headers.index("Stime")])
            duration = float(row[headers.index("dur")])
            end_time = timestamp_epoch + duration

            # Based on the 5-tuple (Source IP, Source Port, Destination IP, Destination Port, Protocol)
            key = tuple(row[headers.index(i)] for i in ["srcip", "sport", "dstip", "dsport", "proto"])
            if timestamp_epoch < collapsed[key]["start_time"]:
                collapsed[key]["start_time"] = timestamp_epoch
            if end_time > collapsed[key]["end_time"]:
                collapsed[key]["end_time"] = end_time
            if row[headers.index("Label")] != '0':
                collapsed[key]["label"] = 'ATTACK'
                collapsed[key]["attack_cat"] = row[headers.index("attack_cat")]

    new_filename = filename.split(".")[0] + "_collapsed.csv"

    with open(new_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Source IP', 'Source Port', 'Destination IP', 'Destination Port', 'Protocol', 'Start Time', 'End Time', 'Label', 'Attack Category'])
        for key, data in collapsed.items():
            new_row = list(key) + [data["start_time"], data["end_time"], data["label"], data["attack_cat"]]
            writer.writerow(new_row)
    return new_filename

def flow_tuple_to_string(flow_tuple):
    """Convert a flow tuple to the string format."""
    return f"{flow_tuple[0]}-{flow_tuple[2]}-{flow_tuple[1]}-{flow_tuple[3]}"

def delete_file_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)

def get_flow_tuple_for_matching(row):
    src_ip, dst_ip = row.get('ip.src', '0.0.0.0'), row.get('ip.dst', '0.0.0.0')
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
        proto = 'icmp'
    
    # ARP
    elif row['arp.opcode']:
        proto = 'arp'
        src_ip, dst_ip = row['arp.src.proto_ipv4'], row['arp.dst.proto_ipv4']
    
    # IPv6
    elif row['ipv6.src'] and row['ipv6.dst']:
        src_ip, dst_ip = row['ipv6.src'], row['ipv6.dst']
        if row['udp.srcport'] and row['udp.dstport']:
            src_port, dst_port = row['udp.srcport'], row['udp.dstport']
            proto = 'udp/ipv6'
        else:
            proto = 'ipv6'

    timestamp = row['frame.time_epoch']

    flow_forward = (src_ip, src_port, dst_ip, dst_port)
    flow_backward = (dst_ip, dst_port, src_ip, src_port)
    
    return flow_forward, flow_backward, proto

def process_files(packet_file, flow_file, output_file, print_interval, max_lines):
    flows = {}
    
    with open(flow_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            try:
                flow_tuple = (row['Source IP'], row['Source Port'], row['Destination IP'], row['Destination Port'])
                label = 'ATTACK' if row['Label'] != 'BENIGN' else 'BENIGN'
                start_time = float(row['Start Time'])
                end_time = round(float(row['End Time']),0)
                category = row['Attack Category']
                flows[flow_tuple] = (label, start_time, end_time, category, row['Protocol'])
            except ValueError as ve:
                print(f"Error parsing line: {row}")
                print(f"Error message: {ve}")
                continue

    delete_file_if_exists(output_file)

    with open(packet_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='\t')
        fieldnames = reader.fieldnames
        fieldnames.extend(['Label', 'Attack Category', 'old_protocol', 'proto'])

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for idx, row in enumerate(reader, 1):
            if max_lines and idx > max_lines:
                break

            working_row = copy.deepcopy(row)

            flow_forward, flow_backward, proto = get_flow_tuple_for_matching(working_row)
            
            #print(f"Flow forward: {flow_forward}, Flow backward: {flow_backward}, proto: {proto}")

            flow_data = flows.get(flow_forward, flows.get(flow_backward, ('unknown', None, None, 'unknown', 'unknown')))
            packet_time = float(working_row['frame.time_epoch'])
            
            #print(f"Flow data: {flow_data}, packet time: {round(packet_time,0)}")

            if flow_data[1] is not None and flow_data[2] is not None and flow_data[1] <= round(packet_time,0) <= flow_data[2]:
                row['Label'] = flow_data[0]
                row['Attack Category'] = flow_data[3]
                row['old_protocol'] = proto # Modify this to whatever field name holds the protocol info in the packet file
                row['proto'] = flow_data[4] # new protocol
            else:
                row['Label'] = 'unknown'
                row['Attack Category'] = 'unknown'
                row['old_protocol'] = proto
                row['proto'] = 'unknown'

            writer.writerow(row)

            if idx % print_interval == 0:
                print(f"Processed {idx} lines")

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
    
    collapsed_flow_filename = flow_file.split(".")[0] + "_collapsed.csv"
    if not os.path.exists(collapsed_flow_filename):
        collapsed_flow_file = collapse_flows(flow_file)
    else:
        collapsed_flow_file = collapsed_flow_filename

    process_files(packet_file, collapsed_flow_file, output_file, print_interval, max_lines)