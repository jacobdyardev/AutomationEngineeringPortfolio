def validate_required_params(params: dict, spec: dict):

    required = spec.get("required", [])

    missing = [p for p in required if p not in params]

    if missing:
        raise RuntimeError(
            f"Missing required params: {', '.join(missing)}"
        )


def apply_param_defaults(params: dict, spec: dict) -> dict:

    defaults = spec.get("defaults", {})

    merged = dict(defaults)
    merged.update(params or {})

    return merged

def print_param_help(task_name, spec):

    print()
    print(f"Task: {task_name}")
    print()
    print("Params:")
    print()

    for name, meta in spec.items():

        required = meta.get("required", False)
        default = meta.get("default")
        desc = meta.get("description", "")

        line = f"- {name}"

        if required:
            line += " (required)"
        else:
            line += " (optional)"

        if default is not None:
            line += f", default={default}"

        print(line)

        if desc:
            print(f"  {desc}")

        print()
