import sys
import typing


def display_block(content: str) -> None:
    print("---")
    print(content, end="")
    if content and not content.endswith("\n"):
        print()
    print("---")


def display_file(file_name: str) -> None:
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{file_name}'")

    archive_file: typing.IO[str] | None = None
    try:
        archive_file = open(file_name, "r")
        content = archive_file.read()
        display_block(content)
    except Exception as error:
        print(f"Error opening file '{file_name}': {error}")
    finally:
        if archive_file is not None:
            archive_file.close()
            print(f"File '{file_name}' closed.")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return
    display_file(sys.argv[1])


if __name__ == "__main__":
    main()
