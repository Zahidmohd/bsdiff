# create_test_files.py
import os

def create_binary_file(filename, size):
    with open(filename, 'wb') as f:
        f.write(os.urandom(size))

# Create test files of different sizes (e.g., 1MB, 10MB, 50MB)
sizes = [1 * 1024 * 1024, 10 * 1024 * 1024, 50 * 1024 * 1024]
for i, size in enumerate(sizes):
    create_binary_file(f'old_file_{i}.bin', size)
    create_binary_file(f'new_file_{i}.bin', size)

print("Test files created successfully.")
