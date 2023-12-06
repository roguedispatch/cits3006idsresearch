import csv
import sys

# Ensure a filename is provided
if len(sys.argv) < 2:
    print("Usage: python script_name.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

# Read the TSV data
with open(filename, 'r') as file:
    reader = csv.DictReader(file, delimiter='\t')
    data = list(reader)

# Create a dictionary to store mappings
ip_to_mac = {}

# Iterate through the rows of the dataset
for row in data:
    src_ip = row['ip.src']
    src_mac = row['sll.src.eth']
    
    # Store the source IP to MAC mapping
    ip_to_mac[src_ip] = src_mac

    # If destination IP has been seen as a source before, use its MAC
    if row['ip.dst'] in ip_to_mac:
        row['eth.dst'] = ip_to_mac[row['ip.dst']]
    else:
        row['eth.dst'] = None  # We don't have the MAC for this IP yet

# Print the results
for row in data:
    print(row['ip.src'], row['ip.dst'], row['sll.src.eth'], row.get('eth.dst', 'Unknown'))
