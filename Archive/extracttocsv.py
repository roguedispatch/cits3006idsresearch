import subprocess
import os
import platform
import sys
import csv

def _get_tshark_path():
    if platform.system() == 'Windows':
        return 'C:\\Program Files\\Wireshark\\tshark.exe'
    else:
        system_path = os.environ['PATH']
        for path in system_path.split(os.pathsep):
            filename = os.path.join(path, 'tshark')
            if os.path.isfile(filename):
                return filename
    return ''


def pcap2csv_with_tshark(input_path, output_path):
    tshark_path = _get_tshark_path()
    if not tshark_path:
        print("tshark not found.")
        sys.exit(1)

    fields = "-e frame.time_epoch -e frame.len -e eth.src -e eth.dst -e ip.src -e ip.dst " \
             "-e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e icmp.type -e icmp.code " \
             "-e arp.opcode -e arp.src.hw_mac -e arp.src.proto_ipv4 -e arp.dst.hw_mac -e arp.dst.proto_ipv4 " \
             "-e ipv6.src -e ipv6.dst"

    cmd = [tshark_path, '-r', input_path, '-T', 'fields', '-E', 'separator=,', '-E', 'header=y', '-E', 'occurrence=f'] + fields.split()
    with open(output_path, 'w') as output_file:
        process = subprocess.Popen(cmd, stdout=output_file, stderr=subprocess.PIPE, text=True)
        line_count = 0

    print("tshark parsing complete. File saved as:", output_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract features with tshark")
    parser.add_argument('-i', '--input', required=True, help="Input pcap file path")
    parser.add_argument('-o', '--output', required=True, help="Output CSV file path")
    args = parser.parse_args()

    pcap2csv_with_tshark(args.input, args.output)