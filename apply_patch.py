import bsdiff4

# Read the old file and patch file
with open('old_file.bin', 'rb') as old_file:
    old_data = old_file.read()
with open('file.patch', 'rb') as patch_file:
    patch_data = patch_file.read()

# Apply the patch to recreate the new file
new_data = bsdiff4.patch(old_data, patch_data)

# Write the recreated new file
with open('new_file_recreated.bin', 'wb') as new_file:
    new_file.write(new_data)

print("New file recreated successfully.")
