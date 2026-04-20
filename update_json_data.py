import json

source_file_path = r"card_ids.json"
target_file_path = r"DuelMastersCards.json"

with open(source_file_path, "r", encoding="utf-8") as f:
    source_data = json.load(f)

with open(target_file_path, "r", encoding="utf-8") as f:
    target_data = json.load(f)

for source_card in source_data:
    for target_card in target_data["cards"]:
        if source_card["name"] == target_card["name"] and source_card["id"] not in target_card["uuid"]:
            target_card["uuid"].append(source_card["id"])
            break

with open(target_file_path, "w", encoding="utf-8") as f:
    json.dump(target_data, f, indent=2, ensure_ascii=False)

print("Updated file in place")

with open(target_file_path, "r", encoding="utf-8") as f:
    target_data = json.load(f)

count = 0

d = {
    "name": []
}

for target_card in target_data["cards"]:
    if not target_card["uuid"]:
        d["name"].append(target_card["name"])
        count += 1
        print(f"Card with name '{target_card['name']}' has an empty uuid list.")

print(f"Total cards with empty uuid list: {count}")