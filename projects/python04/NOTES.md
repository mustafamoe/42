# Python Module 04 Notes

## Big idea

This module is about file operations and streams.

The main goal is to open text files, read their contents, write new files, handle
errors, and close resources correctly.

Subject files:

- `en.subject.pdf`
- `en.subject.txt`

Common requirements:

- Use Python 3.10 or later.
- Pass `flake8`.
- Add type hints to all functions and methods and pass `mypy`.
- Handle exceptions gracefully.
- Only repository content is evaluated.
- Do not use `with open(...)` before exercise 3.
- Standard types and collections are allowed with their methods and constructors:
  `str`, `int`, `float`, `list`, `dict`, `set`, and `tuple`.

Important rule from the subject:

Do not use `with open(...)` before exercise 3.

Subject compliance:

Exercises 0, 1, and 2 manually close opened files. Exercise 3 is the first and only
exercise in this module that uses `with open(...)`.

## Useful functions and objects

`open(file_name, "r")` opens a file for reading.

`open(file_name, "w")` opens a file for writing. It creates the file if needed and
replaces the file if it already exists.

`read()` returns the file content as a string.

`write(content)` writes a string to a file.

`close()` closes the file object and releases the resource.

`typing.IO[str]` is used as a type hint for a text file object.

## Exercise 0: Ancient Text Recovery

File: `ex0/ft_ancient_text.py`

Authorized:

- `import sys`
- `sys.argv`
- `len()`
- `open()`
- `import typing`
- `typing.IO`
- file object `read()`
- file object `close()`
- `print()`

Not allowed / avoid:

- `with open(...)`
- `input()`
- direct use of `sys.stdin`, `sys.stdout`, or `sys.stderr`
- writing files

Idea:

Read a file name from the command line and display the file content like `cat`, with
extra archive headers and footers.

Useful pattern:

```python
archive_file = open(file_name, "r")
content = archive_file.read()
archive_file.close()
```

The exercise teaches:

- Get the file name from `sys.argv`
- Open a file in read mode
- Read all text from a file
- Catch errors for missing or inaccessible files
- Close the file when it was opened successfully

Important lesson:

`open()` returns a file object. In this project, it is type hinted as `typing.IO[str]`
because the files are opened as text.

## Exercise 1: Archive Creation

File: `ex1/ft_archive_creation.py`

Authorized:

- `import sys`
- `sys.argv`
- `len()`
- `open()`
- `import typing`
- `typing.IO`
- file object `read()`
- file object `write()`
- file object `close()`
- `print()`
- `input()`

Not allowed / avoid:

- `with open(...)`
- direct use of `sys.stdin`, `sys.stdout`, or `sys.stderr`

Idea:

Reuse the reading logic from exercise 0, then create a transformed version of the text
by adding `#` at the end of each line.

Example transformation:

```text
hello
world
```

becomes:

```text
hello#
world#
```

The exercise teaches:

- Reuse file-reading code
- Transform a string before saving it
- Ask the user for an output file name with `input()`
- Open a file in write mode
- Write new content to the file
- Treat end-of-file at the prompt like an empty answer

Important lesson:

Opening a file with `"w"` creates it if it does not exist and replaces its content if it
already exists.

## Exercise 2: Stream Management

File: `ex2/ft_stream_management.py`

Authorized:

- `import sys`
- `sys.argv`
- `sys.stdin`
- `sys.stdout`
- `sys.stderr`
- `len()`
- `open()`
- `import typing`
- `typing.IO`
- file object `read()`
- stream/file object `readline()`
- stream/file object `write()`
- stream/file object `flush()`
- file object `close()`
- `print()`

Not allowed / avoid:

- `with open(...)`
- `input()`
- printing exception messages to standard output

Idea:

Use the three standard streams directly:

- `sys.stdin` for input
- `sys.stdout` for normal output
- `sys.stderr` for error output

This exercise keeps the same archive transformation from exercise 1, but replaces
`input()` with `sys.stdin.readline()`.

Useful pattern:

```python
sys.stdout.write("Enter new file name (or empty): ")
sys.stdout.flush()
output_name = sys.stdin.readline().rstrip("\r\n")
```

Errors are written to `stderr`:

```python
sys.stderr.write("[STDERR] Error message\n")
sys.stderr.flush()
```

The exercise teaches:

- Standard output and standard error are different channels
- Error messages should not always go to normal output
- `flush()` forces buffered text to appear immediately
- `readline()` reads one line from standard input

Important lesson:

Use `stderr` for errors so normal output can be separated from problem messages.
The prompt strips line endings only, so spaces inside a file name are preserved.

Gotcha:

Exercise 2 must not use `input()`. It reads from `sys.stdin.readline()` and writes the
prompt through `sys.stdout.write()`.

## Exercise 3: Vault Security

File: `ex3/ft_vault_security.py`

Authorized:

- `open()`
- `read()`
- `write()`
- `print()`

Required / allowed:

- Use `with open(...)`.
- Create `secure_archive()`.
- Return `(True, str)` on success and `(False, str)` on failure.
- Accept a mandatory file name, an optional action, and optional write content.

Not allowed / avoid:

- Crashing on file errors.
- Reusing the manual close pattern from exercises 0, 1, and 2.

Idea:

Create `secure_archive()` to safely read or write a file and return a result tuple:

```python
(True, "file content or success message")
(False, "error message")
```

This is the only exercise where `with open(...)` is required.

Useful pattern:

```python
with open(file_name, "r") as archive_file:
    return True, archive_file.read()
```

The exercise teaches:

- Use a context manager for automatic cleanup
- Return information instead of crashing
- Support both read and write actions in one function
- Use a boolean to tell whether the operation succeeded

Important lesson:

`with open(...)` closes the file automatically, even if an exception happens while the
file is being used.

The script demonstration creates `ancient_fragment.txt` only if it is missing, so the
regular-file example works without overwriting a provided sample file.

## Module summary

```text
ex0: open, read, close, and handle file errors
ex1: transform text and write a new file
ex2: use stdin, stdout, and stderr directly
ex3: use with open(...) for safe file access
```

Short version:

This module teaches how to work with files safely and how to separate normal program
output from error messages.

## Checks

```sh
python3.10 -m flake8 projects/python04
python3.10 -m mypy projects/python04
```
