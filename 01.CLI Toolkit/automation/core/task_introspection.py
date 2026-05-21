def get_param_spec(task_callable):

    module = task_callable.__module__

    try:
        mod = __import__(module, fromlist=["PARAM_SPEC"])
        return getattr(mod, "PARAM_SPEC", {}) or {}
    except Exception:
        return {}
    

def summarize_params(spec: dict | None) -> str:
    if not spec:
        return "no params"

    parts = []

    for name, meta in spec.items():
        if meta.get("required"):
            parts.append(f"{name} required")
        else:
            parts.append(f"{name} optional")

    return "params (" + ", ".join(parts) + ")"