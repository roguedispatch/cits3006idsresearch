import csv
import json

# Paths to input and output files
input_path = 'flows_csv.csv'
output_path = 'cleaned_flows.csv'

protocols = {
    'tcp': 6,
    'udp': 17,
    'ip': 0
}

# Extract data from the input file
with open(input_path, 'r') as infile:
    reader = csv.DictReader(infile, delimiter=',')
    flows = []
    for row in reader:
        print(row)
        flow_data = json.loads(row['flow'])
        label = row['label']
        flows.append((flow_data, label))

# Write the flow and label information to the CSV
with open(output_path, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    # Write headers
    writer.writerow(['starttime', 'uid', 'saddr', 'sport', 'daddr', 'dport', 'proto', 'dur', 'appproto', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'smac', 'dmac', 'state', 'history', 'type_', 'dir_', 'label'])
    
    for flow, label in flows:
        flow['proto'] = protocols.get(flow['proto'].lower(), flow['proto'])
        writer.writerow([flow['starttime'], flow['uid'], flow['saddr'], flow['sport'], flow['daddr'], flow['dport'], flow['proto'], flow['dur'], flow['appproto'], flow['spkts'], flow['dpkts'], flow['sbytes'], flow['dbytes'], flow['smac'], flow['dmac'], flow['state'], flow['history'], flow['type_'], flow['dir_'], label])