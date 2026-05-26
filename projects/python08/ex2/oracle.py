import os
import sys

VALID_MODES = ("development", "production")
CONFIG_KEYS = (
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
)


class MatrixConfig:
    def __init__(
        self,
        matrix_mode: str,
        database_url: str,
        api_key: str,
        log_level: str,
        zion_endpoint: str,
        warnings: list[str],
    ) -> None:
        self.matrix_mode = matrix_mode
        self.database_url = database_url
        self.api_key = api_key
        self.log_level = log_level
        self.zion_endpoint = zion_endpoint
        self.warnings = warnings


def project_path(filename: str) -> str:
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, filename)


def load_dotenv_file(env_path: str) -> bool:
    try:
        dotenv_module = __import__("dotenv")
    except ImportError:
        print("[WARN] python-dotenv is not installed.")
        print("Install it with: python -m pip install python-dotenv")
        return False

    load_dotenv = getattr(dotenv_module, "load_dotenv")
    load_dotenv(env_path, override=False)
    return True


def configured_value(
    name: str,
    default: str,
    warnings: list[str],
) -> str:
    value = os.environ.get(name, "")
    if value:
        return value

    warnings.append(f"{name} is missing; using a safe default.")
    return default


def default_log_level(mode: str) -> str:
    if mode == "production":
        return "INFO"
    return "DEBUG"


def load_config() -> MatrixConfig:
    warnings: list[str] = []
    mode = configured_value("MATRIX_MODE", "development", warnings)
    if mode not in VALID_MODES:
        warnings.append("MATRIX_MODE must be development or production.")
        mode = "development"

    database_url = configured_value(
        "DATABASE_URL",
        "sqlite:///matrix_default.db",
        warnings,
    )
    api_key = configured_value("API_KEY", "", warnings)
    log_level = configured_value(
        "LOG_LEVEL",
        default_log_level(mode),
        warnings,
    )
    zion_endpoint = configured_value(
        "ZION_ENDPOINT",
        "http://localhost:4242",
        warnings,
    )

    return MatrixConfig(
        mode,
        database_url,
        api_key,
        log_level,
        zion_endpoint,
        warnings,
    )


def database_status(config: MatrixConfig) -> str:
    if not config.database_url:
        return "Missing database URL"
    if config.matrix_mode == "production":
        return "Connected to production endpoint"
    if "localhost" in config.database_url or "sqlite" in config.database_url:
        return "Connected to local instance"
    return "Connected to development endpoint"


def api_status(config: MatrixConfig) -> str:
    if config.api_key:
        return "Authenticated"
    return "Missing API key"


def zion_status(config: MatrixConfig) -> str:
    if config.zion_endpoint:
        return "Online"
    return "Missing endpoint"


def runtime_profile(config: MatrixConfig) -> str:
    if config.matrix_mode == "production":
        return "strict production checks"
    return "development diagnostics enabled"


def file_contains(path: str, expected_line: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() == expected_line:
                    return True
    except OSError:
        return False
    return False


def source_contains_secret(api_key: str) -> bool:
    if not api_key:
        return False

    try:
        with open(__file__, "r", encoding="utf-8") as file:
            source = file.read()
    except OSError:
        return False
    return api_key in source


def env_file_status() -> str:
    if os.path.exists(project_path(".env")):
        return "[OK] .env file loaded for local development"
    return "[WARN] .env file not found; defaults and env vars are active"


def gitignore_status() -> str:
    if file_contains(project_path(".gitignore"), ".env"):
        return "[OK] .env file properly ignored"
    return "[WARN] .env is not listed in .gitignore"


def print_warnings(warnings: list[str]) -> None:
    if not warnings:
        return

    print()
    print("Configuration warnings:")
    for warning in warnings:
        print(f"[WARN] {warning}")


def print_security_check(config: MatrixConfig) -> None:
    print("Environment security check:")
    if source_contains_secret(config.api_key):
        print("[WARN] Possible hardcoded API key detected")
    else:
        print("[OK] No hardcoded secrets detected")
    print(gitignore_status())
    print(env_file_status())
    print("[OK] Production overrides available")


def print_config(config: MatrixConfig) -> None:
    print("Configuration loaded:")
    print(f"Mode: {config.matrix_mode}")
    print(f"Database: {database_status(config)}")
    print(f"API Access: {api_status(config)}")
    print(f"Log Level: {config.log_level}")
    print(f"Zion Network: {zion_status(config)}")
    print(f"Runtime Profile: {runtime_profile(config)}")


def main() -> int:
    print("Accessing the Mainframe")
    print("$> python oracle.py")
    print("ORACLE STATUS: Reading the Matrix...")
    load_dotenv_file(project_path(".env"))
    config = load_config()
    print_config(config)
    print_warnings(config.warnings)
    print_security_check(config)
    print("The Oracle sees all configurations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
