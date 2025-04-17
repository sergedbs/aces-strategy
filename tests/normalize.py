import re
import unicodedata
from pathlib import Path
import keyword
import sys

# Add the root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

def normalize_name(name: str) -> str:
    """
    Normalizes a string to be a valid Python identifier.
    - Converts to lowercase.
    - Inserts underscores before capitals in camel/pascal case (e.g., CamelCase -> camel_case).
    - Handles acronyms correctly (e.g., HTTPRequest -> http_request).
    - Replaces spaces and hyphens with underscores.
    - Removes accents and non-ASCII characters.
    - Removes other invalid characters.
    - Prepends '_' if it starts with a digit.
    - Appends '_' if it's a Python keyword.
    """
    # 1. Handle potential non-string input gracefully
    if not isinstance(name, str):
        name = str(name)

    # 2. Normalize Unicode characters (handle accents first)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')

    # 3. Insert underscores before capitals in camel/pascal case
    #    Handles cases like CamelCase -> Camel_Case, camelCase -> camel_Case
    #    Handles acronyms followed by PascalCase like HTTPRequest -> HTTP_Request
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name) # ABCDef -> ABC_Def
    name = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', name)    # abcDef -> abc_Def, a1Def -> a1_Def

    # 4. Replace spaces and hyphens with underscores
    name = name.replace(' ', '_').replace('-', '_')

    # 5. Convert to lowercase
    name = name.lower()

    # 6. Remove any character that is not a lowercase letter, digit, or underscore
    name = re.sub(r'[^a-z0-9_]+', '', name)

    # 7. Collapse multiple consecutive underscores into one
    name = re.sub(r'_+', '_', name)

    # 8. Remove leading/trailing underscores
    name = name.strip('_')

    # 9. Prepend underscore if it starts with a digit
    if name and name[0].isdigit():
        name = '_' + name # Corrected variable name

    # 10. Append underscore if it's a Python keyword
    if keyword.iskeyword(name):
        name += '_'

    # 11. Handle empty string case
    if not name:
        return "_invalid_name"

    return name

def rename_strategy_files(folder: str | Path = "strategies"):
    """
    Renames .py files in the specified folder according to normalization rules.
    """
    strategies_path = Path(folder)
    if not strategies_path.is_dir():
        print(f"Error: Folder '{folder}' not found.")
        return

    print(f"Scanning folder: {strategies_path.resolve()}")
    renamed_count = 0
    skipped_count = 0
    potential_conflicts = {} # Track target names to avoid overwriting

    # First pass: determine target names and check for conflicts
    files_to_rename = {}
    for file_path in strategies_path.glob("*.py"):
        if file_path.name == "__init__.py":
            continue

        original_stem = file_path.stem
        new_stem = normalize_name(original_stem)
        new_filename = new_stem + ".py"

        if file_path.name == new_filename:
            # print(f"Skipping '{file_path.name}' (already normalized).")
            continue

        if new_filename in potential_conflicts:
            print(f"Conflict detected: Both '{potential_conflicts[new_filename]}' and '{file_path.name}' would rename to '{new_filename}'. Skipping '{file_path.name}'.")
            skipped_count += 1
        else:
            potential_conflicts[new_filename] = file_path.name
            files_to_rename[file_path] = strategies_path / new_filename

    # Second pass: perform renaming if no conflicts were found for a file
    if not files_to_rename:
        print("No files need renaming.")
        return

    print("\n--- Proposed Renames ---")
    for old_path, new_path in files_to_rename.items():
         print(f"'{old_path.name}' -> '{new_path.name}'")

    confirm = input("\nProceed with renaming? (yes/no): ").lower()
    if confirm == 'yes':
        print("\n--- Renaming Files ---")
        for old_path, new_path in files_to_rename.items():
            try:
                old_path.rename(new_path)
                print(f"Renamed '{old_path.name}' to '{new_path.name}'")
                renamed_count += 1
            except OSError as e:
                print(f"Error renaming '{old_path.name}' to '{new_path.name}': {e}")
                skipped_count += 1
        print(f"\nFinished: {renamed_count} files renamed, {skipped_count} files skipped.")
    else:
        print("Renaming cancelled.")


if __name__ == "__main__":
    # Assumes the script is run from the project root directory
    # or that the 'strategies' folder is in the current working directory.
    # Adjust the path if necessary.
    strategies_directory = root_dir / "strategies"
    rename_strategy_files(strategies_directory)