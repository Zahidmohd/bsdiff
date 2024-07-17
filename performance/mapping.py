import os
import bsdiff4
import time
import mmap

def create_patch_mmap(old_file, new_file, patch_file):
    with open(old_file, 'rb') as old_f, open(new_file, 'rb') as new_f:
        old_size = os.path.getsize(old_file)
        new_size = os.path.getsize(new_file)
        
        old_map = mmap.mmap(old_f.fileno(), old_size, access=mmap.ACCESS_READ)
        new_map = mmap.mmap(new_f.fileno(), new_size, access=mmap.ACCESS_READ)
        
        old_bytes = old_map[:]  # Convert mmap to bytes
        new_bytes = new_map[:]  # Convert mmap to bytes
        
        start_time = time.time()
        patch = bsdiff4.diff(old_bytes, new_bytes)
        end_time = time.time()
        
        old_map.close()
        new_map.close()
    
    patch_size = len(patch) / (1024 * 1024)  # Convert to MB
    
    with open(patch_file, 'wb') as patch_f:
        patch_f.write(patch)
    
    return end_time - start_time, patch_size

def apply_patch_mmap(old_file, patch_file, new_file_recreated):
    with open(old_file, 'rb') as old_f, open(patch_file, 'rb') as patch_f:
        old_size = os.path.getsize(old_file)
        patch_size = os.path.getsize(patch_file)
        
        old_map = mmap.mmap(old_f.fileno(), old_size, access=mmap.ACCESS_READ)
        patch_map = mmap.mmap(patch_f.fileno(), patch_size, access=mmap.ACCESS_READ)
        
        old_bytes = old_map[:]  # Convert mmap to bytes
        patch_bytes = patch_map[:]  # Convert mmap to bytes
        
        start_time = time.time()
        new_data = bsdiff4.patch(old_bytes, patch_bytes)
        end_time = time.time()
        
        old_map.close()
        patch_map.close()
    
    with open(new_file_recreated, 'wb') as new_f:
        new_f.write(new_data)
    
    return end_time - start_time

def files_are_identical_mmap(file1, file2):
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)
    if size1 != size2:
        return False
    
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        map1 = mmap.mmap(f1.fileno(), size1, access=mmap.ACCESS_READ)
        map2 = mmap.mmap(f2.fileno(), size2, access=mmap.ACCESS_READ)
        
        if map1[:] != map2[:]:
            map1.close()
            map2.close()
            return False
        
        map1.close()
        map2.close()
    return True

# File sizes to test
sizes = [0.246, 1, 10, 50]  # Sizes in MB

# Measure performance and patch size for each test file
for i, size in enumerate(sizes):
    old_file = f'old_file_{i}.bin'
    new_file = f'new_file_{i}.bin'
    patch_file = f'file_{i}.patch'
    new_file_recreated = f'new_file_recreated_{i}.bin'
    
    print(f"\nProcessing {size:.2f} MB files:")
    
    # Measure patch creation
    creation_time, patch_size = create_patch_mmap(old_file, new_file, patch_file)
    print(f"Patch creation for {size:.2f} MB files took {creation_time:.2f} seconds.")
    print(f"Patch size: {patch_size:.2f} MB")
    
    # Measure patch application
    application_time = apply_patch_mmap(old_file, patch_file, new_file_recreated)
    print(f"Patch application for {size:.2f} MB files took {application_time:.2f} seconds.")
    
    # Verify patched files
    if files_are_identical_mmap(new_file, new_file_recreated):
        print(f"The files for {size:.2f} MB are identical.")
    else:
        print(f"The files for {size:.2f} MB are different.")
