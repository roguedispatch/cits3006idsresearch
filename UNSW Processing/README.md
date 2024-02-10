# Datasets for UNSW
https://research.unsw.edu.au/projects/unsw-nb15-dataset

NOTE: The host for the above dataset is down. The processed dataset has been included in the Folder ./PCAP Processing/UNSWFirstFive.zip instead

# Run commands

## Setting up pcaps

Add all pcaps to folder ./PCAP Processing (we used the first 5 pcap files in the UNSW dataset) and run the following commands to:
- Convert the pcap files to tsv files
- Combine the tsv files into a single file

Ensure the Wireshark path is updated in converttotsv.py

`python3 converttotsv.py`
`python3 combinecsvsnew.py`

Add labelled flow files from UNSW to ./Final Processing & Combining and ensure combineflows.py file paths are correcy

`python3 combineflows.py`

## Label combined pcaps with flow data

For use in packet-based IDS Systems, the packets are labelled with the flow data. This is done by matching the flow data with the packets and adding the label to the packet data

labeler.py takes up to 5 arguments: the flow file, the packet file, the output file, the progress print interval and the (optional) number of packets to process. The flow file is labeled file that can be acquired from the source above. The packet file is the output of the pcap extractor. The number of packets to process is used to limit the size of the output file. The output file is a csv file with the packet data and the flow labels combined.

`python3 labeler.py <flow file> <packet file> <output file> <progress print interval> <number of packets to process>`