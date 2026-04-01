import os
import shutil

# Path to the folder that currently holds all the sets
SOURCE_DIR = "Sets"  # Change this if your folder name is different
# Path to the destination folder for your Vue app
DEST_DIR = "webapp/public/assets/cards"

# Create the destination folder if it doesn't exist
os.makedirs(DEST_DIR, exist_ok=True)

# Counter
copied = 0
skipped = 0

# Walk through all subfolders recursively
for root, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        if file.lower().endswith(".jpg"):
            src_path = os.path.join(root, file)
            dest_path = os.path.join(DEST_DIR, file)

            # Skip if file with same name already exists
            if os.path.exists(dest_path):
                print(f"Skipped (exists): {file}")
                skipped += 1
                continue

            try:
                shutil.copy2(src_path, dest_path)
                copied += 1
                print(f"Copied: {file}")
            except Exception as e:
                print(f"Error copying {file}: {e}")

print(f"\n✅ Done. {copied} images copied, {skipped} skipped.")
print(f"All images now in: {os.path.abspath(DEST_DIR)}")
