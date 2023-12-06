from FeatureExtractor import FE
from Nomalizor import Normalizor
import warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
warnings.filterwarnings("ignore")
import matplotlib 
matplotlib.use("AGG")
from matplotlib import cm
from matplotlib import pyplot as plt
from scipy.stats import norm
import numpy as np
import Cpip
import pandas as pd
import time
import zipfile

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

# File location
input_file = "BoT_100ktrain_Sampled.csv"
converted_file = "BoT_100ktrain_Sampled.tsv"

# Convert CSV to TSV if needed
convert_csv_to_tsv(input_file, converted_file)

# Load the original TSV file into a DataFrame
original_df = pd.read_csv("BoT_100ktrain_Sampled.tsv", sep='\t')

# Feature extraction
fe = FE("BoT_100ktrain_Sampled.tsv")
X_unormalized = fe.feature_extract()

# Normalization
n = Normalizor()
n.fit(X_unormalized)
X = n.normalize(X_unormalized)

# Setting up grace period values
maxAE = 10
total_grace = 100000
FMgrace = total_grace // 10  # 10% for Feature Mapper
ADgrace = 7 * (total_grace // 10)  # 70% for Anomaly Detector
LSTMgrace = total_grace - FMgrace - ADgrace  # Remaining for LSTM

# Initialize CPIP
C = Cpip.CPIP(X.shape[1], FMgrace, ADgrace, LSTMgrace)

print("Running CPIP:")
start = time.time()

# Open a file to write results as they are processed
with open('output_with_scores_bot.tsv', 'w') as file:
    # Write headers
    headers = original_df.columns.tolist() + ['RMScore', 'LTScore']
    file.write('\t'.join(headers) + '\n')
    
    for i in range(X.shape[0]):
        if (i+1) % 10000 == 0:
            print(i+1)
        # Process the normalized data
        rm, lt = C.process(X[i, ])
        
        # Get the original row data
        original_row = original_df.iloc[i].tolist()
        
        # Append RM and LT scores to the original row
        current_row = original_row + [rm, lt]
        
        # Write the row with scores to the file
        file.write('\t'.join(map(str, current_row)) + '\n')

stop = time.time()
print("Complete. Time elapsed: " + str(stop - start))