# Stratosphere Linux IPS (SLIPS) Setup
https://github.com/stratosphereips/StratosphereLinuxIPS/tree/6bf631f3c5c9ec73361f8b78148a397e8f4df0be
## Test Bench Specifications
- Intel i5 13600KF
- Nvidia RTX 3070
- 32GB Memory
- Windows 11
- SLIPS version 1.0.8 (November 15, 2023)
## Prerequisites
The easiest way to run SLIPS is via a Docker container. The Docker engine and command line interface are the only prerequisites - no other dependicies are required. Docker software can be found here: https://docs.docker.com/get-docker/
## Installation 
Download and run the docker container:

```docker run -it -d --name slips stratosphereips/slips:1.0.8```
## Running the Code
1. Move the required datasets from the host machine to the container: ```docker cp <target_dataset_directory>/<dataset> <container_id>:<datasets_directory>
2. Run SlIPS in daemonsied mode: ```./slips.py -c config/slips.conf -f <datasets_directory>/<dataset>```
> [!NOTE]
> Various traffic capture formats may be used including raw pcaps and zeek conn.log files.
## Obtaining Results
One of SLIPS' outputs is an SQLite table of flows. These flows can be compared to the original network capture by matching up source and destination information and timestamps among other data. This process can be automated with a simple script.

An example of such a script can be found in the Jupyter notebook "Stratosphere.ipynb."

All other assets used can be found here: https://uniwa-my.sharepoint.com/:f:/g/personal/23072152_student_uwa_edu_au/EukIC8Y4JLFHs2DDBXvr3JMBmE0VcN6Rputgkk3Qtx0bfw?e=h9odfd

