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
/BoT_IoT: Contains the BoT_IoT related processing scripts.
/CICIDS2017: Contains the CICIDS2017 related processing scripts.
/CTU: Contains the CTU related processing scripts.
/EditedHELAD: Contains the HELAD IDS edited to output the RMSE output.
/EditedKitsune: Contains the Kitsune IDS edited to output the RMSE output.
/ResultsScripts: Contains the scripts used to process the results.
/Straosphere: Contains the BOTIOT assets for Straosphere.
/UNSW: Contains the UNSW related processing scripts.
/kitsune_to_sdn.py: Script to adapt Kitsune output for SDN environments.
/stratosphere_processing.ipynb: Jupyter notebook for processing data for Straosphere.
