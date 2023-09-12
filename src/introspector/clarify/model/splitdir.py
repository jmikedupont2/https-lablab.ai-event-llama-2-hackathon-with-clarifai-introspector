import os

# Set the directory path where you want to perform the operation
directory_path = "outputs"
N = 3  # Replace this with the number of characters you want to split by

# Get a list of all files in the directory
file_list = os.listdir(directory_path)

# Iterate through each file in the directory
for filename in file_list:
    if os.path.isfile(os.path.join(directory_path, filename)):
        # Split the filename by the first N characters
        file_prefix = filename[:N]
        file_suffix = filename[N:]
        directory_parts = directory_path.split(file_prefix, 1)
        new_directory = os.path.join(directory_parts[0], file_prefix)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

        new_file_path = os.path.join(new_directory, file_suffix)
        old_file_path = os.path.join(directory_path, filename)
        os.rename(old_file_path, new_file_path)
        #print("mv",old_file_path, new_file_path)

print("Files and directories have been split successfully.")
