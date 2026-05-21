import json
import csv


def write_json(output_path, data):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)


def write_csv(output_path, data):

    if not data:
        return

    # ========================
    # FORCE COLUMN ORDER
    # ========================
    ordered_keys = ["source", "status"]

    for row in data:
        for k in row.keys():
            if k not in ordered_keys:
                ordered_keys.append(k)

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ordered_keys)
        writer.writeheader()
        writer.writerows(data)