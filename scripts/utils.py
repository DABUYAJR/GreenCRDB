from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def get_project_root(start: Path | None = None) -> Path:
    candidate = (start or Path(__file__)).resolve()
    for path in [candidate, *candidate.parents]:
        if (path / "config").exists() and (path / "data").exists():
            return path
    raise FileNotFoundError("Could not locate project root from current path.")


def get_path(*parts: str, root: Path | None = None) -> Path:
    return (root or get_project_root()) / Path(*parts)


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_module_dirs(module_name: str, root: Path | None = None) -> dict[str, Path]:
    root = root or get_project_root()
    paths = {
        "figures": root / "outputs" / "figures" / module_name,
        "tables": root / "outputs" / "tables" / module_name,
        "dashboards": root / "outputs" / "dashboards" / module_name,
        "processed": root / "data" / "processed" / module_name,
    }
    for path in paths.values():
        ensure_dir(path)
    return paths


def load_yaml_config(name: str) -> dict[str, Any]:
    path = get_path("config", name)
    data = _parse_simple_yaml(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Config file {path} did not load as a mapping.")
    return data


def safe_read_csv(path: Path | str, *, required_columns: list[str] | None = None) -> pd.DataFrame:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Required CSV not found: {csv_path}")
    frame = pd.read_csv(csv_path)
    if required_columns:
        missing = [column for column in required_columns if column not in frame.columns]
        if missing:
            raise ValueError(f"CSV {csv_path} is missing required columns: {missing}")
    return frame


def export_csv(df: pd.DataFrame, *paths: Path) -> None:
    for path in paths:
        ensure_dir(path.parent)
        df.to_csv(path, index=False)


def export_figure(fig, *paths: Path, dpi: int = 180, facecolor: str = "#f8f9fa") -> None:
    for path in paths:
        ensure_dir(path.parent)
        fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=facecolor)


def _parse_scalar(raw_value: str) -> Any:
    value = raw_value.strip()
    if not value:
        return ""
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    lines = text.splitlines()

    for index, raw_line in enumerate(lines):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()

        container = stack[-1][1]

        if stripped.startswith("- "):
            if not isinstance(container, list):
                raise ValueError("Invalid YAML structure: list item without list container.")
            container.append(_parse_scalar(stripped[2:]))
            continue

        key, _, raw_value = stripped.partition(":")
        if not _:
            raise ValueError(f"Invalid YAML line: {raw_line}")

        if raw_value.strip():
            if isinstance(container, dict):
                container[key.strip()] = _parse_scalar(raw_value)
            else:
                raise ValueError("Invalid YAML structure: scalar entry inside list.")
            continue

        next_container: Any = {}
        for next_line in lines[index + 1 :]:
            if not next_line.strip() or next_line.lstrip().startswith("#"):
                continue
            next_container = [] if next_line.strip().startswith("- ") else {}
            break
        if isinstance(container, dict):
            container[key.strip()] = next_container
        else:
            raise ValueError("Invalid YAML structure: nested key inside list.")
        stack.append((indent, next_container))
    return root
