import csv
import sys
import random
from collections import defaultdict, Counter

import pandas as pd

def sample_and_combine_csv(file, output_file, x_benign, y_benign, z_attack):
    headers = read_headers(file)
    flow_id_to_rows_map = defaultdict(list)

    with open(file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            flow_id_to_rows_map[row['Flow ID']].append(row)

    benign_flows = {fid: rows for fid, rows in flow_id_to_rows_map.items() if rows[0]['Label'] == 'BENIGN'}
    attack_flows = {fid: rows for fid, rows in flow_id_to_rows_map.items() if rows[0]['Label'] == 'ATTACK'}

    initial_benign_flows = list(benign_flows.values())[:x_benign]

    for flow in initial_benign_flows:
        del benign_flows[flow[0]['Flow ID']]

    sampled_additional_benign = random.sample(list(benign_flows.values()), min(y_benign, len(benign_flows)))
    sampled_attack = random.sample(list(attack_flows.values()), min(z_attack, len(attack_flows)))

    additional_flows = sampled_additional_benign + sampled_attack
    random.shuffle(additional_flows)

    combined_flows = initial_benign_flows + additional_flows
    with open(output_file, 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=headers)
        writer.writeheader()
        for flow in combined_flows:
            writer.writerows(flow)

    packet_counts = Counter({'x': sum(len(flow) for flow in initial_benign_flows),
                             'y': sum(len(flow) for flow in sampled_additional_benign),
                             'z': sum(len(flow) for flow in sampled_attack)})
    
    print(f"Packet counts - x BENIGN: {packet_counts['x']}, y BENIGN: {packet_counts['y']}, z ATTACK: {packet_counts['z']}")

def read_headers(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
    return headers

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: script.py <input_file> <output_file> <x_benign> <y_benign> <z_attack>")
        sys.exit(1)

    file = sys.argv[1]
    output_file = sys.argv[2]
    x_benign = int(sys.argv[3])
    y_benign = int(sys.argv[4])
    z_attack = int(sys.argv[5])

    sample_and_combine_csv(file, output_file, x_benign, y_benign, z_attack)
