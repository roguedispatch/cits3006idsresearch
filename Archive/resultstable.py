def process_file(filename):
    TP, FP, TN, FN, total = 0, 0, 0, 0, 0
    threshold = 0.125

    with open(filename, 'r') as f:
        # Skip the header
        header = f.readline()

        for _ in range(49861):
            f.readline()

        for line in f:
            fields = line.strip().split('\t')
            label = fields[-3]
            rmse = float(fields[-1])

            # Classification
            is_anomalous = rmse > threshold
            if label == "BENIGN":
                if is_anomalous:
                    FP += 1
                else:
                    TN += 1
            else:  # Malicious flows
                if is_anomalous:
                    TP += 1
                else:
                    FN += 1

            total += 1

    # Displaying Metrics
    print(f"Total Matched Flows: {total}")
    print(f"True Positives: {TP}")
    print(f"False Negatives: {FN}")
    print(f"False Positives: {FP}")
    print(f"True Negatives: {TN}")
    print(f"Accuracy: {(TP + TN) / total}") # Accuracy - the proportion of true results (both true positives and true negatives) among the total number of cases examined.
    print(f"Precision: {TP / (TP + FP) if TP + FP != 0 else 0}") # Precision - the proportion of true labelled attacks among all the cases that were classified as an attack.
    print(f"Recall: {TP / (TP + FN) if TP + FN != 0 else 0}") # Recall - the proportion of labelled attacks among all the cases that were actually an attack.


# Use the function
filename = "output_with_rmse.tsv"
process_file(filename)
