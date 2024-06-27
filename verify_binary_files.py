# Read and print the content of old_file.bin
with open('old_file.bin', 'rb') as old_file:
    old_content = old_file.read()
    print("Content of old_file.bin:")
    print(old_content.decode('utf-8'))

# Read and print the content of new_file.bin
with open('new_file.bin', 'rb') as new_file:
    new_content = new_file.read()
    print("\nContent of new_file.bin:")
    print(new_content.decode('utf-8'))
