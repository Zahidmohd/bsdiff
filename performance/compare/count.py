import os

def count_byte_differences(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        byte1 = f1.read(1)
        byte2 = f2.read(1)
        count = 0
        while byte1 and byte2:
            if byte1 != byte2:
                count += 1
            byte1 = f1.read(1)
            byte2 = f2.read(1)
        # Handle the case where files are of different lengths
        while byte1:
            count += 1
            byte1 = f1.read(1)
        while byte2:
            count += 1
            byte2 = f2.read(1)
    return count

# List of file pairs to compare
file_pairs = [
    ("old_firmware_246KB.bin", "new_firmware_246KB.bin"),
    ("old_firmware_50MB.bin", "new_firmware_50MB.bin"),
    ("old_firmware_1MB.bin", "new_firmware_1MB.bin"),
    ("old_firmware_10MB.bin", "new_firmware_10MB.bin")
]

for old_file, new_file in file_pairs:
    if os.path.exists(old_file) and os.path.exists(new_file):
        differences = count_byte_differences(old_file, new_file)
        print(f'Total differing bytes between {old_file} and {new_file}: {differences}')
    else:
        print(f'One or both files {old_file} and {new_file} do not exist.')
