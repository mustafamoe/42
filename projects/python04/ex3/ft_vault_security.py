def secure_archive(
    file_name: str,
    action: str = "read",
    content: str = "",
) -> tuple[bool, str]:
    try:
        if action == "read":
            with open(file_name, "r") as archive_file:
                return True, archive_file.read()
        if action == "write":
            with open(file_name, "w") as archive_file:
                archive_file.write(content)
            return True, "Content successfully written to file"
        return False, f"Unknown archive action: '{action}'"
    except Exception as error:
        return False, str(error)


def main() -> None:
    sample_content = (
        "[FRAGMENT 001] Digital preservation protocols established 2087\n"
        "[FRAGMENT 002] Knowledge must survive the entropy wars\n"
        "[FRAGMENT 003] Every byte saved is a victory against oblivion\n"
    )

    print("=== Cyber Archives Security ===")

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd"))

    print("Using 'secure_archive' to read from a regular file:")
    success, content = secure_archive("ancient_fragment.txt")
    if not success:
        secure_archive("ancient_fragment.txt", "write", sample_content)
        success, content = secure_archive("ancient_fragment.txt")
    print((success, content))

    print("Using 'secure_archive' to write previous content to a new file:")
    print(secure_archive("new_fragment.txt", "write", content))


if __name__ == "__main__":
    main()
