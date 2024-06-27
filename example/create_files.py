# create_files.py
# Create old_file.bin with some initial data
with open('old_file.bin', 'wb') as old_file:
    old_file.write(b'Example data in the old file.\n')

# Create new_file.bin with modified data
with open('new_file.bin', 'wb') as new_file:
    new_file.write(b'Example data in the new file.\n')
