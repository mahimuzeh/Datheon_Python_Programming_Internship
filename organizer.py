import os
import shutil
from pathlib import Path

# 1. Extension mapping dictionary
EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".xlsx": "Documents",
    ".csv": "Documents",
    ".pptx": "Documents",
    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".svg": "Images",
    ".webp": "Images",
    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".7z": "Archives",
    # Code
    ".py": "Code",
    ".js": "Code",
    ".html": "Code",
    ".css": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".json": "Code",
}


def get_unique_destination(dest_folder: Path, filename: str) -> Path:
    """Resolves naming collisions by appending a counter (e.g., file_1.pdf)."""
    dest_path = dest_folder / filename
    if not dest_path.exists():
        return dest_path

    stem = dest_path.stem
    suffix = dest_path.suffix
    counter = 1

    while dest_path.exists():
        dest_path = dest_folder / f"{stem}_{counter}{suffix}"
        counter += 1

    return dest_path


def organize_directory(target_dir: str):
    target_path = Path(target_dir).expanduser().resolve()

    if not target_path.is_dir():
        print(f"Error: '{target_path}' is not a valid directory.")
        return

    summary = {}
    total_moved = 0
    errors = 0

    # 2. Scan directory entries
    with os.scandir(target_path) as entries:
        for entry in entries:
            # Skip directories and the script itself if run inside target_dir
            if not entry.is_file() or entry.name == os.path.basename(__file__):
                continue

            file_path = Path(entry.path)
            ext = file_path.suffix.lower()

            # Determine category folder (defaults to 'Others' if unmapped)
            category = EXTENSION_MAP.get(ext, "Others")
            category_folder = target_path / category

            try:
                # 3. Dynamically create category subfolders
                category_folder.mkdir(exist_ok=True)

                # Handle naming collisions safely
                destination = get_unique_destination(category_folder, entry.name)

                # Relocate file
                shutil.move(str(file_path), str(destination))

                summary[category] = summary.get(category, 0) + 1
                total_moved += 1

            # 4. Catch permission and file existence exceptions
            except (PermissionError, FileExistsError, OSError) as e:
                print(f"[Skipped] Could not move '{entry.name}': {e}")
                errors += 1

    # 5. Print formatted execution summary
    print("\n" + "=" * 40)
    print(f"ORGANIZATION SUMMARY: {target_path}")
    print("=" * 40)
    if summary:
        for category, count in sorted(summary.items()):
            print(f"  {category:<15}: {count} file(s)")
    else:
        print("  No files needed moving.")
    print("-" * 40)
    print(f"  Total Relocated : {total_moved}")
    print(f"  Errors/Skipped  : {errors}")
    print("=" * 40 + "\n")


if __name__ == "__main__":
    # Example: Organize the user's Downloads folder
    downloads_folder = Path.home() / "Downloads"
    organize_directory(str(downloads_folder))
