# Python Module 04 Notes

## Big idea

This module is about file operations and streams.

The main goal is to open text files, read their contents, write new files, handle
errors, and close resources correctly.

Important rule from the subject:

Do not use `with open(...)` before exercise 3.

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

Important lesson:

Opening a file with `"w"` creates it if it does not exist and replaces its content if it
already exists.

## Exercise 2: Stream Management

File: `ex2/ft_stream_management.py`

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
output_name = sys.stdin.readline().rstrip("\n")
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

## Exercise 3: Vault Security

File: `ex3/ft_vault_security.py`

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
