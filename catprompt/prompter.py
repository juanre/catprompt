# -*- coding: utf-8 -*-

import sys
import os
import argparse
import configparser
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
            f"{description} follows delimited by ```",
            "```",
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
        processed_lines.append("```")


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


def read_config_files(config_files):
    config = configparser.ConfigParser()

    for config_file in config_files:
        if os.path.exists(config_file):
            config.read(config_file)

    private_words = []
    if config.has_section("PrivateWords"):
        private_words = [word.strip() for word in config.get("PrivateWords", "list").split(',')]

    flavors = {}
    if config.has_section("Flavors"):
        for key in config.options("Flavors"):
            flavors[key] = config.get("Flavors", key).replace("\\n", "\n")

    return private_words, flavors


def replace_private_words(content, private_words):
    replacement_map = {}
    for word in private_words:
        if word not in replacement_map:
            replacement_map[word] = f"private{len(replacement_map)}"

        content = content.replace(word, replacement_map[word])

    return content


def reverse_private_words(content, private_words):
    replacement_map = {}
    for word in private_words:
        if word not in replacement_map:
            replacement_map[word] = f"private{len(replacement_map)}"

    reversed_map = {v: k for k, v in replacement_map.items()}

    for key, value in reversed_map.items():
        content = content.replace(key, value)

    return content


def main():
    parser = argparse.ArgumentParser(
        description="Process text files and copy processed content to the clipboard")
    parser.add_argument("input_files", metavar="input_file", type=str, nargs="*",
                        help="Input file(s) to process")
    parser.add_argument("-c", "--config", metavar="config_file", type=str, nargs="*",
                        default=[os.path.expanduser("~/.catprompt.ini"), "catprompt.ini"],
                        help=("Configuration file(s) containing private words and "
                              "flavors: (default: ~/.catprompt.ini and ./catprompt.ini)"))
    parser.add_argument("-r", "--reverse", metavar="reverse_file", type=str,
                        help=("Reverse the privatization from a given file and output "
                              "the original content to stdout"))
    parser.add_argument("-f", "--flavor", metavar="flavor", type=str,
                        help=("The flavor to use to prefix the output, extracted"
                              "from the config file file"))

    args = parser.parse_args()

    if not args.input_files and not args.reverse:
        print("Error: No input files or reverse file specified.")
        sys.exit(1)

    config_files = args.config

    private_words, flavors = read_config_files(config_files)

    flavor_text = ""
    if args.flavor:
        flavor = args.flavor.lower()
        if flavor not in flavors:
            print(f"Error: Flavor '{args.flavor}' not found in the configuration files.")
            sys.exit(1)
        flavor_text = flavors[flavor]

    if args.reverse:
        with open(args.reverse, "r", encoding='utf-8') as reverse_file:
            content = reverse_file.read()
            original_content = reverse_private_words(content, private_words)
            print(original_content)
            return

    input_files = args.input_files
    processed_lines = []

    for input_file in input_files:
        file_path = Path(input_file)
        if not file_path.is_file():
            print(f"Error: '{input_file}' not found.")
            sys.exit(1)
        print(f'Reading {input_file}')
        process_file(file_path, processed_lines)

    processed_content = "\n".join(filter(None, processed_lines))
    processed_content = flavor_text + '\n\n' + \
        replace_private_words(processed_content, private_words)
    clipboard.copy(processed_content)

    encoding = 'cl100k_base'
    tokenizer = tiktoken.get_encoding(encoding)
    tokens = tokenizer.encode(processed_content)
    print(f"Processed content copied to clipboard, {len(tokens)} {encoding} tokens")


if __name__ == "__main__":
    main()
