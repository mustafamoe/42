import os
import site
import sys


def is_virtual_environment() -> bool:
    # Old virtualenv sets real_prefix; modern venv changes sys.prefix.
    return (
        hasattr(sys, "real_prefix")
        or sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    )


def environment_path() -> str:
    # VIRTUAL_ENV exists after activation; sys.prefix works as a fallback.
    return os.environ.get("VIRTUAL_ENV", sys.prefix)


def environment_name(path: str) -> str:
    # Keep only the final folder name, for example matrix_env.
    name = os.path.basename(path)
    if name:
        return name
    return path


def default_site_packages(prefix: str) -> str:
    if os.name == "nt":
        # Windows venvs store packages in Lib/site-packages.
        return os.path.join(prefix, "Lib", "site-packages")

    # Unix venvs include the Python version in the package path.
    version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    return os.path.join(prefix, "lib", version, "site-packages")


def detected_site_packages() -> list[str]:
    # Ask Python for package locations, then fall back for limited installs.
    try:
        return site.getsitepackages()
    except (AttributeError, OSError):
        user_site = site.getusersitepackages()
        if user_site:
            return [user_site]
        return []


def current_site_packages() -> str:
    # Prefer detected paths; compute the common layout only if needed.
    locations = detected_site_packages()
    if locations:
        return locations[0]
    return default_site_packages(sys.prefix)


def global_site_packages() -> str:
    # base_prefix points back to the original/global Python install.
    base_prefix = getattr(sys, "base_prefix", sys.prefix)
    return default_site_packages(base_prefix)


def show_outside_matrix() -> None:
    print("Outside the Matrix")
    print("$> python construct.py")
    print("MATRIX STATUS: You're still plugged in")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print("Global package installation path:")
    print(global_site_packages())
    print("A virtual environment keeps packages in its own site-packages.")
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print(r"matrix_env\Scripts\activate # On Windows")
    print("Then run this program again.")


def show_inside_construct() -> None:
    path = environment_path()

    print("Inside the Construct")
    print("$> python construct.py")
    print("MATRIX STATUS: Welcome to the construct")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {environment_name(path)}")
    print(f"Environment Path: {path}")
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print("Package installation path:")
    print(current_site_packages())
    print("Global package installation path:")
    print(global_site_packages())


def main() -> None:
    if is_virtual_environment():
        show_inside_construct()
    else:
        show_outside_matrix()


if __name__ == "__main__":
    main()
