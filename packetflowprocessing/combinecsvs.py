import csv

def read_headers(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        headers = next(reader)
    return headers

def combine_tsvs(start, end, output_file):
    first_file = f"{start}.pcap.tsv"
    original_headers = read_headers(first_file)
    
    output_headers = list(original_headers)
    if 'sll.src.eth' in output_headers:
        output_headers.remove('sll.src.eth')
    if 'eth.src' not in output_headers:
        output_headers.append('eth.src')

    with open(output_file, 'w', newline='') as out_file:
        writer = csv.writer(out_file, delimiter='\t')
        writer.writerow(output_headers)

        for i in range(start, end + 1):
            current_file = f"{i}.pcap.tsv"
            current_headers = read_headers(current_file)
            if set(current_headers) != set(original_headers):
                print(f"Warning: Headers in {current_file} do not match the original headers. Skipping file.")
                continue

            with open(current_file, 'r') as file:
                reader = csv.DictReader(file, delimiter='\t')

                for row in reader:
                    # Transfer sll.src.eth to eth.src and remove sll.src.eth
                    if 'sll.src.eth' in row:
                        row['eth.src'] = row['sll.src.eth']
                        del row['sll.src.eth']

                    writer.writerow([row[key] for key in output_headers])

        print(f"Combined TSV written to {output_file}")

start, end = 1, 27
output_file = 'UNSWFull.tsv'
combine_tsvs(start, end, output_file)
