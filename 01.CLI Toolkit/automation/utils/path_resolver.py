from pathlib import Path


def resolve_path(file_name: str, subdir: str = "") -> Path:
    """
    Resolves a file path intelligently.

    Priority:
    1. Absolute path
    2. Relative to current working directory
    3. Relative to project configs folder
    """

    path = Path(file_name)

    # 1. Absolute path
    if path.is_absolute() and path.exists():
        return path

    # 2. Relative to cwd
    cwd_path = Path.cwd() / file_name
    if cwd_path.exists():
        return cwd_path

    # 3. Relative to configs folder
    project_root = Path(__file__).resolve().parents[2]
    config_path = project_root / "configs" / subdir / file_name

    if config_path.exists():
        return config_path

    raise RuntimeError(f"File not found: {file_name}")