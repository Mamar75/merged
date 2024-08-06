import pandas as pd
import time
from tqdm import tqdm


# Function to filter rows based on the first two digits of 'gsubind' and 'gsubind_o'
def filter_gsubind(df):
    return df[~(df['gsubind'].astype(str).str.startswith('40') | df['gsubind_o'].astype(str).str.startswith('40'))]


def remove_self_owned(df):
    return df[~(df['cik_owner'] == df['cik_company'])]

# File path to your large CSV
file_path = 'pair_data.csv'
output_file_path = 'pair_data_nf.csv'

# Define the chunk size to read the CSV in parts
chunk_size = 100000  # You can adjust this size based on your memory capacity

# Get the total number of lines in the file (for progress tracking)
total_lines = sum(1 for _ in open(file_path))
total_chunks = (total_lines // chunk_size) + 1

# Initialize the progress bar
progress_bar = tqdm(total=total_chunks, unit='chunk')

# Start time for tracking
start_time = time.time()

# Use a context manager to open the output file
with pd.read_csv(file_path, chunksize=chunk_size) as reader:
    for i, chunk in enumerate(reader):
        # Filter the chunk
        filtered_chunk = filter_gsubind(chunk)
        filtered_chunk = remove_self_owned(filtered_chunk)

        # Write the filtered chunk to the output file
        if i == 0:
            # Write the header in the first chunk
            filtered_chunk.to_csv(output_file_path, mode='w', index=False)
        else:
            # Append to the file for subsequent chunks
            filtered_chunk.to_csv(output_file_path, mode='a', index=False, header=False)

        # Update the progress bar
        progress_bar.update(1)

        # Calculate elapsed time and estimated time remaining
        elapsed_time = time.time() - start_time
        estimated_total_time = (elapsed_time / (i + 1)) * total_chunks
        estimated_time_remaining = estimated_total_time - elapsed_time

        # Print progress and estimated time remaining
        progress_bar.set_postfix({
            'Elapsed Time': f'{elapsed_time:.2f}s',
            'Estimated Time Remaining': f'{estimated_time_remaining:.2f}s'
        })

# Close the progress bar
progress_bar.close()

print(f"Filtered data has been written to {output_file_path}")