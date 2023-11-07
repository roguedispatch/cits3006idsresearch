import csv


def read_headers(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
    return headers


def is_empty(row):
    return all(cell.strip() == "" for cell in row)


def combine_csv_files(files, output_file):
    # Read headers from all files and ensure they match
    headers_list = [read_headers(file) for file in files]
    headers_set_list = [set(headers) for headers in headers_list]
    common_headers = set.intersection(*headers_set_list)

    if all(headers == headers_list[0] for headers in headers_list):
        with open(output_file, "w", newline="") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(headers_list[0])  # Write the common headers

            for file in files:
                with open(file, "r") as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip the header row
                    for row in reader:
                        if not is_empty(row):
                            writer.writerow(row)

        print(f"Combined CSV written to {output_file}")
    else:
        # For files with headers not matching the common set, print the unique headers
        for i, file in enumerate(files):
            unique_headers = headers_set_list[i] - common_headers
            if unique_headers:
                print(f"Headers only in {file}: {', '.join(unique_headers)}")


if __name__ == "__main__":

    file1 = "datasets/TrafficLabelling/Friday-WorkingHours-Morning.pcap_ISCX.csv"
    file2 = (
        "datasets/TrafficLabelling/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"
    )
    file3 = "datasets/TrafficLabelling/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
    output_file = "Friday-WorkingHours-Full.csv"

    combine_csv_files([file1, file2, file3], output_file)
