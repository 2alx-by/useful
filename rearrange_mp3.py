from pathlib import Path
import shutil
import string

# Root directory to scan.
# "." means the current directory.
source_root = Path("e:\\Transfer\\Lvl2\\_").resolve()

# Destination base is one level above the source directory.
dest_base = source_root.parent

# Create destination folders.
for c in string.ascii_lowercase:
    (dest_base / c).mkdir(exist_ok=True)

for d in string.digits:
    (dest_base / d).mkdir(exist_ok=True)

(dest_base / "other").mkdir(exist_ok=True)

# Find all MP3 files recursively.
for mp3 in source_root.rglob("*.mp3"):
    first = mp3.name[0].lower()

    if first.isalpha():
        dest_dir = dest_base / first
    elif first.isdigit():
        dest_dir = dest_base / first
    else:
        dest_dir = dest_base / "other"

    dest_file = dest_dir / mp3.name

    # Avoid overwriting existing files.
    if dest_file.exists():
        stem = dest_file.stem
        suffix = dest_file.suffix
        counter = 1

        while True:
            candidate = dest_dir / f"{stem}_{counter}{suffix}"
            if not candidate.exists():
                dest_file = candidate
                break
            counter += 1

    print(f"Moving: {mp3} -> {dest_file}")
    shutil.move(str(mp3), str(dest_file))

print("Done.")
