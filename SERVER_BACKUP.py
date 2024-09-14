import subprocess
import os
import shutil

def compress_and_copy(source_dir, output_dir):
    # Get the base name of the source directory to use as the folder and archive name
    dir_name = os.path.basename(os.path.normpath(source_dir))
    
    # Handle special case where dir_name might be empty (e.g., if path ends with a backslash)
    if not dir_name:
        dir_name = os.path.basename(os.path.dirname(os.path.normpath(source_dir)))
    
    # Replace spaces in dir_name with underscores for the archive name
    archive_name = dir_name.replace(' ', '_')
    
    # Convert dir_name to uppercase for the folder name
    folder_name = dir_name.upper()
    
    # Define the subfolder in the output directory
    output_subdir = os.path.join(output_dir, folder_name)
    
    # Ensure the output subdirectory exists
    os.makedirs(output_subdir, exist_ok=True)
    
    # Define the output file path within the subfolder
    output_file = os.path.join(output_subdir, f'{archive_name}.7z')
    compressed_file = output_file + ".temp"
    
    # Normalize paths
    source_dir = os.path.normpath(source_dir)
    output_file = os.path.normpath(output_file)
    compressed_file = os.path.normpath(compressed_file)
    
    # Ensure paths are properly quoted
    source_dir_quoted = f'"{source_dir}"'
    compressed_file_quoted = f'"{compressed_file}"'
    
    # Use the full path to 7z.exe if necessary
    seven_zip_path = '7z'  # Or specify the full path, e.g., r"C:\Program Files\7-Zip\7z.exe"
    
    # Construct the command
    command = f'{seven_zip_path} a {compressed_file_quoted} {source_dir_quoted}'
    
    # Print the command for debugging
    print(f"Running command: {command}")
    
    # Execute the command and capture output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Check if the compression was successful
    if result.returncode == 0 and os.path.exists(compressed_file):
        # Remove the existing .7z file if it exists
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # Move the compressed file to the target location, renaming it
        shutil.move(compressed_file, output_file)
        print(f"Compressed and copied {source_dir} to {output_file}\n")
    else:
        print(f"Compression failed for {source_dir}")
        print("Error output:")
        print(result.stderr)
        print()

# List of source directories
source_directories = [
    r"W:\Docker\Config\Adguard",
    r"W:\Docker\Config\homebridge",
    r"W:\Docker\Config\MTProto",
    r"B:\Squire\Config\Bazarr",
    r"B:\Squire\Config\Kometa",
    r"B:\Squire\Config\Overseerr",
    r"B:\Squire\Config\Prowlarr",
    r"B:\Squire\Config\Radarr",
    r"B:\Squire\Config\Sonarr",
    r"B:\Squire\Config\Tautulli",
    r"B:\Squire\Config\Unpackerr",
    r"C:\Users\spenc\AppData\Local\Plex Media Server",  
    R"O:\Tdarr"
]

# Output directory
output_directory = r"C:\Users\spenc\OneDrive - NorviTech\SYSTEM\BACKUP"

# Loop over each source directory and compress it
for source_directory in source_directories:
    compress_and_copy(source_directory, output_directory)
