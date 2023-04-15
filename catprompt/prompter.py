# -*- coding: utf-8 -*-

import sys
from pathlib import Path
import clipboard
import tiktoken


# pylint: disable=inconsistent-return-statements
def process_line(line, base_dir, processed_lines):
    if line.startswith('++'):
        return

    if line.startswith('+='):
        file_to_include = line[2:].strip()
        file_path = base_dir / file_to_include
        if not file_path.is_file():
            file_path = Path(file_to_include)
        if file_path.is_file():
            print(f'Including {str(file_path)}')
            process_file(file_path, processed_lines)
        else:
            raise RuntimeError(f'Cannot find {file_to_include}')
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
        print("Usage: catprompt <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    file_path = Path(input_file)

    if not file_path.is_file():
        print(f"Error: '{input_file}' not found.")
        sys.exit(1)

    processed_content = process_and_copy_to_clipboard(file_path)
    encoding = 'cl100k_base'
    tokenizer = tiktoken.get_encoding(encoding)
    tokens = tokenizer.encode(processed_content)
    print(f"Processed content copied to clipboard, {len(tokens)} {encoding} tokens")


if __name__ == "__main__":
    main()
