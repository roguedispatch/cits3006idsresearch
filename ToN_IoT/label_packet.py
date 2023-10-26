import copy
import csv
import sys
from collections import defaultdict
import os
import datetime

def collapse_flows(filename):
    collapsed = defaultdict(list)

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = [header.strip() for header in next(reader)]
        
        for row in reader:
            # Extract key data: 5-tuple, start time, end time
            key = tuple(row[headers.index(i)] for i in ["src_ip", "src_port", "dst_ip", "dst_port", "proto", "ts", "duration"])
            
            # Find existing record or create new one
            existing = None
            for rec in collapsed[key]:
                if rec["start_time"] == row[headers.index("ts")] and rec["end_time"] == (float(row[headers.index("ts")]) + float(row[headers.index("duration")])):
                    existing = rec
                    break
            
            if existing:
                # Update existing record if label is not BENIGN
                if row[headers.index("label")] != '0':
                    existing["label"] = 'ATTACK'
                    existing["type"] = row[headers.index("type")]
            else:
                # Add new record
                collapsed[key].append({
                    "start_time": row[headers.index("ts")],
                    "end_time": float(row[headers.index("ts")]) + float(row[headers.index("duration")]),
                    "label": 'ATTACK' if row[headers.index("label")] != '0' else 'BENIGN',
                    "type": row[headers.index("type")]
                })

    new_filename = filename.split(".")[0] + "_collapsed.csv"

    with open(new_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        headers = ['Source IP', 'Source Port', 'Destination IP', 'Destination Port', 'Protocol', 'Start Time', 'End Time', 'Label', 'Attack Category']
        writer.writerow(headers)
        
        for key, entries in collapsed.items():
            for entry in entries:
                new_row = list(key[:-2]) + [entry["start_time"], entry["end_time"], entry["label"], entry["type"]]
                writer.writerow(new_row)

    return new_filename

def flow_tuple_to_string(flow_tuple):
    """Convert a flow tuple to the string format."""
    return f"{flow_tuple[0]}-{flow_tuple[2]}-{flow_tuple[1]}-{flow_tuple[3]}"

def delete_file_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)

def get_flow_tuple_for_matching(row):
    """Get flow tuple based on the provided row."""
    src_ip = row.get('ip.src', '0.0.0.0')
    dst_ip = row.get('ip.dst', '0.0.0.0')
    src_port, dst_port = '0', '0'
    proto = row.get('protocol', 'unknown')
    
    # OSPF (for debugging)
    #if proto == 'ospf':
    #    print(f"Before OSPF adjustments: {src_ip}, {dst_ip}, {src_port}, {dst_port}, {proto}")
    
    # TCP
    if proto == 'tcp':
        src_port, dst_port = row['tcp.srcport'], row['tcp.dstport']
    
    # UDP
    elif proto == 'udp':
        src_port, dst_port = row['udp.srcport'], row['udp.dstport']
    
    # ICMP
    elif proto == 'icmp':
        pass
    
    # ARP
    elif proto == 'arp':
        src_ip, dst_ip = row['arp.src.proto_ipv4'], row['arp.dst.proto_ipv4']
    
    # IPv6
    elif 'ipv6.src' in row and 'ipv6.dst' in row:
        src_ip, dst_ip = row.get('ipv6.src', src_ip), row.get('ipv6.dst', dst_ip)
        if 'udp.srcport' in row and 'udp.dstport' in row:
            src_port, dst_port = row['udp.srcport'], row['udp.dstport']

    #if proto == 'ospf':
    #    print(f"After OSPF adjustments: {src_ip}, {dst_ip}, {src_port}, {dst_port}, {proto}")

    flow_forward = (src_ip, src_port, dst_ip, dst_port, proto)
    flow_backward = (dst_ip, dst_port, src_ip, src_port, proto)

    #print(f"Flow data: {flow_forward}, {flow_backward}")
    
    return flow_forward, flow_backward

def process_files(packet_file, flow_file, output_file, print_interval, max_lines):
    flows = {}
    
    with open(flow_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            try:
                flow_tuple = (row['Source IP'], row['Source Port'], row['Destination IP'], row['Destination Port'], row['Protocol'])
                label = 'ATTACK' if row['Label'] != 'BENIGN' else 'BENIGN'
                start_time = float(row['Start Time'])
                end_time = float(row['End Time'])
                category = row['Attack Category']

                if flow_tuple not in flows:
                    flows[flow_tuple] = []
                flows[flow_tuple].append((start_time, end_time, label, category))
            except ValueError as ve:
                print(f"Error parsing line: {row}")
                print(f"Error message: {ve}")
                continue

    delete_file_if_exists(output_file)

    with open(packet_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='\t')
        print(reader.fieldnames)
        fieldnames = reader.fieldnames
        fieldnames.extend(['Label', 'Attack Category', 'Flow ID'])

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for idx, row in enumerate(reader, 1):
            if max_lines and idx > max_lines:
                break

            working_row = copy.deepcopy(row)
            flow_forward, flow_backward = get_flow_tuple_for_matching(working_row)
            packet_time = float(working_row['frame.time_epoch'])

            def find_flow_data(flow_key):
                for time_start, time_end, label, category in flows.get(flow_key, []):
                    if time_start <= int(round(packet_time, 0)) <= time_end:
                        return label, category, time_start
                return 'unknown', 'unknown', 'unknown'

            # Check both forward and backward flows
            label, category, time_start = find_flow_data(flow_forward)
            if label == 'unknown':
                label, category, time_start = find_flow_data(flow_backward)

            row['Label'] = label
            row['Attack Category'] = category
            # Flow ID should be the flow tuple to string + the start time of the flow
            row['Flow ID'] = flow_tuple_to_string(flow_forward) + "-" + str(time_start)

            #if row['protocol'] == 'arp':
            #    print(f"Row data: {row}")
            
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
    delete_file_if_exists(output_file)
    collapsed_flow_filename = flow_file.split(".")[0] + "_collapsed.csv"
    if not os.path.exists(collapsed_flow_filename):
        collapsed_flow_file = collapse_flows(flow_file)
    else:
        collapsed_flow_file = collapsed_flow_filename

    process_files(packet_file, collapsed_flow_file, output_file, print_interval, max_lines)