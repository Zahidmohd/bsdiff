import os

def create_base_text(size):
    """Create base text with the specified size by repeating a paragraph."""
    base_paragraph = (
        "This is a sample paragraph used for generating test files. "
        "It contains enough text to reach the desired size. "
        "The quick brown fox jumps over the lazy dog. "
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Vivamus lacinia odio vitae vestibulum vestibulum. "
        "Cras vehicula nunc et enim venenatis, sit amet gravida est aliquam. "
    )
    # Repeat the paragraph to reach the desired size
    repeated_text = (base_paragraph * ((size // len(base_paragraph)) + 1))[:size]
    return repeated_text

def modify_text(text, modifications):
    """Modify the base text by applying the given modifications."""
    text_list = list(text)
    for position, new_char in modifications:
        if position < len(text_list):
            text_list[position] = new_char
    return ''.join(text_list)

def create_binary_file(filename, content):
    """Create a binary file with the specified text content."""
    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))

# Sizes of the test files in bytes (1MB, 10MB, 50MB)
sizes = [1 * 1024 * 1024, 10 * 1024 * 1024, 50 * 1024 * 1024]

# Create old and new files with slight differences
for i, size in enumerate(sizes):
    # Create base text for the old file
    base_text = create_base_text(size)
    
    # Create the old file with the base text
    create_binary_file(f'old_file_{i}.bin', base_text)
    
    # Define some modifications (e.g., change some characters)
    modifications = [(10, 'A'), (20, 'B'), (30, 'C')]  # (position, new_char)
    
    # Create the new text by modifying the base text
    new_text = modify_text(base_text, modifications)
    
    # Create the new file with the modified text
    create_binary_file(f'new_file_{i}.bin', new_text)

print("Test files created successfully.")
