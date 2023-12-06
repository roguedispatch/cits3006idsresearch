import csv
import sys
import random
from collections import defaultdict

def read_headers(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
    return headers

def sample_by_packet_count(flow_map, desired_packet_count):
    """Sample rows such that the combined length is as close as possible to desired_packet_count, 
    but can exceed if the next flow pushes it over, while keeping entire flows."""
    sampled_rows = []
    flows = list(flow_map.keys())
    random.shuffle(flows)
    
    for flow in flows:
        if len(sampled_rows) + len(flow_map[flow]) <= desired_packet_count:
            sampled_rows.extend(flow_map[flow])
        else:
            break
    
    return sampled_rows

def combine_and_sample_csvs(file1, file2, output_file, sample_size_file1, sample_size_file2, attack_percentage):
    headers1 = read_headers(file1)
    headers2 = read_headers(file2)

    if headers1 == headers2:
        flow_id_to_rows_map = defaultdict(list)

        # Read rows from the first file
        with open(file1, 'r') as f1:
            reader1 = csv.DictReader(f1)
            for row in reader1:
                row['Source File'] = file1
                flow_id_to_rows_map[row['Flow ID']].append(row)

        # Read rows from the second file
        with open(file2, 'r') as f2:
            reader2 = csv.DictReader(f2)
            for row in reader2:
                row['Source File'] = file2
                flow_id_to_rows_map[row['Flow ID']].append(row)

        # Separate the flow IDs based on criteria
        flow_ids_file1 = {fid: rows for fid, rows in flow_id_to_rows_map.items() if rows[0]['Source File'] == file1}
        flow_ids_file2_benign = {fid: rows for fid, rows in flow_id_to_rows_map.items() if rows[0]['Source File'] == file2 and rows[0]['Label'] == 'BENIGN'}
        flow_ids_file2_attack = {fid: rows for fid, rows in flow_id_to_rows_map.items() if rows[0]['Source File'] == file2 and rows[0]['Label'] == 'ATTACK'}

        # Sample rows based on desired packet count
        sampled_rows_file1 = sample_by_packet_count(flow_ids_file1, sample_size_file1)
        
        num_attack_samples = int(sample_size_file2 * attack_percentage / 100)
        sampled_rows_file2_attack = sample_by_packet_count(flow_ids_file2_attack, num_attack_samples)
        
        num_benign_samples = sample_size_file2 - len(sampled_rows_file2_attack)
        sampled_rows_file2_benign = sample_by_packet_count(flow_ids_file2_benign, num_benign_samples)

        # Consolidate sampled rows with file1 entries first
        sampled_rows = sampled_rows_file1 + sampled_rows_file2_benign + sampled_rows_file2_attack

        # Write to the output file
        with open(output_file, 'w', newline='') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=headers1 + ['Source File'])
            writer.writeheader()
            writer.writerows(sampled_rows)

        print(f"Combined CSV written to {output_file}")

    else:
        set1, set2 = set(headers1), set(headers2)
        common = set1.intersection(set2)
        only_in_file1 = set1 - common
        only_in_file2 = set2 - common

        if only_in_file1:
            print(f"Headers only in {file1}: {', '.join(only_in_file1)}")
        if only_in_file2:
            print(f"Headers only in {file2}: {', '.join(only_in_file2)}")

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: script.py <file1> <file2> <output_file> <sample_size_file1> <sample_size_file2> <attack_percentage>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]
    sample_size_file1 = int(sys.argv[4])
    sample_size_file2 = int(sys.argv[5])
    attack_percentage = float(sys.argv[6])

    combine_and_sample_csvs(file1, file2, output_file, sample_size_file1, sample_size_file2, attack_percentage)