# Run commands

## Setting up pcaps

Add all pcaps and alter pcap_to_tsv file

`python3 pcap_to_tsv.py`

Combine all those pcaps 

`python3 join_pcap_tsvs.py`

## Setting up flows 

Add all flows and alter join_flows_files

`python3 join_flow_files.py`

## Label combined pcaps with flow data 

`python3 label_packet.py FourDDoS.tsv Flows/CombinedFlows.csv FinalOutput.csv 100000`