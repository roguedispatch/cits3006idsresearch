import csv
import json
import sys

class FlowCleaner:

    PROTOCOLS = {
        'tcp': 6,
        'udp': 17,
        'ip': 0
    }

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def extract_flows(self):
        """Extract flows from the input file."""
        flows = []
        with open(self.input_path, 'r') as infile:
            reader = csv.DictReader(infile, delimiter=',')
            for row in reader:
                flow_data = json.loads(row['flow'])
                label = row['label']
                flows.append((flow_data, label))
        return flows

    def save_cleaned_flows(self, flows):
        """Save cleaned flow and label information to the CSV."""
        with open(self.output_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            # Write headers
            writer.writerow(['starttime', 'uid', 'saddr', 'sport', 'daddr', 'dport', 'proto', 'dur', 'appproto', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'smac', 'dmac', 'state', 'history', 'type_', 'dir_', 'label'])
            for flow, label in flows:
                flow['proto'] = self.PROTOCOLS.get(flow['proto'].lower(), flow['proto'])
                writer.writerow([flow['starttime'], flow['uid'], flow['saddr'], flow['sport'], flow['daddr'], flow['dport'], flow['proto'], flow['dur'], flow['appproto'], flow['spkts'], flow['dpkts'], flow['sbytes'], flow['dbytes'], flow['smac'], flow['dmac'], flow['state'], flow['history'], flow['type_'], flow['dir_'], label])

    def process(self):
        flows = self.extract_flows()
        self.save_cleaned_flows(flows)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: cleaner.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    cleaner = FlowCleaner(input_path, output_path)
    cleaner.process()
