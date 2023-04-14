import sys
import os
from pathlib import Path
import clipboard


def process_line(line, base_dir, processed_lines):
    if line.startswith('++'):
        return
    elif line.startswith('+='):
        file_to_include = line[2:].strip()
        file_path = base_dir / file_to_include
        if not file_path.is_file():
            file_path = Path(file_to_include)
        if file_path.is_file():
            process_file(file_path, processed_lines)
    elif line.startswith('+#'):
        return False
    else:
        processed_lines.append(line)


def process_file(file_path, processed_lines=None):
    if processed_lines is None:
        processed_lines = []
    base_dir = file_path.parent
    with file_path.open() as f:
        for line in f:
            line = line.rstrip()
            should_stop = process_line(line, base_dir, processed_lines)
            if should_stop is False:
                break
    return processed_lines


def process_and_copy_to_clipboard(file_path):
    processed_lines = process_file(file_path)
    processed_content = "\n".join(filter(None, processed_lines))
    clipboard.copy(processed_content)
    return processed_content


def main():
    if len(sys.argv) != 2:
        print("Usage: python catprompt.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    file_path = Path(input_file)

    if not file_path.is_file():
        print(f"Error: '{input_file}' not found.")
        sys.exit(1)

    process_and_copy_to_clipboard(file_path)
    print("Processed content copied to clipboard.")


if __name__ == "__main__":
    main()
