import csv

# Extract headers from the feature information
headers = [
    "srcip", "sport", "dstip", "dsport", "proto", "state", "dur", "sbytes", 
    "dbytes", "sttl", "dttl", "sloss", "dloss", "service", "Sload", "Dload",
    "Spkts", "Dpkts", "swin", "dwin", "stcpb", "dtcpb", "smeansz", "dmeansz",
    "trans_depth", "res_bdy_len", "Sjit", "Djit", "Stime", "Ltime", "Sintpkt",
    "Dintpkt", "tcprtt", "synack", "ackdat", "is_sm_ips_ports", "ct_state_ttl",
    "ct_flw_http_mthd", "is_ftp_login", "ct_ftp_cmd", "ct_srv_src", "ct_srv_dst",
    "ct_dst_ltm", "ct_src_ ltm", "ct_src_dport_ltm", "ct_dst_sport_ltm", 
    "ct_dst_src_ltm", "attack_cat", "Label"
]

# File names
files = [f"UNSW-NB15_{i}.csv" for i in range(1, 5)]

# Output file
output_file = "CombinedFlows.csv"

with open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(headers) 

    for file in files:
        with open(file, "r", newline="") as infile:
            reader = csv.reader(infile)
            
            for row in reader:
                if len(row) != 49:
                    print(f"File {file} has an incorrect number of columns on some rows.")
                    break
                else:
                    writer.writerows(reader)

print(f"Data from {', '.join(files)} has been combined into {output_file}.")
