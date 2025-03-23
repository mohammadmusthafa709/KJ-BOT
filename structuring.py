import json
import re

# Read the cleaned data
with open("cleaned_data.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

structured_data = []
current_url = None
current_content = []

# Regular expression to detect URLs in the format ===== URL =====
url_pattern = re.compile(r"^===== (https?://[^\s]+) =====$")

for line in lines:
    line = line.strip()
    
    url_match = url_pattern.match(line)
    if url_match:
        # Save previous URL-content pair if exists
        if current_url and current_content:
            structured_data.append({
                "url": current_url,
                "content": " ".join(current_content).strip()
            })
        
        # Start a new entry
        current_url = url_match.group(1)
        current_content = []
    else:
        # Collect content
        if line:
            current_content.append(line)

# Append the last entry
if current_url and current_content:
    structured_data.append({
        "url": current_url,
        "content": " ".join(current_content).strip()
    })

# Save to JSON
with open("structured_data.json", "w", encoding="utf-8") as json_file:
    json.dump(structured_data, json_file, indent=4, ensure_ascii=False)

print("✅ Data successfully structured into JSON!")
