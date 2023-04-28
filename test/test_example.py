# -*- coding: utf-8 -*-

import os
from pathlib import Path
from catprompt.prompter import process_and_copy_to_clipboard
import clipboard


def test_example_file():
    # Prepare test data
    test_data_dir = Path(__file__).parent / "example"
    input_file = test_data_dir / "main-prompt.txt"
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
