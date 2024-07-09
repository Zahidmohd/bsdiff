import bsdiff4
import os
import time

# Function to create a patch in chunks
def create_patch_in_chunks(old_file, new_file, patch_file, chunk_size=1024*1024):
    with open(old_file, 'rb') as old_f, open(new_file, 'rb') as new_f:
        old_data = []
        new_data = []
        while True:
            old_chunk = old_f.read(chunk_size)
            new_chunk = new_f.read(chunk_size)
            if not old_chunk and not new_chunk:
                break
            old_data.append(old_chunk)
            new_data.append(new_chunk)

    start_time = time.time()
    patch = bsdiff4.diff(b''.join(old_data), b''.join(new_data))
    end_time = time.time()

    patch_size = len(patch) / (1024 * 1024)  # Convert to MB

    with open(patch_file, 'wb') as patch_f:
        patch_f.write(patch)

    return end_time - start_time, patch_size

# Function to apply a patch in chunks
def apply_patch_in_chunks(old_file, patch_file, new_file_recreated, chunk_size=1024*1024):
    with open(old_file, 'rb') as old_f, open(patch_file, 'rb') as patch_f:
        old_data = []
        patch_data = patch_f.read()  # Read the entire patch file at once
        while True:
            old_chunk = old_f.read(chunk_size)
            if not old_chunk:
                break
            old_data.append(old_chunk)

    start_time = time.time()
    new_data = bsdiff4.patch(b''.join(old_data), patch_data)
    end_time = time.time()

    with open(new_file_recreated, 'wb') as new_f:
        new_f.write(new_data)

    return end_time - start_time

# Function to verify if two files are identical in chunks
def files_are_identical_in_chunks(file1, file2, chunk_size=1024*1024):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        while True:
            chunk1 = f1.read(chunk_size)
            chunk2 = f2.read(chunk_size)
            if chunk1 != chunk2:
                return False
            if not chunk1 and not chunk2:
                break
    return True

# Measure performance, patch size, and verification for creating and applying patches in chunks
sizes = [1 * 1024 * 1024, 10 * 1024 * 1024, 50 * 1024 * 1024]
for i, size in enumerate(sizes):
    old_file = f'old_file_{i}.bin'
    new_file = f'new_file_{i}.bin'
    patch_file = f'file_{i}.patch'
    new_file_recreated = f'new_file_recreated_{i}.bin'
    
    print(f"\nProcessing {size // (1024 * 1024)}MB files:")
    
    # Measure patch creation in chunks
    creation_time, patch_size = create_patch_in_chunks(old_file, new_file, patch_file)
    print(f"Patch creation in chunks took {creation_time:.2f} seconds.")
    print(f"Patch size: {patch_size:.2f} MB")
    
    # Measure patch application in chunks
    application_time = apply_patch_in_chunks(old_file, patch_file, new_file_recreated)
    print(f"Patch application in chunks took {application_time:.2f} seconds.")
    
    # Verify patched files in chunks
    if files_are_identical_in_chunks(new_file, new_file_recreated):
        print(f"The files are identical.")
    else:
        print(f"The files are different.")
