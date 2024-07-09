import bsdiff4
import os
import time
import psutil  # Import psutil for memory usage measurement

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
    
    # Calculate memory usage of patch
    patch_size = len(patch)
    mem_patch = patch_size / (1024 * 1024)  # Convert to MB
    
    with open(patch_file, 'wb') as patch_f:
        patch_f.write(patch)
    
    return end_time - start_time, mem_patch

# Function to apply a patch in chunks
def apply_patch_in_chunks(old_file, patch_file, new_file_recreated, chunk_size=1024*1024):
    with open(old_file, 'rb') as old_f, open(patch_file, 'rb') as patch_f:
        old_data = []
        patch_data = []
        while True:
            old_chunk = old_f.read(chunk_size)
            patch_chunk = patch_f.read(chunk_size)
            if not old_chunk and not patch_chunk:
                break
            old_data.append(old_chunk)
            patch_data.append(patch_chunk)
    
    start_time = time.time()
    new_data = bsdiff4.patch(b''.join(old_data), b''.join(patch_data))
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

def get_memory_usage():
    process = psutil.Process(os.getpid())
    mem_usage = process.memory_info().rss  # Get RSS (resident set size) memory usage
    return mem_usage

# Measure performance, memory usage, and patch size for creating patches in chunks
sizes = [1 * 1024 * 1024, 10 * 1024 * 1024, 50 * 1024 * 1024]
for i, size in enumerate(sizes):
    old_file = f'old_file_{i}.bin'
    new_file = f'new_file_{i}.bin'
    patch_file = f'file_{i}.patch'
    new_file_recreated = f'new_file_recreated_{i}.bin'
    
    # Measure memory usage before creating patch in chunks
    mem_before_creation = get_memory_usage()
    print(f"Memory usage before patch creation in chunks: {mem_before_creation / 1024 / 1024:.2f} MB")
    
    # Measure patch creation in chunks
    creation_time, patch_memory = create_patch_in_chunks(old_file, new_file, patch_file)
    print(f"Patch creation in chunks for {size//(1024*1024)}MB files took {creation_time:.2f} seconds.")
    print(f"Memory occupied by patch: {patch_memory:.2f} MB")
    
    # Measure memory usage after patch creation in chunks
    mem_after_creation = get_memory_usage()
    print(f"Memory usage after patch creation in chunks: {mem_after_creation / 1024 / 1024:.2f} MB")
    
    # Measure patch application in chunks
    application_time = apply_patch_in_chunks(old_file, patch_file, new_file_recreated)
    print(f"Patch application in chunks for {size//(1024*1024)}MB files took {application_time:.2f} seconds.")
    
    # Verify patched files in chunks
    if files_are_identical_in_chunks(new_file, new_file_recreated):
        print(f"The files for {size//(1024*1024)}MB are identical.")
    else:
        print(f"The files for {size//(1024*1024)}MB are different.")
    
    # Measure memory usage after patch application in chunks
    mem_after_application = get_memory_usage()
    print(f"Memory usage after patch application in chunks: {mem_after_application / 1024 / 1024:.2f} MB")

# Get memory usage at the end
memory_usage = get_memory_usage()
print(f"Memory usage at the end of execution: {memory_usage / 1024 / 1024:.2f} MB")
