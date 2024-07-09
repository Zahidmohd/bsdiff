import os
import concurrent.futures
import time
import psutil
import bsdiff4

# Function to create a patch and measure its size and creation time
def create_patch(old_file, new_file, patch_file):
    with open(old_file, 'rb') as old_f:
        old_data = old_f.read()
    with open(new_file, 'rb') as new_f:
        new_data = new_f.read()
    
    start_time = time.time()
    patch = bsdiff4.diff(old_data, new_data)
    creation_time = time.time() - start_time

    with open(patch_file, 'wb') as patch_f:
        patch_f.write(patch)

    patch_size = len(patch)  # Calculate patch size
    return creation_time, patch_size

# Function to apply a patch and measure its application time
def apply_patch(old_file, patch_file, new_file_recreated):
    with open(old_file, 'rb') as old_f:
        old_data = old_f.read()
    with open(patch_file, 'rb') as patch_f:
        patch_data = patch_f.read()

    start_time = time.time()
    new_data = bsdiff4.patch(old_data, patch_data)
    application_time = time.time() - start_time

    with open(new_file_recreated, 'wb') as new_f:
        new_f.write(new_data)
    
    return application_time

# Function to verify if two files are identical
def files_are_identical(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()

# Measure performance for parallel patch creation
def create_patches_parallel(file_pairs):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(create_patch, old_file, new_file, patch_file) for old_file, new_file, patch_file in file_pairs]
        for future in concurrent.futures.as_completed(futures):
            try:
                creation_time, patch_size = future.result()
                results.append((creation_time, patch_size))
            except Exception as e:
                print(f"Error occurred: {e}")
    return results

# Measure performance for parallel patch application
def apply_patches_parallel(file_pairs):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(apply_patch, old_file, patch_file, new_file_recreated) for old_file, patch_file, new_file_recreated in file_pairs]
        for future in concurrent.futures.as_completed(futures):
            try:
                application_time = future.result()
                results.append(application_time)
            except Exception as e:
                print(f"Error occurred: {e}")
    return results

# Verify patches in parallel
def verify_patches_parallel(file_pairs):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(files_are_identical, file1, file2) for file1, file2 in file_pairs]
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error occurred: {e}")
    return results

# Example usage
file_pairs_creation = [
    ('old_file_0.bin', 'new_file_0.bin', 'file_0.patch'),
    ('old_file_1.bin', 'new_file_1.bin', 'file_1.patch'),
    ('old_file_2.bin', 'new_file_2.bin', 'file_2.patch'),
]

file_pairs_application = [
    ('old_file_0.bin', 'file_0.patch', 'new_file_recreated_0.bin'),
    ('old_file_1.bin', 'file_1.patch', 'new_file_recreated_1.bin'),
    ('old_file_2.bin', 'file_2.patch', 'new_file_recreated_2.bin'),
]

file_pairs_verification = [
    ('new_file_0.bin', 'new_file_recreated_0.bin'),
    ('new_file_1.bin', 'new_file_recreated_1.bin'),
    ('new_file_2.bin', 'new_file_recreated_2.bin'),
]

# Measure performance for parallel operations
creation_results = create_patches_parallel(file_pairs_creation)
application_results = apply_patches_parallel(file_pairs_application)
verification_results = verify_patches_parallel(file_pairs_verification)

# Print results
for i, (creation_time, patch_size) in enumerate(creation_results):
    print(f"Patch creation for {os.path.basename(file_pairs_creation[i][0])} -> {os.path.basename(file_pairs_creation[i][1])} took {creation_time:.2f} seconds.")
    print(f"Patch size: {patch_size / 1024 / 1024:.2f} MB")

for i, application_time in enumerate(application_results):
    print(f"Patch application for {os.path.basename(file_pairs_application[i][0])} -> {os.path.basename(file_pairs_application[i][1])} took {application_time:.2f} seconds.")

for i, result in enumerate(verification_results):
    if result:
        print(f"The files {file_pairs_verification[i][0]} and {file_pairs_verification[i][1]} are identical.")
    else:
        print(f"The files {file_pairs_verification[i][0]} and {file_pairs_verification[i][1]} are different.")
