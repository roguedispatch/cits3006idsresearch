import csv
import sys
import random
from collections import defaultdict

def read_headers(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
    return headers

def combine_and_sample_csvs(file1, file2, output_file, sample_size_file1, sample_size_file2):
    headers1 = read_headers(file1)
    headers2 = read_headers(file2)

    if headers1 == headers2:
        combined_rows = []
        flow_id_to_rows_map = defaultdict(list)

        # Read rows from the first file
        with open(file1, 'r') as f1:
            reader1 = csv.DictReader(f1)
            for row in reader1:
                row['Source File'] = file1
                combined_rows.append(row)
                flow_id_to_rows_map[row['Flow ID']].append(row)

        # Read rows from the second file
        with open(file2, 'r') as f2:
            reader2 = csv.DictReader(f2)
            for row in reader2:
                row['Source File'] = file2
                combined_rows.append(row)
                flow_id_to_rows_map[row['Flow ID']].append(row)

        # Randomly sample Flow IDs
        flow_ids_file1 = [fid for fid, rows in flow_id_to_rows_map.items() if rows[0]['Source File'] == file1]
        flow_ids_file2 = [fid for fid, rows in flow_id_to_rows_map.items() if rows[0]['Source File'] == file2]

        sampled_flow_ids_file1 = random.sample(flow_ids_file1, sample_size_file1)
        sampled_flow_ids_file2 = random.sample(flow_ids_file2, sample_size_file2)

        sampled_rows = []
        for fid in sampled_flow_ids_file1 + sampled_flow_ids_file2:
            sampled_rows.extend(flow_id_to_rows_map[fid])

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
    if len(sys.argv) < 6:
        print("Usage: script.py <file1> <file2> <output_file> <sample_size_file1> <sample_size_file2>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]
    sample_size_file1 = int(sys.argv[4])
    sample_size_file2 = int(sys.argv[5])

    combine_and_sample_csvs(file1, file2, output_file, sample_size_file1, sample_size_file2)
