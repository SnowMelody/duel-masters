import os
import json
import xml.etree.ElementTree as ET

def extract_card_ids(root_folder, output_file):
    result = []

    # Only process these folders
    target_folders = [
        "18a06307-e6d0-4877-87b4-39ed788e1f4e",
        "d01a4a9c-b7bf-4cf6-bb98-c6d4b857f82b",
        "d02a2916-0269-4ee6-840d-cc6d1b4afb80",
        "d03a93de-60d1-42ab-a081-6e3d8f14ed43",
        "d04ae236-0ddf-4f43-96f0-1a053f6d1621",
        "d05a3b86-eb95-4367-88f9-11151a8fa47f",
        "d06ab787-dce8-423e-91cb-25779dd32ed5",
        "d07abf1a-27bc-4ef7-a113-fcd64002b6fc",
        "d08a7efc-c874-4387-bb96-615f6c684825",
        "d09aa471-b946-4b32-83ee-dc2180f49baf",
        "d10a6579-732a-481d-89e7-6891700b51c5",
        "d11af506-c421-4ab1-8ef4-d19c05f705f8",
        "d12a2ecb-b44e-49ba-826b-4ef7a91bc0eb",
        "d13a5505-aead-467f-9bd3-fd52e36fd461",
        "d14acdd6-7dd3-4fa8-a4e6-a3361229dcac",
        "d15a6984-d9eb-4655-9f57-39bd7b46011a",
        "d16b5a3e-3224-407d-824e-1a233ff56cae"
    ]

    for folder in target_folders:
        folder_path = os.path.join(root_folder, folder)

        if not os.path.isdir(folder_path):
            print(f"Skipping missing folder: {folder_path}")
            continue

        for file in os.listdir(folder_path):
            if file.endswith(".xml"):
                file_path = os.path.join(folder_path, file)

                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()

                    for card in root.findall(".//card"):
                        card_id = card.get("id")
                        card_name = card.get("name")

                        if card_id and card_name:
                            result.append({
                                "id": card_id,
                                "name": card_name
                            })

                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Extraction complete. JSON saved as {output_file}")


root_folder = r"C:\Users\Daniel\AppData\Local\Programs\OCTGN\Data\GameDatabase\bb784fc6-fe21-4603-90d7-82c049908a74\Sets"
output_file = r"C:\Users\Daniel\Desktop\card_ids.json"

extract_card_ids(root_folder, output_file)