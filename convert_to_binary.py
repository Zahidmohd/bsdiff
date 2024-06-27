# Read the text file and write its content to a binary file

def convert_text_to_binary(input_text_file, output_binary_file):
    with open(input_text_file, 'r') as text_file:
        content = text_file.read()
    with open(output_binary_file, 'wb') as binary_file:
        binary_file.write(content.encode('utf-8'))

# Convert old_file.txt to old_file.bin
convert_text_to_binary('old_file.txt', 'old_file.bin')

# Convert new_file.txt to new_file.bin
convert_text_to_binary('new_file.txt', 'new_file.bin')
