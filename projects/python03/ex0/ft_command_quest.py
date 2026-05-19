import sys


def main() -> None:
    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")
    if len(sys.argv) == 1:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(sys.argv) - 1}")
        index = 1
        while index < len(sys.argv):
            print(f"Argument {index}: {sys.argv[index]}")
            index += 1
    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    main()
