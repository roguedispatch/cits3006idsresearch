import sys

# Importing helper functions
from cleaner import FlowCleaner
from labeler import collapse_flows, process_files
from extractor import pcap2csv_with_tshark

def main(pcap_file, flow_file, cleaned_flow_output, final_output):
    # Step 1: Convert pcap to csv using tshark
    packet_csv = pcap_file.split(".")[0] + "_packet.csv"
    pcap2csv_with_tshark(pcap_file, packet_csv)

    # Step 2: Clean the flow file
    cleaner = FlowCleaner(flow_file, cleaned_flow_output)
    cleaner.process()

    # Step 3: Collapse the cleaned flows
    collapsed_flow_file = collapse_flows(cleaned_flow_output)

    # Step 4: Label the packets
    process_files(packet_csv, collapsed_flow_file, final_output, print_interval=10000, max_lines=None)

    print("All steps completed successfully!")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: main.py <pcap_file> <flow_file> <cleaned_flow_output> <final_output>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
