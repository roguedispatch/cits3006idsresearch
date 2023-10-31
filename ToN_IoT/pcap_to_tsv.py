import platform
import subprocess
import os
from multiprocessing import Pool, Manager, cpu_count

def _get_tshark_path():
    if platform.system() == 'Windows':
        return r'C:\Program Files\Wireshark\tshark.exe'
    else:
        system_path = os.environ['PATH']
        for path in system_path.split(os.pathsep):
            filename = os.path.join(path, 'tshark')
            if os.path.isfile(filename):
                return filename
    return ''

def pcap2tsv_with_tshark(path, tshark_path, output_queue):
    fields = ("-e frame.time_epoch -e frame.len "
              "-e frame.protocols "
              "-e sll.src.eth " 
              "-e eth.src -e eth.dst " 
              "-e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport "
              "-e udp.dstport -e icmp.type -e icmp.code -e arp.opcode -e arp.src.hw_mac "
              "-e arp.src.proto_ipv4 -e arp.dst.hw_mac -e arp.dst.proto_ipv4 "
              "-e ipv6.src -e ipv6.dst")
    cmd = ('"' + tshark_path + '" -r "' + path + '" -T fields ' + fields +
           ' -E header=y -E occurrence=f > "' + path + '.tsv"')
    subprocess.call(cmd, shell=True)

    output_queue.put(path)

def progress_reporter(queue, total):
    processed_count = 0
    while processed_count < total:
        _ = queue.get()
        processed_count += 1
        print(f"Processed {processed_count}/{total} files")

if __name__ == '__main__':
    # File paths
    input_basepath = "."
    tshark_path = _get_tshark_path()

    input_files = [f"Raw/normal_{i}.pcap" for i in range(1, 3)]
    for i in input_files: 
        print(os.path.join(input_basepath, i))
    manager = Manager()
    output_queue = manager.Queue()

    num_processes = min(cpu_count(), 4)

    with Pool(processes=num_processes) as pool:
        pool.apply_async(progress_reporter, (output_queue, len(input_files)))

        pool.starmap(pcap2tsv_with_tshark, [(os.path.join(input_basepath, f), tshark_path, output_queue) for f in input_files])
