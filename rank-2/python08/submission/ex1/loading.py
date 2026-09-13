import importlib
import importlib.metadata
import sys

Dependency = tuple[str, str, str]

DATA_POINTS = 1000
OUTPUT_FILE = "matrix_analysis.png"
# Each dependency stores: package name, import name, success message.
DEPENDENCIES: list[Dependency] = [
    ("pandas", "pandas", "Data manipulation ready"),
    ("numpy", "numpy", "Numerical computation ready"),
    ("matplotlib", "matplotlib", "Visualization ready"),
]


def dependency_version(package_name: str, import_name: str) -> str:
    # Prefer installed package metadata; fall back to module __version__.
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        module = importlib.import_module(import_name)
        version = getattr(module, "__version__", "unknown")
        return str(version)


def check_dependency(dependency: Dependency) -> bool:
    package_name, import_name, ready_message = dependency
    try:
        # Dynamic import lets us report missing packages without a traceback.
        importlib.import_module(import_name)
    except ImportError:
        print(f"[MISSING] {package_name} - install this Matrix program")
        return False

    version = dependency_version(package_name, import_name)
    print(f"[OK] {package_name} ({version}) - {ready_message}")
    return True


def check_dependencies() -> list[str]:
    missing: list[str] = []

    print("Checking dependencies:")
    for dependency in DEPENDENCIES:
        if not check_dependency(dependency):
            missing.append(dependency[0])
    return missing


def print_installation_help(missing: list[str]) -> None:
    print()
    print("Missing dependencies:")
    for package_name in missing:
        print(f"- {package_name}")
    print()
    print("Install with pip:")
    print("python -m pip install -r requirements.txt")
    print()
    print("Install with Poetry:")
    print("poetry install")
    print("poetry run python loading.py")


def show_dependency_management_comparison() -> None:
    # pip uses requirements.txt; Poetry uses pyproject.toml.
    print()
    print("Dependency management comparison:")
    print("pip reads requirements.txt and installs into the active Python.")
    print("Poetry reads pyproject.toml and manages a project environment.")
    print(f"Active Python: {sys.executable}")
    print(f"Active environment prefix: {sys.prefix}")


def import_programs() -> dict[str, object]:
    matplotlib = importlib.import_module("matplotlib")
    use_backend = getattr(matplotlib, "use")
    # Agg saves image files without needing a GUI window.
    use_backend("Agg")

    return {
        "pandas": importlib.import_module("pandas"),
        "numpy": importlib.import_module("numpy"),
        "pyplot": importlib.import_module("matplotlib.pyplot"),
    }


def column(frame: object, name: str) -> object:
    getter = getattr(frame, "__getitem__")
    return getter(name)


def row_count(frame: object) -> int:
    length = getattr(frame, "__len__")
    return int(length())


def series_mean(series: object) -> float:
    mean = getattr(series, "mean")
    return float(mean())


def series_max(series: object) -> float:
    maximum = getattr(series, "max")
    return float(maximum())


def build_matrix_data(
    pandas_module: object,
    numpy_module: object,
) -> object:
    random_module = getattr(numpy_module, "random")
    default_rng = getattr(random_module, "default_rng")
    # A seed keeps the simulated data repeatable during review.
    rng = default_rng(42)
    linspace = getattr(numpy_module, "linspace")

    # Numpy is the source of the dataset, as required by the subject.
    data = {
        "cycle": linspace(1, DATA_POINTS, DATA_POINTS, dtype=int),
        "signal_strength": rng.normal(100.0, 12.0, DATA_POINTS),
        "anomaly_score": rng.normal(4.5, 1.2, DATA_POINTS),
        "agents_detected": rng.integers(0, 8, DATA_POINTS),
    }
    data_frame = getattr(pandas_module, "DataFrame")
    return data_frame(data)


def analyze_matrix_data(frame: object) -> dict[str, float]:
    signal = column(frame, "signal_strength")
    anomaly = column(frame, "anomaly_score")
    agents = column(frame, "agents_detected")

    # Pandas Series methods produce the summary statistics.
    return {
        "average_signal": series_mean(signal),
        "average_anomaly": series_mean(anomaly),
        "max_agents": series_max(agents),
    }


def generate_visualization(
    pyplot: object,
    frame: object,
    summary: dict[str, float],
) -> None:
    figure = getattr(pyplot, "figure")
    plot = getattr(pyplot, "plot")
    axhline = getattr(pyplot, "axhline")
    title = getattr(pyplot, "title")
    xlabel = getattr(pyplot, "xlabel")
    ylabel = getattr(pyplot, "ylabel")
    legend = getattr(pyplot, "legend")
    tight_layout = getattr(pyplot, "tight_layout")
    savefig = getattr(pyplot, "savefig")
    close = getattr(pyplot, "close")

    figure(figsize=(9, 5))
    plot(column(frame, "cycle"), column(frame, "signal_strength"))
    plot(column(frame, "cycle"), column(frame, "anomaly_score"))
    axhline(
        summary["average_signal"],
        linestyle="--",
        color="green",
        label="Average signal",
    )
    title("Matrix Data Stream Analysis")
    xlabel("Cycle")
    ylabel("Reading")
    legend(["Signal strength", "Anomaly score", "Average signal"])
    tight_layout()
    # The visualization is generated output, not a file to submit.
    savefig(OUTPUT_FILE, dpi=150)
    close()


def run_analysis() -> None:
    modules = import_programs()
    pandas_module = modules["pandas"]
    numpy_module = modules["numpy"]
    pyplot = modules["pyplot"]

    print()
    print("Analyzing Matrix data...")
    frame = build_matrix_data(pandas_module, numpy_module)
    print(f"Processing {row_count(frame)} data points...")
    summary = analyze_matrix_data(frame)
    print(f"Average signal strength: {summary['average_signal']:.2f}")
    print(f"Average anomaly score: {summary['average_anomaly']:.2f}")
    print(f"Maximum agents detected: {summary['max_agents']:.0f}")
    print("Generating visualization...")
    generate_visualization(pyplot, frame, summary)
    print("Analysis complete!")
    print(f"Results saved to: {OUTPUT_FILE}")


def main() -> int:
    print("Loading Programs")
    print("$> python loading.py")
    print("LOADING STATUS: Loading programs...")
    missing = check_dependencies()
    show_dependency_management_comparison()

    if missing:
        print_installation_help(missing)
        return 1

    run_analysis()
    return 0


if __name__ == "__main__":
    sys.exit(main())
