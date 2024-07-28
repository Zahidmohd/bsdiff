import bsdiff4
import sys

def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)

def create_patch(old_file, new_file, patch_file):
    old_data = read_file(old_file)
    new_data = read_file(new_file)
    patch_data = bsdiff4.diff(old_data, new_data)
    write_file(patch_file, patch_data)

def apply_patch(old_file, patch_file, patched_file):
    old_data = read_file(old_file)
    patch_data = read_file(patch_file)
    patched_data = bsdiff4.patch(old_data, patch_data)
    write_file(patched_file, patched_data)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} oldfile newfile patchfile patchedfile")
        sys.exit(1)

    old_file = sys.argv[1]
    new_file = sys.argv[2]
    patch_file = sys.argv[3]
    patched_file = sys.argv[4]

    # Create patch
    create_patch(old_file, new_file, patch_file)
    print(f"Patch created successfully and saved to {patch_file}")

    # Apply patch
    apply_patch(old_file, patch_file, patched_file)
    print(f"Patch applied successfully and saved to {patched_file}")
