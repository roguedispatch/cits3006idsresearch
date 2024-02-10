def process_file(filename):
    TP, FP, TN, FN, total = 0, 0, 0, 0, 0
    threshold = 0.05  # Threshold for RMSE  
    flow_rmse = {}  # Dictionary to keep track of highest RMSE for each flow

    with open(filename, 'r') as f:
        header = f.readline()  # Skip the header

        # Skipping initial rows
        #unsw - 473418 / 320000
        for _ in range(473418):
            f.readline()

        # Process remaining lines
        for line in f:
            fields = line.strip().split('\t')
            #print(fields)
            label = fields[-4]
            #flow_id = fields[-5]
            rmse = float(fields[-2])
            #print(f"Flow {flow_id} has RMSE {rmse}")
            #if label == "BENIGN" or label == "ATTACK":
            #    # Update the dictionary with the highest RMSE value for each flow
            #    if flow_id not in flow_rmse or rmse > flow_rmse[flow_id][0]:
            #        #print(f"Flow {flow_id} has RMSE {rmse}")
            #        flow_rmse[flow_id] = (rmse, label)

    # Now evaluate each flow based on the highest RMSE recorded
    for rmse, label in flow_rmse.values():
        is_anomalous = rmse > threshold
        if label == "BENIGN":
            if is_anomalous:
                FP += 1
            else:
                TN += 1
        elif label == "ATTACK":
            if is_anomalous:
                TP += 1
            else:
                FN += 1

        total += 1

    # Calculate metrics
    accuracy = (TP + TN) / total if total > 0 else 0
    precision = TP / (TP + FP) if TP + FP > 0 else 0
    recall = TP / (TP + FN) if TP + FN > 0 else 0
    f1score = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0

    # Displaying Metrics
    print(f"Total Matched Flows: {total}")
    print(f"True Positives: {TP}")
    print(f"False Positives: {FP}")
    print(f"True Negatives: {TN}")
    print(f"False Negatives: {FN}")    
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1score}")

# Use the function
filename = "output_with_scores_thursday_new.tsv"
process_file(filename)
