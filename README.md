# catprompt


`catprompt` is a command-line tool that simplifies the process of combining prompts in different files for programming with ChatGPT. It allows users to define a system prompt along with several functionality-specific prompts, which may include files with code, into a single prompt. The prompt files can be part of the project and later be used as the seed for documentation.

## Usage

1. Install catprompt
2. Create your prompt files
3. Run catprompt with the main prompt file as a command-line argument
4. Use the processed content from the clipboard

## Installation

: pip install catprompt

## Prompt file format

- Lines starting with `++` are ignored
- Lines starting with `+=` should be followed by the name of a file to include. The file will be searched for in the directory of the original file, or in the working directory if not found there. The named file will be read, processed, and its content will replace the current line.
- Lines starting with `+#` will cause the current line and all following lines in the file being processed to be ignored

### Example

Let's consider the following example with three files:

**main_prompt.txt**

```
This is the main prompt.

++ This is a comment and will be ignored.
+= sub_prompt_1.txt
+= code_snippet.py

This is the end of the main prompt.
```

**sub_prompt_1.txt**

```
This is the sub-prompt 1.
+# Ignore the rest of this file
This line will be ignored.

This is useful to record the prompt that you used with this file,  which
you probably don't want when the file is included by another file
```

**code_snippet.py**

```python
def example_function():
    return "This is an example code snippet."
```

When running `catprompt main_prompt.txt`, the processed content will be:

```
This is the main prompt.
This is the sub-prompt 1.
def example_function():
    return "This is an example code snippet."
This is the end of the main prompt.
```

This processed content will be copied to your clipboard, ready for use with ChatGPT.

## Use cases

- Combining a system prompt with functionality-specific prompts;
- Including code snippets in your prompts;
- Organizing prompt files as part of a project;
- Using prompt files as the seed for documentation.

## Developing

```
mkdir ~/venv/catp && python3.9 -m venv ~/venv/catp
source ~/venv/catp/bin/activate
pip install --upgrade pip
pip install -e .
pip install ".[dev]"
```
