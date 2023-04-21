from pathlib import Path
from catprompt.prompter import process_and_copy_to_clipboard
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
