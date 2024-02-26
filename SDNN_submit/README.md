# Overview

This section relates to the adaptation of the Shallow and Deep Neural Networks papers' 3 layer deep neural network algorithm to a range of provided datasets. The kitsune data fields were used as the standard for this research, and thus that format has been translated to a form usable by the SDNN algorithm. 

# Building the environment

In this experiment, a python3.10 conda environment was used. The configuration from this environment has been provided in the conda_env.txt file. To replicate this environment, install conda or a variant (miniconda etc.) and run: 

`conda create --name <env_name> --file conda_env.txt`

# Running the code 

The convert_kitsune_file.py was used to translate the files from the kitsune format to the SDNN data format.

In general, to run the SDNN algorithm on a dataset the dataset should contain both training and testing data. 
The usage of the implemented python script is as follows: 

`python3 kitsune_to_sdnn.py <Input_File> <Number_of_training_rows>`

For example, in our experiment we ran the mirai dataset with 55,000 training rows. To replicate this, run: 

`python3 kitsune_to_sdnn.py Files/mirai.pcap.csv 55000`