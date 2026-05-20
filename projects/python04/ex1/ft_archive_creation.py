import sys
import typing


def display_block(content: str) -> None:
    print("---")
    print(content, end="")
    if content and not content.endswith("\n"):
        print()
    print("---")


def read_archive(file_name: str) -> str | None:
    print(f"Accessing file '{file_name}'")

    archive_file: typing.IO[str] | None = None
    try:
        archive_file = open(file_name, "r")
        content = archive_file.read()
        display_block(content)
        return content
    except Exception as error:
        print(f"Error opening file '{file_name}': {error}")
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


def save_archive(file_name: str, content: str) -> None:
    print(f"Saving data to '{file_name}'")

    archive_file: typing.IO[str] | None = None
    try:
        archive_file = open(file_name, "w")
        archive_file.write(content)
        print(f"Data saved in file '{file_name}'.")
    except Exception as error:
        print(f"Error opening file '{file_name}': {error}")
        print("Data not saved.")
    finally:
        if archive_file is not None:
            archive_file.close()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    print("=== Cyber Archives Recovery & Preservation ===")
    content = read_archive(sys.argv[1])
    if content is None:
        return

    transformed = add_archive_markers(content)
    display_transformed_data(transformed)

    output_name = input("Enter new file name (or empty): ")
    if output_name == "":
        print("Not saving data.")
    else:
        save_archive(output_name, transformed)


if __name__ == "__main__":
    main()
