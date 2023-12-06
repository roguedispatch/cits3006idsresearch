import subprocess
import os
import platform
import sys
import csv
import glob

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

def pcap2csv_with_tshark(files, output_path):
    tshark_path = _get_tshark_path()
    if not tshark_path:
        print("tshark not found.")
        sys.exit(1)

    fields = "-e frame.time_epoch -e frame.len -e eth.src -e eth.dst -e ip.src -e ip.dst " \
             "-e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e icmp.type -e icmp.code " \
             "-e arp.opcode -e arp.src.hw_mac -e arp.src.proto_ipv4 -e arp.dst.hw_mac -e arp.dst.proto_ipv4 " \
             "-e ipv6.src -e ipv6.dst -e tcp.flags.fin"

    header_written = False
    for input_path in files:
        source = os.path.splitext(os.path.basename(input_path))[0]
        cmd = [tshark_path, '-r', input_path, '-T', 'fields', '-E', 'separator=,', '-E', 'header=y', '-E', 'occurrence=f'] + fields.split()
        print(f"Executing command: {' '.join(cmd)}")

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            print("Standard Output:", stdout.decode())
            print("Standard Error:", stderr.decode())

            if process.returncode != 0:
                print(f"tshark process returned with error code {process.returncode}.")
            else:
                with open(output_path, 'a' if header_written else 'w', newline='') as output_file:
                    for line in stdout.decode().splitlines():
                        output_file.write(f"{line},{source}\n")
                    print("tshark parsing complete. Data appended to:", output_path)

        except subprocess.TimeoutExpired:
            print(f"tshark process timed out after 1 hour.")
        except Exception as e:
            print(f"An error occurred: {e}")

        if not header_written:
            header_written = True

if __name__ == "__main__":
    pcap_files = glob.glob('*.pcap')
    output_csv = 'combined_output.csv'
    pcap2csv_with_tshark(pcap_files, output_csv)
