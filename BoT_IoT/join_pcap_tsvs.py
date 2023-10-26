import csv

def read_headers(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        headers = next(reader)
    return headers

def get_top_level_protocol(protocol_stack):
    protocols = [
        "udp", "arp", "tcp", "ospf", "icmp", "igmp", "sctp", "udt", "sep", "sun-nd", 
        "swipe", "mobile", "pim", "rtp", "ipnip", "ip", "ggp", "st2", "egp", "cbt", 
        "emcon", "nvp", "igp", "xnet", "argus", "bbn-rcc", "chaos", "pup", "hmp", 
        "mux", "dcn", "prm", "trunk-1", "xns-idp", "trunk-2", "leaf-1", "leaf-2", 
        "irtp", "rdp", "iso-tp4", "netblt", "mfe-nsp", "merit-inp", "3pc", "xtp", 
        "idpr", "tp++", "ddp", "idpr-cmtp", "ipv6", "il", "idrp", "ipv6-frag", 
        "sdrp", "ipv6-route", "gre", "rsvp", "mhrp", "bna", "esp", "i-nlsp", "narp", 
        "ipv6-no", "tlsp", "skip", "ipv6-opts", "any", "cftp", "sat-expak", "kryptolan", 
        "rvd", "ippc", "sat-mon", "ipcv", "visa", "cpnx", "cphb", "wsn", "pvp", 
        "br-sat-mon", "wb-mon", "wb-expak", "iso-ip", "secure-vmtp", "vmtp", "vines", 
        "ttp", "nsfnet-igp", "dgp", "tcf", "eigrp", "sprite-rpc", "larp", "mtp", "ax.25", 
        "ipip", "micp", "aes-sp3-d", "encap", "etherip", "pri-enc", "gmtp", "pnni", 
        "ifmp", "aris", "qnx", "a/n", "scps", "snp", "ipcomp", "compaq-peer", "ipx-n-ip", 
        "vrrp", "zero", "pgm", "iatp", "ddx", "l2tp", "srp", "stp", "smp", "uti", 
        "sm", "ptp", "fire", "crtp", "isis", "crudp", "sccopmce", "sps", "pipe", 
        "iplt", "unas", "fc", "ib"
    ]
    for protocol in reversed(protocol_stack.split(':')):
        if protocol in protocols:
            return protocol

    return protocol_stack.split(':')[-1]

def combine_tsvs(start, end, output_file):
    # Todo EDIT BELOW
    first_file = f"Raw/IoT_Dataset_OSScan__0000{start}.pcap.tsv"
    original_headers = read_headers(first_file)
    
    output_headers = list(original_headers)
    if 'sll.src.eth' in output_headers:
        output_headers.remove('sll.src.eth')
    if 'eth.src' not in output_headers:
        output_headers.append('eth.src')
    if 'frame.protocols' in original_headers: 
        output_headers[original_headers.index('frame.protocols')] = 'protocol' 

    with open(output_file, 'w', newline='') as out_file:
        writer = csv.writer(out_file, delimiter='\t')
        writer.writerow(output_headers)

        for i in range(start, end + 1):
            # Todo EDIT BELOW
            current_file = f"Raw/IoT_Dataset_OSScan__0000{start}.pcap.tsv"
            current_headers = read_headers(current_file)
            if set(current_headers) != set(original_headers):
                print(f"Warning: Headers in {current_file} do not match the original headers. Skipping file.")
                continue

            with open(current_file, 'r') as file:
                reader = csv.DictReader(file, delimiter='\t')

                for row in reader:
                    if 'sll.src.eth' in row:
                        row['eth.src'] = row['sll.src.eth']
                        del row['sll.src.eth']

                    if 'frame.protocols' in row:
                        row['protocol'] = get_top_level_protocol(row['frame.protocols'])
                        del row['frame.protocols']

                    writer.writerow([row[key] for key in output_headers])

        print(f"Combined TSV written to {output_file}")

# Todo EDIT BELOW
start, end = 1, 3
output_file = 'ScanningFirstThree.tsv'
combine_tsvs(start, end, output_file)
