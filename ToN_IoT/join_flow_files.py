import csv

# Extract headers from the feature information
headers = [
    "ts","src_ip","src_port","dst_ip","dst_port","proto","service",
    "duration","src_bytes","dst_bytes","conn_state","missed_bytes",
    "src_pkts","src_ip_bytes","dst_pkts","dst_ip_bytes","dns_query",
    "dns_qclass","dns_qtype","dns_rcode","dns_AA","dns_RD","dns_RA",
    "dns_rejected","ssl_version","ssl_cipher","ssl_resumed","ssl_established",
    "ssl_subject","ssl_issuer","http_trans_depth","http_method","http_uri",
    "http_version","http_request_body_len","http_response_body_len","http_status_code",
    "http_user_agent","http_orig_mime_types","http_resp_mime_types","weird_name",
    "weird_addl","weird_notice","label","type"
]
print(len(headers))
# File names
files = [f"Flows/Network_dataset_{i}.csv" for i in range(1, 24)]

# Output file
output_file = "Flows/CombinedFlows.csv"

with open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(headers) 

    for file in files:
        with open(file, "r", newline="") as infile:
            reader = csv.reader(infile)
            hd = next(reader)
            print(len(hd))
            for row in reader:
                if len(row) != 45:
                    print(f"File {file} has an incorrect number of columns on some rows.")
                    break
                else:
                    writer.writerows(reader)

print(f"Data from {', '.join(files)} has been combined into {output_file}.")
