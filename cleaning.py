import re

def clean_scraped_data(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    cleaned_data = []
    unique_content = set()
    current_url = None
    temp_content = []

    for line in lines:
        line = line.strip()
        
        if line.startswith("=====") and "http" in line:
            # Save previous URL's content if exists
            if current_url and temp_content:
                cleaned_data.append(current_url)
                cleaned_data.extend(temp_content)
                cleaned_data.append("\n")  # Add spacing
            
            # New URL found
            current_url = line
            temp_content = []
        
        elif line and line not in unique_content:
            temp_content.append(line)
            unique_content.add(line)

    # Add last URL's content
    if current_url and temp_content:
        cleaned_data.append(current_url)
        cleaned_data.extend(temp_content)

    # Write cleaned output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_data))

# Run the function
clean_scraped_data("scraped_data.txt", "cleaned_data.txt")
