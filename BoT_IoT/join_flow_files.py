import csv

# Extract headers from the feature information
headers = [
    "pkSeqID","stime","flgs","proto","saddr","sport","daddr","dport",
    "pkts","bytes","state","ltime","seq","dur","mean","stddev","smac",
    "dmac","sum","min","max","soui","doui","sco","dco","spkts","dpkts",
    "sbytes","dbytes","rate","srate","drate","attack","category","subcategory" 
]
print(len(headers))
# File names
# Todo EDIT BELOW
files = [f"Flows/UNSW_2018_IoT_Botnet_Dataset_{i}.csv" for i in range(1,7)]

# Output file
output_file = "Flows/CombinedFlows.csv"

with open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(headers) 
    for file in files:
        with open(file, "r", newline="") as infile:
            reader = csv.reader(infile)
            for row in reader:
                # Todo EDIT BELOW
                if len(row) != 35:
                    print(f"File {file} has an incorrect number of columns on row {row} with len {len(row)}.")
                    break
                else:
                    writer.writerows(reader)

print(f"Data from {', '.join(files)} has been combined into {output_file}.")
