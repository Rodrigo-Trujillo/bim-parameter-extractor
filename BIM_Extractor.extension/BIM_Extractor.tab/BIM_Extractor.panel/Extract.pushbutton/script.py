# -*- coding: utf-8 -*-
import sys
import os

LIB_PATH = r"D:\BIM EXTRACTOR\lib"
if LIB_PATH not in sys.path:
    sys.path.insert(0, LIB_PATH)

from extractor import extract_all
from exporter  import export_json, export_excel
from pyrevit    import forms

PROJECT_NAME = "BIM_Extractor"

def main():
    doc = __revit__.ActiveUIDocument.Document

    print("Extrayendo elementos del modelo: {}".format(doc.Title))
    data = extract_all(doc)

    total = sum(len(v) for v in data.values())
    print("Total extraido: {} elementos".format(total))

    print("Exportando...")
    json_path  = export_json(data, PROJECT_NAME)
    excel_path = export_excel(data, PROJECT_NAME)

    msg = "Extraccion completada!\n\nElementos: {}\n\nJSON: {}\nExcel: {}".format(
        total,
        json_path  or "No generado",
        excel_path or "No generado",
    )
    forms.alert(msg, title="BIM Extractor")

main()