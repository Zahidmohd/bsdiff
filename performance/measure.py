# measure_patch_creation.py
import bsdiff4
import time

def create_patch(old_file, new_file, patch_file):
    with open(old_file, 'rb') as old_f:
        old_data = old_f.read()
    with open(new_file, 'rb') as new_f:
        new_data = new_f.read()
    
    start_time = time.time()
    patch = bsdiff4.diff(old_data, new_data)
    end_time = time.time()
    
    with open(patch_file, 'wb') as patch_f:
        patch_f.write(patch)
    
    return end_time - start_time

# Measure patch creation time for each test file
sizes = [1, 10, 50]  # Sizes in MB
for i, size in enumerate(sizes):
    old_file = f'old_file_{i}.bin'
    new_file = f'new_file_{i}.bin'
    patch_file = f'file_{i}.patch'
    duration = create_patch(old_file, new_file, patch_file)
    print(f"Patch creation for {size}MB files took {duration:.2f} seconds.")
