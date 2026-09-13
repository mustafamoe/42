import sys
import typing


def display_block(content: str) -> None:
    print("---")
    print(content, end="")
    if content and not content.endswith("\n"):
        print()
    print("---")


def print_error(message: str) -> None:
    sys.stdout.flush()
    sys.stderr.write(f"[STDERR] {message}\n")
    sys.stderr.flush()


def read_archive(file_name: str) -> str | None:
    print(f"Accessing file '{file_name}'")

    archive_file: typing.IO[str] | None = None
    try:
        archive_file = open(file_name, "r")
        content = archive_file.read()
        display_block(content)
        return content
    except Exception as error:
        print_error(f"Error opening file '{file_name}': {error}")
        return None
    finally:
        if archive_file is not None:
            archive_file.close()
            print(f"File '{file_name}' closed.")


def add_archive_markers(content: str) -> str:
    transformed = content.replace("\n", "#\n")
    if content and not content.endswith("\n"):
        transformed += "#"
    return transformed


def display_transformed_data(content: str) -> None:
    print("Transform data:")
    display_block(content)


def read_output_name() -> str:
    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    return sys.stdin.readline().rstrip("\r\n")


def save_archive(file_name: str, content: str) -> None:
    print(f"Saving data to '{file_name}'")

    archive_file: typing.IO[str] | None = None
    try:
        archive_file = open(file_name, "w")
        archive_file.write(content)
    except Exception as error:
        print_error(f"Error opening file '{file_name}': {error}")
        print("Data not saved.")
        return
    finally:
        if archive_file is not None:
            archive_file.close()
    print(f"Data saved in file '{file_name}'.")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>")
        return

    print("=== Cyber Archives Recovery & Preservation ===")
    content = read_archive(sys.argv[1])
    if content is None:
        return

    transformed = add_archive_markers(content)
    display_transformed_data(transformed)

    output_name = read_output_name()
    if output_name == "":
        print("Not saving data.")
    else:
        save_archive(output_name, transformed)


if __name__ == "__main__":
    main()
