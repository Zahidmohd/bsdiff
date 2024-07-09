import bsdiff4
import time
import tracemalloc

# Function to start memory tracing
def start_memory_tracing():
    tracemalloc.start()

# Function to stop memory tracing and print current memory usage
def stop_memory_tracing():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("[ Top 10 memory usage ]")
    for stat in top_stats[:10]:
        print(stat)

    tracemalloc.stop()

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
    
    with open(patch_file, 'wb') as patch_f:
        patch_f.write(patch)
    
    return end_time - start_time

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

# File sizes to test
sizes = [1 * 1024 * 1024, 10 * 1024 * 1024, 50 * 1024 * 1024]

# Measure performance for each test file
for i, size in enumerate(sizes):
    old_file = f'old_file_{i}.bin'
    new_file = f'new_file_{i}.bin'
    patch_file = f'file_{i}.patch'
    new_file_recreated = f'new_file_recreated_{i}.bin'
    
    # Start memory tracing for patch creation
    start_memory_tracing()
    
    # Measure patch creation
    creation_time = create_patch_in_chunks(old_file, new_file, patch_file)
    
    # Stop memory tracing and print memory usage
    stop_memory_tracing()

    print(f"Patch creation for {size//(1024*1024)}MB files took {creation_time:.2f} seconds.")
    
    # Start memory tracing for patch application
    start_memory_tracing()

    # Measure patch application
    application_time = apply_patch_in_chunks(old_file, patch_file, new_file_recreated)

    # Stop memory tracing and print memory usage
    stop_memory_tracing()

    print(f"Patch application for {size//(1024*1024)}MB files took {application_time:.2f} seconds.")
    
    # Verify patched files
    if files_are_identical_in_chunks(new_file, new_file_recreated):
        print(f"The files for {size//(1024*1024)}MB are identical.")
    else:
        print(f"The files for {size//(1024*1024)}MB are different.")
