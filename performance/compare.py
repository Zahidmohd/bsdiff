def files_are_identical(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()

    return data1 == data2

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file1> <file2>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    if files_are_identical(file1, file2):
        print("Files are identical.")
        sys.exit(0)
    else:
        print("Files are different.")
        sys.exit(1)
