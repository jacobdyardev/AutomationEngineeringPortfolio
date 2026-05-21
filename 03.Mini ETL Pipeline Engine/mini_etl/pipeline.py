from pathlib import Path

try:
    # Preferred (CLI / full system)
    from automation.utils.excel_writer import write_excel  # pyright: ignore
except ImportError:
    # Standalone fallback
    from .internal.excel_writer import write_excel

from .extractors import extract_json
from .transformer import (
    parse_list,
    parse_mapping,
    apply_transforms,
    compute_metrics
)
from .loaders import write_json, write_csv


# =========================================
# 🔥 Nested path resolver (supports lists)
# =========================================
def get_nested_value(data, path):
    keys = path.split(".")
    value = data

    for key in keys:

        if isinstance(value, list):
            try:
                index = int(key)
            except ValueError:
                return None

            if index < len(value):
                value = value[index]
            else:
                return None

        elif isinstance(value, dict):
            if key in value:
                value = value[key]
            else:
                return None

        else:
            return None

    return value


# =========================================
# 🔥 Mapping Resolver (normalize + aliases)
# =========================================
def resolve_mapping(source, mapping_config):

    if not source:
        return None, None

    source_norm = source.lower()

    # -----------------------------
    # 1. Direct normalized match
    # -----------------------------
    for key, config in mapping_config.items():
        if key.lower() == source_norm:
            return key, config

    # -----------------------------
    # 2. Alias match
    # -----------------------------
    for key, config in mapping_config.items():
        aliases = config.get("aliases", [])

        for alias in aliases:
            if alias.lower() == source_norm:
                return key, config

    return None, None


# =========================================
# 🔥 EXTRACTION (UPDATED + CORRECT)
# =========================================
def apply_extraction(data, mapping_config, mapping_key=None):

    cleaned = []

    # ----------------------------------------
    # 🔥 Pre-resolve mapping (if using mapping_key)
    # ----------------------------------------
    if mapping_key:
        mapping = mapping_config.get(mapping_key)

        if not mapping:
            raise RuntimeError(f"Mapping '{mapping_key}' not found in mapping file")

    for row in data:

        # ----------------------------------------
        # 🔥 Mode 1 — UWAF (mapping_key)
        # ----------------------------------------
        if mapping_key:
            source = mapping_key

        # ----------------------------------------
        # 🔥 Mode 2 — API (original behavior)
        # ----------------------------------------
        else:
            source = row.get("source")

            if not mapping_config:
                continue

            resolved_key, mapping = resolve_mapping(source, mapping_config)

            if not mapping:
                print(f"[ETL WARNING] No mapping found for source: {source}")
                continue

            source = resolved_key  # normalize source name

        if not mapping:
            continue

        new_row = {
            "source": source
        }

        # Preserve API error state
        if "error" in row:
            new_row["error"] = row["error"]

        # ----------------------------------------
        # 🔥 Apply mapping
        # ----------------------------------------
        for key, path in mapping.items():

            if key == "aliases":
                continue

            # Prevent overwriting normalized source
            if mapping_key and key == "source":
                continue

            if "." in path:
                value = get_nested_value(row, path)
            else:
                value = row.get(path)

            new_row[key] = value

        cleaned.append(new_row)

    return cleaned


# =========================================
# MAIN PIPELINE
# =========================================
def run_pipeline(artifact_dir: Path, params: dict):

    pipeline_mode = params.get("pipeline_mode", False)

    output_format = params.get("output_format", "json")
    output_mode = params.get("output_mode", "wide")

    pipeline_next = params.get("pipeline_next")

    if pipeline_mode and pipeline_next == "excel_kpi":
        output_format = "json"

    input_path = Path(params["input_path"])

    mapping_file = params.get("mapping_file")
    mapping_key = params.get("mapping_key")

    mapping_config = None

    if mapping_file:
        from automation.utils.path_resolver import resolve_path  # pyright: ignore[reportMissingImports]

        mapping_path = resolve_path(mapping_file, "mappings")

        import toml
        mapping_config = toml.load(mapping_path)

    # =========================================
    # Extract
    # =========================================
    data = extract_json(input_path)

    mapping_config = {
        key.lower(): value
        for key, value in mapping_config.items()
    } 

    if mapping_config:
        data = apply_extraction(data, mapping_config, mapping_key)

    # =========================================
    # Parse params
    # =========================================
    fields = parse_list(params.get("fields"))
    rename_map = parse_mapping(params.get("rename"))
    metrics = parse_list(params.get("metrics"))

    # =========================================
    # Transform
    # =========================================
    transformed = apply_transforms(
        data,
        fields,
        rename_map,
        mapping_config
    )

    # =========================================
    # Metrics
    # =========================================
    metric_results = compute_metrics(transformed, metrics)

    data_file = artifact_dir / "etl_output"
    metrics_file = artifact_dir / "metrics.json"

    # =========================================
    # Output handling
    # =========================================
    if output_format == "csv":
        data_file = data_file.with_suffix(".csv")
        write_csv(data_file, transformed)

    elif output_format == "excel":
        if not transformed:
            raise RuntimeError("No data to write to Excel")

        data_file = data_file.with_suffix(".xlsx")
        write_excel(data_file, transformed, mode=output_mode)

    else:
        data_file = data_file.with_suffix(".json")
        write_json(data_file, transformed)

    if metric_results:
        write_json(metrics_file, metric_results)

    return transformed, metric_results, data_file, metrics_file