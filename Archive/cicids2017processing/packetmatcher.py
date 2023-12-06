import csv
import datetime

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

flows = []
flow_headers = []
packets = []
packet_headers = []

# Read the flows and convert their timestamp to epoch
with open('Thursday-WorkingHoursFlows.csv', 'r') as flowfile:
    reader = csv.reader(flowfile)
    flow_headers = next(reader)
    print("Processing flows...")
    for i, row in enumerate(reader):
        if not any(row): 
            continue

        start_time = timestamp_to_epoch(row[6])
        duration = float(row[7])
        end_time = start_time + duration
        flows.append(row + [start_time, end_time, 0])

        if i % 100000 == 0:
            print(f"Processed {i} flows...")

print("Flow processing complete!")
flow_index = 0
packets = []
packet_num = 1
print("\nProcessing packets...")

with open('Thursday-WorkingHoursFIN.csv', 'r') as packetfile:
    reader = csv.reader(packetfile)
    packet_headers = next(reader)

    for i, row in enumerate(reader):
        packet_time = float(row[0])

        # TCP and UDP
        if row[4] and row[5]:
            src_ip, dst_ip = row[4], row[5]
            if row[6] and row[7]:  # TCP
                src_port, dst_port = row[6], row[7]
                protocol = 'TCP'
            elif row[8] and row[9]:  # UDP
                src_port, dst_port = row[8], row[9]
                protocol = 'UDP'

        # ICMP
        elif row[10] and row[11]:
            src_ip, dst_ip = row[4], row[5]
            src_port, dst_port = row[10], row[11] 
            protocol = 'ICMP'

        # ARP
        elif row[12]:
            src_ip, dst_ip = row[14], row[16]
            protocol = 'ARP'

        # IPv6
        elif row[17] and row[18]:
            src_ip, dst_ip = row[17], row[18]
            if row[8] and row[9]:  # UDP with IPv6
                src_port, dst_port = row[8], row[9]
                protocol = 'UDP/IPv6'
            else:
                protocol = 'IPv6'

        tcp_fin_flag = int(row[19]) if row[19] else 0

        found = False
        while flow_index < len(flows) and flows[flow_index][-3] < packet_time:
            flow_index += 1

        if flow_index < len(flows) and flows[flow_index][-4] <= packet_time <= flows[flow_index][-3]:
            f_src_ip = flows[flow_index][1]
            f_dst_ip = flows[flow_index][3]
            f_src_port = flows[flow_index][2]
            f_dst_port = flows[flow_index][4]

            match_normal = src_ip == f_src_ip and dst_ip == f_dst_ip and src_port == f_src_port and dst_port == f_dst_port
            match_reverse = src_ip == f_dst_ip and dst_ip == f_src_ip and src_port == f_dst_port and dst_port == f_src_port

            if match_normal or match_reverse:
                packets.append(row + [flows[flow_index][0]])
                found = True
                if tcp_fin_flag == 1:
                    flows[flow_index][-1] += 1
                    if flows[flow_index][-1] >= 2: 
                        flow_index += 1

        if not found:
            packets.append(row + ["FLOW_NOT_FOUND"])

        packet_num += 1
        if i % 100000 == 0:
            print(f"Processed {i} packets...")

with open('Thursady-WorkingHoursPackets_Output.csv', 'w', newline='') as packetfile:
    writer = csv.writer(packetfile)
    writer.writerow(packet_headers + ['Flow ID'])
    writer.writerows(packets)

print("\nProcessing complete!")