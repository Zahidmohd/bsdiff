# measure_performance.py
import bsdiff4
import time
import psutil
import os

def create_patch(old_file, new_file, patch_file):
    with open(old_file, 'rb') as old_f:
        old_data = old_f.read()
    with open(new_file, 'rb') as new_f:
        new_data = new_f.read()
    
    start_time = time.time()
    process = psutil.Process(os.getpid())
    patch = bsdiff4.diff(old_data, new_data)
    end_time = time.time()
    
    with open(patch_file, 'wb') as patch_f:
        patch_f.write(patch)
    
    duration = end_time - start_time
    memory_used = process.memory_info().rss
    patch_size = os.path.getsize(patch_file)
    cpu_used = process.cpu_percent(interval=None)
    io_counters = process.io_counters()
    
    return duration, memory_used, patch_size, cpu_used, io_counters

def apply_patch(old_file, patch_file, new_file_recreated):
    with open(old_file, 'rb') as old_f:
        old_data = old_f.read()
    with open(patch_file, 'rb') as patch_f:
        patch_data = patch_f.read()
    
    start_time = time.time()
    process = psutil.Process(os.getpid())
    new_data = bsdiff4.patch(old_data, patch_data)
    end_time = time.time()
    
    with open(new_file_recreated, 'wb') as new_f:
        new_f.write(new_data)
    
    duration = end_time - start_time
    memory_used = process.memory_info().rss
    cpu_used = process.cpu_percent(interval=None)
    io_counters = process.io_counters()
    
    return duration, memory_used, cpu_used, io_counters

# Measure performance for each test file
sizes = [1, 10, 50]  # Sizes in MB
for i, size in enumerate(sizes):
    old_file = f'old_file_{i}.bin'
    new_file = f'new_file_{i}.bin'
    patch_file = f'file_{i}.patch'
    new_file_recreated = f'new_file_recreated_{i}.bin'
    
    # Measure patch creation
    creation_time, memory_used, patch_size, cpu_used, io_counters = create_patch(old_file, new_file, patch_file)
    print(f"Patch creation for {size}MB files:")
    print(f"Time: {creation_time:.2f} seconds")
    print(f"Memory: {memory_used / (1024 * 1024):.2f} MB")
    print(f"Patch Size: {patch_size / (1024 * 1024):.2f} MB")
    print(f"CPU: {cpu_used:.2f}%")
    print(f"I/O: {io_counters}")
    
    # Measure patch application
    application_time, memory_used, cpu_used, io_counters = apply_patch(old_file, patch_file, new_file_recreated)
    print(f"Patch application for {size}MB files:")
    print(f"Time: {application_time:.2f} seconds")
    print(f"Memory: {memory_used / (1024 * 1024):.2f} MB")
    print(f"CPU: {cpu_used:.2f}%")
    print(f"I/O: {io_counters}")
