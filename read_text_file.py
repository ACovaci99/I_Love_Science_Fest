# Specify the path to your text file
file_path = 'env.yml'

try:
    # Open the file for reading
    with open(file_path, 'r') as file:
        # Read the entire contents of the file
        file_contents = file.read()
        # Print or process the contents as needed
        print(file_contents)

except FileNotFoundError:
    print(f"File not found: {file_path}")