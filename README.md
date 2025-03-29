Benchmarking IDS Systems
Overview
This repository contains the necessary code and datasets for the research paper on benchmarking Intrusion Detection Systems (IDS). It includes various datasets and scripts to process and analyze the performance of different IDS systems.

Datasets
The datasets included in this study are:
    BoT_IoT
    CICIDS2017
    CTU
    Mirari
    UNSW
These datasets are used to evaluate the effectiveness of the IDS systems.

IDS Systems
The IDS systems evaluated in this research are:
    Kitsune
    HELAD
    Stratosphere
    SDN
Modifications were made to Kitsune and HELAD to ensure that they output CSV files with the Root Mean Square Error (RMSE) scores.

File Structure
/Archive: Contains working and older versions of code
/AOC-IDS: Contains the AOC-IDS model with adapted code for accepting other datasets.
/AOC-IDS Processing: Contains our dataset preprocessing code for the AOC-IDS model
/BoT_IoT: Contains the BoT_IoT related processing scripts.
/CICIDS2017: Contains the CICIDS2017 related processing scripts.
/CTU: Contains the CTU related processing scripts.
/EditedHELAD: Contains the HELAD IDS edited to output the RMSE output.
/EditedKitsune: Contains the Kitsune IDS edited to output the RMSE output.
/NEGSC: Contains the NEGSC model with adapted code for accepting other datasets.
/NEGSC Processing: Directs to the /NEGSC/NEGSC.ipynb code for the preprocessing modifications
/ResultsScripts: Contains the scripts used to process the results.
/SDNN_submit: Contains the scripts required for the SDNN IDS
/Straosphere: Contains the BOTIOT assets for Stratosphere.
/UNSW: Contains the UNSW related processing scripts.
/stratosphere_processing.ipynb: Jupyter notebook for processing data for Stratosphere.

## Usage Guide
For each of the folders in the repository, there are specific usage instructions.

Each dataset has to be processed to be used in the IDS systems, the processing of each dataset within its specific folder will result in a dataset that can be used within Kitsune and HELAD.

These output files can be processed through SDNN_submit/convert_kitsune_file.py to be used with SDNN.

After converting the datasets to the required format, the IDS folders have specific instructions for running converted output file through each IDS

After gathering the results for each combination of dataset and IDS, the ResultsScripts folder can be used to derive the results for the given dataset.