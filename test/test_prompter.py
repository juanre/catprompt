# -*- coding: utf-8 -*-

import os
from pathlib import Path
from catprompt.prompter import process_and_copy_to_clipboard, replace_private_words
import clipboard


def test_process_file():
    # Prepare test data
    test_data_dir = Path(__file__).parent / "data"
    input_file = test_data_dir / "input.txt"
    expected_output_file = test_data_dir / "expected-output.txt"

    # Run process_file
    processed_content = process_and_copy_to_clipboard(input_file)

    # Compare the processed content with the expected output
    with expected_output_file.open() as f:
        expected_output = f.read().rstrip()
    assert processed_content == expected_output

    # Check if processed content was copied to clipboard
    clipboard_content = clipboard.paste()
    assert processed_content == clipboard_content


def test_process_file_with_stop():
    # Prepare test data
    test_data_dir = Path(__file__).parent / "data"
    input_file = test_data_dir / "input-with-stop.txt"
    expected_output_file = test_data_dir / "expected-output-with-stop.txt"

    # Run process_and_copy_to_clipboard
    processed_content = process_and_copy_to_clipboard(input_file)

    # Compare the processed content with the expected output
    with expected_output_file.open() as f:
        expected_output = f.read().rstrip()
    assert processed_content == expected_output

    # Check if processed content was copied to clipboard
    clipboard_content = clipboard.paste()
    assert processed_content == clipboard_content


def test_process_file_with_inline_content():
    # Prepare test data
    test_data_dir = Path(__file__).parent / "data"
    input_file = test_data_dir / "input-with-inline-content.txt"
    expected_output_file = test_data_dir / "expected-output-with-inline-content.txt"

    # Run process_and_copy_to_clipboard
    processed_content = process_and_copy_to_clipboard(input_file)

    # Compare the processed content with the expected output
    with expected_output_file.open() as f:
        expected_output = f.read().rstrip()
    print(processed_content)
    print(expected_output)
    assert processed_content == expected_output

    # Check if processed content was copied to clipboard
    clipboard_content = clipboard.paste()
    assert processed_content == clipboard_content


def test_process_file_with_tags_and_equals():
    # Prepare test data
    test_data_dir = Path(os.path.dirname(os.path.abspath(__file__))) / "data"
    input_file = test_data_dir / "input-with-tags-and-equals.txt"
    expected_output_file = test_data_dir / "expected-output-with-tags-and-equals.txt"

    # Run process_and_copy_to_clipboard
    processed_content = process_and_copy_to_clipboard(input_file)
    print(processed_content)
    print()

    # Compare the processed content with the expected output
    with expected_output_file.open() as f:
        expected_output = f.read().rstrip()
        print(expected_output)
    assert processed_content == expected_output


def test_process_file_with_tags_and_minus():
    # Prepare test data
    test_data_dir = Path(os.path.dirname(os.path.abspath(__file__))) / "data"
    input_file = test_data_dir / "input-with-tags-and-minus.txt"
    expected_output_file = test_data_dir / "expected-output-with-tags-and-minus.txt"

    # Run process_and_copy_to_clipboard
    processed_content = process_and_copy_to_clipboard(input_file)

    # Compare the processed content with the expected output
    with expected_output_file.open() as f:
        expected_output = f.read().rstrip()
    assert processed_content == expected_output


def test_replace_private_words():
    content = "This is a test with some privateWord1 and privateWord2."
    private_words = ["privateWord1", "privateWord2"]

    expected_output = "This is a test with some private0 and private1."
    output = replace_private_words(content, private_words)

    assert output == expected_output
