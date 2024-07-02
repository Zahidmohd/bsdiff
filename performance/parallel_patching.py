import bsdiff4
import os
import concurrent.futures
import time

# Function to create a patch
def create_patch(old_file, new_file, patch_file):
    with open(old_file, 'rb') as old_f:
        old_data = old_f.read()
    with open(new_file, 'rb') as new_f:
        new_data = new_f.read()
    
    patch = bsdiff4.diff(old_data, new_data)
    
    with open(patch_file, 'wb') as patch_f:
        patch_f.write(patch)

# Function to create patches in parallel
def parallel_patch_creation(file_pairs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for old_file, new_file, patch_file in file_pairs:
            futures.append(executor.submit(create_patch, old_file, new_file, patch_file))
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")

# Function to apply a patch
def apply_patch(old_file, patch_file, new_file_recreated):
    with open(old_file, 'rb') as old_f:
        old_data = old_f.read()
    with open(patch_file, 'rb') as patch_f:
        patch_data = patch_f.read()
    
    new_data = bsdiff4.patch(old_data, patch_data)
    
    with open(new_file_recreated, 'wb') as new_f:
        new_f.write(new_data)

# Function to apply patches in parallel
def parallel_patch_application(file_pairs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for old_file, patch_file, new_file_recreated in file_pairs:
            futures.append(executor.submit(apply_patch, old_file, patch_file, new_file_recreated))
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")

# Function to verify if two files are identical
def files_are_identical(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()

# Function to verify files in parallel
def parallel_file_verification(file_pairs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for file1, file2 in file_pairs:
            futures.append(executor.submit(files_are_identical, file1, file2))
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error occurred: {e}")
        return results

# Measure performance for creating patches in parallel
def create_patches_parallel(file_pairs):
    start_time = time.time()
    parallel_patch_creation(file_pairs)
    end_time = time.time()
    print(f"Parallel patch creation took {end_time - start_time:.2f} seconds.")

# Measure performance for applying patches in parallel
def apply_patches_parallel(file_pairs):
    start_time = time.time()
    parallel_patch_application(file_pairs)
    end_time = time.time()
    print(f"Parallel patch application took {end_time - start_time:.2f} seconds.")

# Measure performance for verifying files in parallel
def verify_patches_parallel(file_pairs):
    start_time = time.time()
    verification_results = parallel_file_verification(file_pairs)
    end_time = time.time()
    print(f"Parallel file verification took {end_time - start_time:.2f} seconds.")
    
    for i, result in enumerate(verification_results):
        if result:
            print(f"The files {file_pairs[i][0]} and {file_pairs[i][1]} are identical.")
        else:
            print(f"The files {file_pairs[i][0]} and {file_pairs[i][1]} are different.")

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

create_patches_parallel(file_pairs_creation)
apply_patches_parallel(file_pairs_application)
verify_patches_parallel(file_pairs_verification)
