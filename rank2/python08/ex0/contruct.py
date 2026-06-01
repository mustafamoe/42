import os # interacts operating system
import site # gives info about where packages are installed
import sys #gives info about the python interpreter


def is_virtual_environment() -> bool:
    # sys.prefix = /home/usr/matrix_env and sys.base_prefix = /usr
    # if both equals then out side venv
    # if both not equal then inside venv
    return (
        sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    )


def environment_path() -> str:
    # VIRTUAL_ENV exists after activation; sys.prefix works as a fallback.
    #stores full path of virtual machine
    return os.environ.get("VIRTUAL_ENV", sys.prefix)


def environment_name(path: str) -> str:
    # Keep only the final folder name, for example matrix_env.
    # if there is no file at the end .../.../ (nothing) it will return whole path
    name = os.path.basename(path)
    if name:
        return name
    return path



def get_site_package():
    return site.getsitepackages()




def show_outside_matrix() -> None:
    print("Outside the Matrix")
    print("$> python construct.py")
    print("MATRIX STATUS: You're still plugged in")
    print(f"Current Python: {sys.executable}")  # same as which python3 (returns location where python3 exe. is located)
    print("Virtual Environment: None detected")
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print("Global package installation path:")
    print(get_site_package())
    print("A virtual environment keeps packages in its own site-packages.")
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print(r"matrix_env\Scripts\activate # On Windows")

    print("Then run this program again.")


def show_inside_construct() -> None:
    path = environment_path()

    print("$> python construct.py")
    # nl
    print("MATRIX STATUS: Welcome to the construct")
    # nl
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {environment_name(path)}")
    print(f"Environment Path: {path}")
    # nl
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    # nl
    print("Package installation path:")
    for pkg in get_site_package():
        print(pkg)


def main() -> None:
    if is_virtual_environment():
        show_inside_construct()
    else:
        show_outside_matrix()


if __name__ == "__main__":
    main()

