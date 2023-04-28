# catprompt

`catprompt` is a command-line tool that simplifies the process of combining prompts in different files for programming with ChatGPT. It allows users to define a system prompt along with several functionality-specific prompts, which may include files with code, into a single prompt. The prompt files can be part of the project and later be used as the seed for documentation.

Using `catprompt` when developing a large program with ChatGPT offers several advantages:

1. **System prompt consistency:** By having a central system prompt, you can ensure that essential information or context is consistently provided to ChatGPT across different parts of your project. This helps maintain uniformity and coherence in the responses generated by ChatGPT.

2. **Modularity:** `catprompt` allows you to divide prompts into separate files, enabling better organization of your project and keeping related prompts together. This makes it easier to maintain and update the code, as each functionality-specific prompt can be managed independently.

3. **Reusability:** With `catprompt`, you can reuse prompts or code snippets across different parts of the project, avoiding duplication and improving consistency.

4. **Collaboration:** Separating prompts into different files allows multiple team members to work on different aspects of the project simultaneously, without causing conflicts or requiring constant synchronization.

5. **Documentation:** The prompt files can serve as a foundation for your project's documentation, making it easier to keep the documentation up-to-date and in sync with the code.

## Usage

1. Install catprompt
2. Create your prompt files
3. Run catprompt with the main prompt file[s] as a command-line argument:

`catprompt path/to/prompt.txt [path/to/other-prompts.txt]`

4. Use the processed content from the clipboard

## Installation

`pip install catprompt`

or

1. Visit the homepage at https://github.com/juanre/catprompt
2. Download the package as a ZIP file or clone the repository using git
3. Navigate to the downloaded folder in your command-line interface
4. Run `pip install .` to install the package

Make sure you have `pip` installed on your system. If not, you can find instructions on how to install pip here: https://pip.pypa.io/en/stable/installation/

## Prompt file format

- Lines starting with `++` are ignored
- Lines starting with `+=` should be followed by the name of a file to include. The file will be searched for in the directory of the original file, or in the working directory if not found there. The named file will be read, processed, and its content will replace the current line.
- Lines starting with `+-` should be followed by the name of a file to include, and a description. The file will processed as above, and its content prefaced by a line saying "[description] follows delimited by +-----" and another line with just +-----, and followed by a line with +-----
- Lines starting with `+#` will cause the current line and all following lines in the file being processed to be ignored
- Segments of a file can be tagged by adding a line that contains :prompt:tag at the beginning, and :/prompt:tag at the end. Include them by adding [tag] after the file name.

### Example

Let's consider the following example with three files:

**main-prompt.txt**

```
This is the main prompt.

++ This is a comment and will be ignored.
+= sub-prompt-1.txt
+- code-snippet.py The snippet of code
+- code-snippet.py [tag-1] The snippet of code limited to tag-1

This is the end of the main prompt.
```

**sub-prompt-1.txt**

```
This is the sub-prompt 1.
+# Ignore the rest of this file
This line will be ignored.

This is useful to record the prompt that you used with this file,  which
you probably don't want when the file is included by another file
```

**code-snippet.py**

```python
def example_function_1():
    return "F1"

# :prompt:tag-1
def example_function_2():
    return "F2"
# :/prompt:tag-1

def example_function_3():
    return "F3"

# :prompt:tag-1
def example_function_4():
    return "F4"
# :/prompt:tag-1
```

When running `catprompt main-prompt.txt`, the processed content will be:

```
This is the main prompt.
This is the sub-prompt 1.
The snippet of code follows delimited by +-----
+-----
def example_function_1():
    return "F1"
# :prompt:tag-1
def example_function_2():
    return "F2"
# :/prompt:tag-1
def example_function_3():
    return "F3"
# :prompt:tag-1
def example_function_4():
    return "F4"
# :/prompt:tag-1
+-----
The snippet of code limited to tag-1 follows delimited by +-----
+-----
def example_function_2():
    return "F2"
def example_function_4():
    return "F4"
+-----
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
mkdir ~/venv/catp && python -m venv ~/venv/catp
source ~/venv/catp/bin/activate
pip install --upgrade pip
pip install -e .
pip install ".[dev]"
```

## Author

ChatGPT-4, with prompting and editing help by Juan Reyero.
