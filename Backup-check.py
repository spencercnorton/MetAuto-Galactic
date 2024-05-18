import os
import csv

# Directories to compare
directory1 = r'BACKUP_DIRECTORY'
directory2 = r'HOST_DIRECTORY'

# Get the list of folders in each directory
folders1 = set(next(os.walk(directory1))[1])
folders2 = set(next(os.walk(directory2))[1])

# Create the output CSV file
output_file = r'OUTPUT_DIRECTORY'

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['BACKUP', 'HOST', 'Present in Both'])

    for folder in folders1.union(folders2):
        present_in_dir1 = folder in folders1
        present_in_dir2 = folder in folders2
        present_in_both = present_in_dir1 and present_in_dir2
        writer.writerow([folder if present_in_dir1 else '', folder if present_in_dir2 else '', 'Yes' if present_in_both else 'No'])

print(f'Comparison file created: {output_file}')
