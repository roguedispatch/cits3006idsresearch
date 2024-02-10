# Datasets for CICIDS2017
http://205.174.165.80/CICDataset/CIC-IDS-2017/

# Run commands

## Setting up pcaps

Add pcaps to folder ./CICIDS2017 Processing and update extractorforkitsune.py file with Wireshark path

For our research, the full Thursday pcap was used. Because HELAD is based on Kitsune, the pcap files are processed with this script for both IDS systems. This script simply uses wireshark to extract relevant features from the pcap files and saves them to a csv file.

`python3 extractorforkitsune.py -i <input pcap> -o <output csv>`

Combine all those pcap csvs - the combinecsvs.py has hardcoded file paths, so these should be updated within the script

`python3 combine_csvs.py `

## Setting up flows and labelling packets with flow data

packetlabeler.py takes up to 5 arguments: the flow file, the packet file, the output file, the progress print interval and the (optional) number of packets to process. The flow file is labeled file that can be acquired from the source above. The packet file is the output of the pcap extractor. The number of packets to process is used to limit the size of the output file. The output file is a csv file with the packet data and the flow labels combined.

`python3 packetlabeler.py <flow file> <packet file> <output file> <progress print interval> <number of packets to process>`