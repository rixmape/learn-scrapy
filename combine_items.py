import json

# Load home spider output
with open("home_spider_output.json", "r", encoding="utf-8") as f:
    home_data = json.load(f)

# Load about spider output
with open("about_spider_output.json", "r", encoding="utf-8") as f:
    about_data = json.load(f)

# Combine corresponding items
combined_data = []
for home_item, about_item in zip(home_data, about_data):
    combined_item = {
        **home_item["item"],
        **about_item,
    }
    combined_data.append(combined_item)

# Output combined data in JSON format
output_file = "combined_output.json"
with open(output_file, "w") as f:
    json.dump(combined_data, f, indent=4)

print(f"Combined items saved to {output_file}")
