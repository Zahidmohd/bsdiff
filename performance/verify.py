# verify_files.py
def files_are_identical(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()

# Verify files for each size
sizes = [1, 10, 50]  # Sizes in MB
for i, size in enumerate(sizes):
    if files_are_identical(f'new_file_{i}.bin', f'new_file_recreated_{i}.bin'):
        print(f"The files for {size}MB are identical.")
    else:
        print(f"The files for {size}MB are different.")
