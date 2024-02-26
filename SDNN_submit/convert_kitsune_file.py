import pandas as pd
import sys

# Check if the correct number of command line arguments is provided
if len(sys.argv) != 2:
    print("Usage: python convert_kitsune_file.py <input_file.csv>")
    sys.exit(1)

# Get the input file name from the command line arguments
input_file = sys.argv[1]

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Remove the last two columns
# df = df.iloc[:, :-2]
df = df.drop('Flow ID', axis=1)
df = df.drop('Attack Category',axis=1)
# Rename the "Label" column to "label"
df = df.rename(columns={'Label': 'label'})
df = df[df['label'] != 'unknown']
# Create the output file name
output_file = f"{input_file.split('.')[0]}_forsdnn.csv"

# Save the modified DataFrame to the output file
df.to_csv(output_file, index=False)

# Optional: Display a message indicating the process is complete
print(f"File '{output_file}' created successfully.")
