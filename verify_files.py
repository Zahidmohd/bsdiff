def files_are_identical(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()

if files_are_identical('new_file.bin', 'new_file_recreated.bin'):
    print("The files are identical.")
else:
    print("The files are different.")
