# Run commands

## Setting up pcaps
Copied normal1,2->testing1,2 and normal_scanning1,2->testing3,4
Add all pcaps and alter pcap_to_tsv file

`python3 pcap_to_tsv.py`

Combine all those pcaps 

`python3 join_pcaps.py`

## Setting up flows 

Add all flows and alter join_flows_files

`python3 join_flow_files.py`

## Label combined pcaps with flow data 

`python3 label_packet.py ToNTest4.tsv Flows/CombinedFlows.csv ToNAllLabelled.csv 100000`

python3 sample_packets