import json
import re

def format_name(name):
    # Remove non-alphanumeric characters, then split by whitespace
    parts = re.split(r'[^a-zA-Z0-9]+', name)
    # Capitalize the first letter of each part and join them
    return "".join(part.capitalize() for part in parts if part)

def extract_names_and_sets(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for card in data.get("cards", []):
            formatted_name = format_name(card.get("name", ""))
            for printing in card.get("printings", []):
                set_name = printing.get("set")
                # Regex to extract the DM-XX part if it exists
                match = re.match(r"(DM-\d+)", set_name)
                formatted_set = match.group(1) if match else set_name
                print({"name": formatted_name, "set": formatted_set})
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_names_and_sets("DuelMastersCards.json")
