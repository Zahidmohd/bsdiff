import bsdiff4

# Read the old and new files
with open('old_file.bin', 'rb') as old_file:
    old_data = old_file.read()
with open('new_file.bin', 'rb') as new_file:
    new_data = new_file.read()

# Generate the patch
patch = bsdiff4.diff(old_data, new_data)

# Write the patch to a file
with open('file.patch', 'wb') as patch_file:
    patch_file.write(patch)

print("Patch file created successfully.")
