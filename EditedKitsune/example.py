from Kitsune import Kitsune
import numpy as np
import time

##############################################################################
# Kitsune a lightweight online network intrusion detection system based on an ensemble of autoencoders (kitNET).
# For more information and citation, please see our NDSS'18 paper: Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection

# This script demonstrates Kitsune's ability to incrementally learn, and detect anomalies in recorded a pcap of the Mirai Malware.
# The demo involves an m-by-n dataset with n=115 dimensions (features), and m=100,000 observations.
# Each observation is a snapshot of the network's state in terms of incremental damped statistics (see the NDSS paper for more details)

#The runtimes presented in the paper, are based on the C++ implimentation (roughly 100x faster than the python implimentation)
###################  Last Tested with Anaconda 3.6.3   #######################

def convert_csv_to_tsv(input_csv, output_tsv):
    """
    Converts a CSV file to TSV.
    Args:
    - input_csv (str): Path to the input CSV file.
    - output_tsv (str): Path to the output TSV file.
    """
    with open(input_csv, 'r') as csv_file, open(output_tsv, 'w') as tsv_file:
        for line in csv_file:
            tsv_file.write(line.replace(',', '\t'))

# Load Mirai pcap (a recording of the Mirai botnet malware being activated)
# The first 70,000 observations are clean...
#print("Unzipping Sample Capture...")
#import zipfile
#with zipfile.ZipFile("mirai.zip","r") as zip_ref:
#    zip_ref.extractall()

# File location
#TODO: Update the paths
input_file = "BoT_100ktrain_Sampled.csv"
converted_file = "BoT_100ktrain_Sampled.tsv"

# Convert CSV to TSV if needed
convert_csv_to_tsv(input_file, converted_file)
path = converted_file  # Update path to point to the TSV file

packet_limit = np.Inf
#49861 From Monday
# KitNET params:
# Update these parameters based on the datasets
maxAE = 10
FMgrace = 25000
ADgrace = 75000

# Build Kitsune
K = Kitsune(path, packet_limit, maxAE, FMgrace, ADgrace)

# Create an output file
#TODO: Update the path
output_file = "output_with_rmse_unsw_sample.tsv"

print("Running Kitsune:")
RMSEs = []
i = 0
start = time.time()

# Open input and output files
with open(path, 'r') as f_input, open(output_file, 'w') as f_output:
    # Write the header to the output file
    header = f_input.readline().strip() + "\tRMSE\n"
    f_output.write(header)
    f_output.flush()  # Flush the file buffer to ensure header is written

    # Process each individual packet
    while True:
        i += 1
        if i % 25000 == 0:
            print(i)

        line = f_input.readline().strip()
        if not line:
            break

        # Split the line into columns
        columns = line.split("\t")

        # Remove the three extra columns before sending to Kitsune
        label = columns.pop(-3)
        attack_category = columns.pop(-2)
        flow_id = columns.pop(-1)
        
        # Process the modified line with Kitsune
        rmse = K.proc_next_packet()

        # Append the RMSE value and the three columns back
        columns.extend([label, attack_category, flow_id, str(rmse)])

        # Write the modified row to the output file
        row_with_rmse = "\t".join(columns) + "\n"
        f_output.write(row_with_rmse)

stop = time.time()
print("Complete. Time elapsed:", str(stop - start))
print("Output written to", output_file)

# Here we demonstrate how one can fit the RMSE scores to a log-normal distribution (useful for finding/setting a cutoff threshold \phi)
from scipy.stats import norm
benignSample = np.log(RMSEs[FMgrace+ADgrace+1:100000])
logProbs = norm.logsf(np.log(RMSEs), np.mean(benignSample), np.std(benignSample))

# plot the RMSE anomaly scores
print("Plotting results")
from matplotlib import pyplot as plt
from matplotlib import cm
plt.figure(figsize=(10,5))
fig = plt.scatter(range(FMgrace+ADgrace+1,len(RMSEs)),RMSEs[FMgrace+ADgrace+1:],s=0.1,c=logProbs[FMgrace+ADgrace+1:],cmap='RdYlGn')
plt.yscale("log")
plt.title("Anomaly Scores from Kitsune's Execution Phase")
plt.ylabel("RMSE (log scaled)")
plt.xlabel("Time elapsed [min]")
figbar=plt.colorbar()
figbar.ax.set_ylabel('Log Probability\n ', rotation=270)
plt.savefig('output.png')
