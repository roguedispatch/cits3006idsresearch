import csv
import sys

def convert_tsv_to_csv(input_file):
    output_file = input_file.replace('.tsv', '.csv')

    # Read TSV file
    with open(input_file, 'r', newline='') as input_csvfile:
        tsv_reader = csv.reader(input_csvfile, delimiter='\t')
        data = list(tsv_reader)

    # Write CSV file
    with open(output_file, 'w', newline='') as output_csvfile:
        csv_writer = csv.writer(output_csvfile)
        csv_writer.writerows(data)

    print(f"Conversion complete. Results saved to {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python csvtotsv.py input_file.tsv")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_tsv_to_csv(input_file)

if __name__ == "__main__":
    main()
