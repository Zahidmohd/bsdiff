# measure_patch_application.py
import bsdiff4
import time
import psutil
import os

def apply_patch(old_file, patch_file, new_file_recreated):
    with open(old_file, 'rb') as old_f:
        old_data = old_f.read()
    with open(patch_file, 'rb') as patch_f:
        patch_data = patch_f.read()
    
    start_time = time.time()
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss
    cpu_before = process.cpu_times()

    new_data = bsdiff4.patch(old_data, patch_data)

    memory_after = process.memory_info().rss
    cpu_after = process.cpu_times()
    end_time = time.time()
    
    with open(new_file_recreated, 'wb') as new_f:
        new_f.write(new_data)
    
    memory_used = memory_after - memory_before
    cpu_used = (cpu_after.user - cpu_before.user) + (cpu_after.system - cpu_before.system)
    
    return end_time - start_time, memory_used, cpu_used

# Measure performance for each test file
sizes = [1, 10, 50]  # Sizes in MB
for i, size in enumerate(sizes):
    old_file = f'old_file_{i}.bin'
    patch_file = f'file_{i}.patch'
    new_file_recreated = f'new_file_recreated_{i}.bin'
    
    application_time, memory_used, cpu_used = apply_patch(old_file, patch_file, new_file_recreated)
    print(f"Patch application for {size}MB files took {application_time:.2f} seconds, used {memory_used / (1024 * 1024):.2f} MB of memory, CPU usage is {cpu_used:.2f} seconds")
