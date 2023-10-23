import csv

def match(ids_output_path, source_dataset_path):
    # Load data from the IDS system
    with open(ids_output_path, 'r') as f:
        ids_data = list(csv.DictReader(f))

    # Load data from the source dataset
    with open(source_dataset_path, 'r') as f:
        source_data = list(csv.DictReader(f))

    matched_flows = []
    num_flow = 0
    for ids_flow in ids_data:
        for source_flow in source_data:
            # Matching criteria
            if (ids_flow['saddr'] == source_flow[' Source IP'] and
                ids_flow['daddr'] == source_flow[' Destination IP'] and
                ids_flow['sport'] == source_flow[' Source Port'] and
                ids_flow['dport'] == source_flow[' Destination Port'] and
                ids_flow['proto'] == source_flow[' Protocol']):
                    
                    matched_flow = {
                        'ids_label': ids_flow['label'],
                        'source_label': source_flow[' Label'],
                    }
                    matched_flows.append(matched_flow)
            
        print("Row " + str(num_flow) + " checked")
        num_flow += 1

    compute_metrics(matched_flows)


def compute_metrics(matched_flows):
    # Counters for matches and mismatches
    FN, FP, TP, TN = 0, 0, 0, 0

    for flow in matched_flows:
        ids_label = flow['ids_label']
        source_label = flow['source_label']

        if ids_label == 'malicious' and source_label != 'BENIGN':
            TP += 1
        elif ids_label == 'malicious' and source_label == 'BENIGN':
            FN += 1
        elif ids_label == 'benign' and source_label != 'BENIGN':
            FP += 1
        elif ids_label == 'benign' and source_label == 'BENIGN':
            TN += 1

    # Calculate metrics
    total = TP + FN + FP + TN
    if total == 0:
        print("No matched flows found!")
    else:
        print(f"Total Matched Flows: {total}")
        print(f"True Positives: {TP}")
        print(f"False Negatives: {FN}")
        print(f"False Positives: {FP}")
        print(f"True Negatives: {TN}")
        
        print(f"Accuracy: {(TP + TN) / total}")
        print(f"Precision: {TP / (TP + FP)}")
        print(f"Recall: {TP / (TP + FN)}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Match IDS output with source dataset")
    parser.add_argument('-i', '--ids', required=True, help="IDS output CSV file path")
    parser.add_argument('-s', '--source', required=True, help="Source dataset CSV file path")
    args = parser.parse_args()

    match(args.ids, args.source)
    
if __name__ == "__main__":
    main()