# -*- coding: utf-8 -*-

import sys
from pathlib import Path
import clipboard
import tiktoken


# pylint: disable=inconsistent-return-statements
def process_line(line, base_dir, processed_lines):
    if line.startswith('++'):
        return
    if line.startswith('+=') or line.startswith('+-'):
        file_to_include, tag, description = parse_file_and_tag(line)
        file_path = base_dir / file_to_include
        if not file_path.is_file():
            file_path = Path(file_to_include)
        if file_path.is_file():
            print(f'Inserting {str(file_path)}')
            process_included_file(file_path, tag, processed_lines,
                                  with_delimiter=line.startswith('+-'),
                                  description=description)
        else:
            raise RuntimeError(f'Cannot find {file_to_include}')
    elif line.startswith('+#'):
        return False
    else:
        processed_lines.append(line)


def parse_file_and_tag(line):
    file_and_tag = line[2:].strip().split(maxsplit=1)
    file_to_include = file_and_tag[0].strip()
    tag = None
    description = None
    if len(file_and_tag) > 1:
        if '[' in file_and_tag[1]:
            tag_start = file_and_tag[1].index('[')
            tag_end = file_and_tag[1].index(']')
            tag = file_and_tag[1][tag_start+1:tag_end].strip()
            if line.startswith('+-'):
                description = (file_and_tag[1][:tag_start].strip() +
                               file_and_tag[1][tag_end+1:].strip())
        else:
            if line.startswith('+-'):
                description = file_and_tag[1].strip()
    return file_to_include, tag, description


def process_included_file(file_path, tag, processed_lines, with_delimiter, description=None):
    base_dir = file_path.parent
    include = not tag
    tag_start = f":prompt:{tag}"
    tag_end = f":/prompt:{tag}"
    if with_delimiter:
        description = description if description else file_path.name
        processed_lines.extend([
            f"{description} follows delimited by +-----",
            "+-----",
        ])

    with file_path.open() as f:
        for line in f:
            line = line.rstrip()
            if tag and tag_start in line:
                include = True
                continue
            if tag and tag_end in line:
                include = False
                continue
            if include:
                should_stop = process_line(line, base_dir, processed_lines)
                if should_stop is False:
                    break

    if with_delimiter:
        processed_lines.append("+-----")


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
    if len(sys.argv) < 2:
        print("Usage: catprompt <input_file> [<input_files>]")
        sys.exit(1)

    input_files = sys.argv[1:]
    processed_lines = []

    for input_file in input_files:
        file_path = Path(input_file)

        if not file_path.is_file():
            print(f"Error: '{input_file}' not found.")
            sys.exit(1)

        print(f'Reading {input_file}')
        process_file(file_path, processed_lines)

    processed_content = "\n".join(filter(None, processed_lines))
    clipboard.copy(processed_content)

    encoding = 'cl100k_base'
    tokenizer = tiktoken.get_encoding(encoding)
    tokens = tokenizer.encode(processed_content)
    print(f"Processed content copied to clipboard, {len(tokens)} {encoding} tokens")


if __name__ == "__main__":
    main()
