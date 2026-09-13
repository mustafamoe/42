import alchemy


def main() -> None:
    print("=== Alembic 4 ===", flush=True)
    print("Accessing the alchemy module using 'import alchemy'", flush=True)
    print(f"Testing create_air: {alchemy.create_air()}", flush=True)
    print("Now show that not all functions can be reached", flush=True)
    print("This will raise an exception!", flush=True)
    print(
        "Testing the hidden create_earth: "
        f"{getattr(alchemy, 'create_earth')()}"
    )


if __name__ == "__main__":
    main()
