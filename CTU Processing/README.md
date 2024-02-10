# Datasets for CTU-13
https://www.stratosphereips.org/datasets-iot23

The packet and labelled log files are required for processing

# Run commands

## Setting up pcaps

Add pcaps to folder ./CTU Processing and update extractor.py file with Wireshark path

`python3 extractor.py`

## Sampling and labelling packets

Update the files paths in sample.py for the combined packet csv, the output file and the Zeek conn.log file, this script will parse the log file and add the labels to the packet csv

`python3 sample.py`