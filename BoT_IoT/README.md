# Datasets for BoT-IoT
https://research.unsw.edu.au/projects/bot-iot-dataset

# Run commands

## Setting up pcaps

Add all pcaps to folder ./BoT_IoT/Raw and update pcap_to_tsv file with file paths and Wireshark path

`python3 pcap_to_tsv.py`

Combine all those pcaps 

`python3 join_pcap_tsvs.py`

## Setting up flows 

Add labelled flow files from UNSW to ./Bot_IoT/Flows and update join_flows_files with file paths

`python3 join_flow_files.py`

## Label combined pcaps with flow data

For use in packet-based IDS Systems, the packets are labelled with the flow data. This is done by matching the flow data with the packets and adding the label to the packet data

`python3 label_packet.py FourDDoS.tsv Flows/CombinedFlows.csv FinalOutput.csv 100000`