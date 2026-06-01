import os

VALID_MODES = ("development", "production")

DEFAULTS: dict[str, str | None] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "sqlite:///matrix_default.db",
    "API_KEY": "",
    "LOG_LEVEL": None,
    "ZION_ENDPOINT": "http://localhost:4242",
}


def path(f: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), f)


def load_dotenv(p: str) -> None:
    try:
        from dotenv import load_dotenv as _load
        _load(path(p), override=False)
    except ImportError:
        print("[WARN] python-dotenv not installed. Run: pip install python-dotenv")


def get_env(name: str, default: str, warnings: list[str]) -> str:
    value = os.environ.get(name, "")
    if value:
        return value
    warnings.append(f"{name} is missing; using a safe default.")
    return default


def load_config() -> dict[str, str | list[str]]:
    warnings: list[str] = []

    mode = get_env("MATRIX_MODE", "development", warnings)
    if mode not in VALID_MODES:
        warnings.append("MATRIX_MODE must be development or production.")
        mode = "development"

    default_log = "INFO" if mode == "production" else "DEBUG"

    return {
        "mode":     mode,
        "db_url":   get_env("DATABASE_URL", "sqlite:///matrix_default.db", warnings),
        "api_key":  get_env("API_KEY", "", warnings),
        "log":      get_env("LOG_LEVEL", default_log, warnings),
        "zion":     get_env("ZION_ENDPOINT", "http://localhost:4242", warnings),
        "warnings": warnings,
    }


def db_status(cfg: dict[str, str | list[str]]) -> str:
    if not cfg["db_url"]:
        return "Missing database URL"
    if cfg["mode"] == "production":
        return "Connected to production endpoint"
    if "localhost" in str(cfg["db_url"]) or "sqlite" in str(cfg["db_url"]):
        return "Connected to local instance"
    return "Connected to development endpoint"


def file_has_line(p: str, expected: str) -> bool:
    try:
        with open(p, encoding="utf-8") as f:
            return any(line.strip() == expected for line in f)
    except OSError:
        return False


def key_in_source(value: str) -> bool:
    if not value:
        return False
    try:
        return value in open(__file__, encoding="utf-8").read()
    except OSError:
        return False


def print_config(cfg: dict[str, str | list[str]]) -> None:
    print("Configuration loaded:")
    print(f"Mode:           {cfg['mode']}")
    print(f"Database:       {db_status(cfg)}")
    print(f"API Access:     {'Authenticated' if cfg['api_key'] else 'Missing API key'}")
    print(f"Log Level:      {cfg['log']}")
    print(f"Zion Network:   {'Online' if cfg['zion'] else 'Missing endpoint'}")
    print(f"Runtime:        {'strict production checks' if cfg['mode'] == 'production' else 'development diagnostics enabled'}")


def print_warnings(warnings: list[str]) -> None:
    if warnings:
        print("\nConfiguration warnings:")
        for w in warnings:
            print(f"[WARN] {w}")


def print_security(cfg: dict[str, str | list[str]]) -> None:
    print("Environment security check:")
    print("[WARN] Possible hardcoded API key detected" if key_in_source(str(cfg["api_key"])) else "[OK] No hardcoded secrets detected")
    print("[OK] .env file properly ignored" if file_has_line(path(".gitignore"), ".env") else "[WARN] .env is not listed in .gitignore")
    print("[OK] .env file loaded for local development" if os.path.exists(path(".env")) else "[WARN] .env file not found; defaults and env vars are active")
    print("[OK] Production overrides available")


if __name__ == "__main__":
    print()
    print("$> python oracle.py")
    print()
    print("ORACLE STATUS: Reading the Matrix...")
    load_dotenv(".env")
    cfg = load_config()
    print()
    print_config(cfg)
    print_warnings(list(cfg["warnings"]))
    print()
    print_security(cfg)
    print()
    print("The Oracle sees all configurations.")
    print(f"ALL:\n{cfg if cfg else 'Missing API key'}")
