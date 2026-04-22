# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime

OUTPUT_DIR = r"D:\BIM_Exports"


def ensure_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def export_json(data, project_name):
    ensure_dir()
    filename = "{}_{}.json".format(project_name, get_timestamp())
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print("  JSON guardado: {}".format(filepath))
    return filepath


def export_excel(data, project_name):
    ensure_dir()
    filename = "{}_{}.csv".format(project_name, get_timestamp())
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w") as f:
        for category, records in data.items():
            if not records:
                continue
            f.write("=== {} ===\n".format(category))
            headers = list(records[0].keys())
            f.write(",".join(headers) + "\n")
            for record in records:
                row = [str(record.get(h) or "") for h in headers]
                f.write(",".join(row) + "\n")
            f.write("\n")

    print("  CSV guardado: {}".format(filepath))
    return filepath