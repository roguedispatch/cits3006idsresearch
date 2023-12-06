import csv

def parse_labeled_log(log_file_path):
    label_mapping = {}
    with open(log_file_path, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) > 20:
                # Pad the timestamp to 9 decimal places, assuming it has 6 originally.
                timestamp, src_ip, detailed_label = parts[0], parts[2], parts[20]
                # Pad the timestamp to 9 decimal places
                standardized_timestamp = '{:.9f}'.format(float(timestamp))
                
                if 'Benign' in detailed_label:
                    label = 'BENIGN'
                elif 'Malicious' in detailed_label:
                    label = 'ATTACK'
                else:
                    continue  # Skip if neither 'Benign' nor 'Malicious' is found
                
                #print(f"Adding label {label} for {src_ip} at {standardized_timestamp}.")
                label_mapping[(standardized_timestamp, src_ip)] = label
    return label_mapping


def add_labels_and_sample_csv(csv_file_path, label_mapping, sample_sizes, output_csv_path):
    rows_written = {key: 0 for key in sample_sizes}
    
    with open(csv_file_path, 'r', newline='') as infile, \
         open(output_csv_path, 'w', newline='') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = next(reader)
        writer.writerow(header + ['label'])

        for row in reader:
            source_file = row[-1]

            # Debugging output
            print(f"Processing row for file: {source_file}")

            label = 'BENIGN'
            if 'malicious' in source_file:
                timestamp, src_ip = row[0], row[4]
                # Pad the timestamp to 9 decimal places
                standardized_timestamp = '{:.9f}'.format(float(timestamp))
                # Use the standardized timestamp for matching
                label = label_mapping.get((standardized_timestamp, src_ip), 'BENIGN')

            # Match on the full file name including extension
            if source_file in sample_sizes:
                if rows_written[source_file] < sample_sizes.get(source_file, float('inf')):
                    writer.writerow(row + [label])
                    rows_written[source_file] += 1
                else:
                    # Debugging output
                    print(f"Sample size reached for {source_file}.")
            else:
                # Debugging output
                print(f"File {source_file} not in sample sizes.")

            if all(rows_written[key] >= sample_sizes.get(key, float('inf')) for key in sample_sizes):
                # Debugging output
                print(f"Sampled all requested rows for each file at row number {reader.line_num}.")
                break

# File paths
conn_log_labeled_path = 'conn.log.labeled' 
combined_csv_path = 'combined_output.csv'
output_csv_path = 'sample_output_with_labels.csv'

# Parse the labeled log file
label_mapping = parse_labeled_log(conn_log_labeled_path)

# Dictionary to store the filenames and the number of rows to sample from each
sample_sizes = {
    'benign-2018-09-21-capture': 250000,
    'benign-2018-10-25-14-06-32-192.168.1.132': 250000,
    'benign-2019-07-03-15-15-47': 100000,
    'benign-2019-07-03-16-41-09-192.168.1.158': 100000,
    'benign-2019-07-04-16-41-10-192.168.1.158': 100000,
    'benign-2019-07-05-16-41-14-192.168.1.158': 100000,
    'benign-2019-07-06-16-41-17-192.168.1.158': 100000,
    'benign-2019-07-07-16-41-19-192.168.1.158': 100000,
    'malicious-2018-07-20-17-31-20-192.168.100.108': 500000
}

# Add labels to the combined_output.csv and sample rows
add_labels_and_sample_csv(combined_csv_path, label_mapping, sample_sizes, output_csv_path)