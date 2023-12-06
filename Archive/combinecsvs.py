import csv

def read_headers(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
    return headers

def combine_csvs(file1, file2, output_file):
    headers1 = read_headers(file1)
    headers2 = read_headers(file2)

    if headers1 == headers2:
        with open(output_file, 'w', newline='') as out_file:
            writer = csv.writer(out_file)

            writer.writerow(headers1)

            with open(file1, 'r') as f1:
                reader1 = csv.reader(f1)
                next(reader1) 
                writer.writerows(reader1)

            with open(file2, 'r') as f2:
                reader2 = csv.reader(f2)
                next(reader2) 
                writer.writerows(reader2)

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

file1 = 'Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv'
file2 = 'Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv'
output_file = 'Thursday-WorkingHours-Full.csv'
combine_csvs(file1, file2, output_file)