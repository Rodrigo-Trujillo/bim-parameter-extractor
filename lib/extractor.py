# -*- coding: utf-8 -*-
# extractor.py — Extrae parametros de elementos estructurales

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    BuiltInCategory,
    BuiltInParameter,
    StorageType,
)

CATEGORIES = {
    "Columns": BuiltInCategory.OST_StructuralColumns,
    "Beams":   BuiltInCategory.OST_StructuralFraming,
    "Walls":   BuiltInCategory.OST_Walls,
}

PARAMETERS = {
    "Columns": ["Mark", "Length", "Volume", "Structural Material"],
    "Beams":   ["Mark", "Length", "Volume", "Structural Material"],
    "Walls":   ["Mark", "Length", "Height", "Width", "Area", "Volume"],
}


def get_param_value(element, param_name):
    param = element.LookupParameter(param_name)
    if param is None:
        return None
    if param.StorageType == StorageType.String:
        return param.AsString()
    elif param.StorageType == StorageType.Double:
        return round(param.AsDouble() * 0.3048, 4)
    elif param.StorageType == StorageType.Integer:
        return param.AsInteger()
    return None


def extract_all(doc):
    results = {}
    for category_name, bic in CATEGORIES.items():
        collector = (
            FilteredElementCollector(doc)
            .OfCategory(bic)
            .WhereElementIsNotElementType()
            .ToElements()
        )
        records = []
        for elem in collector:
            tipo = doc.GetElement(elem.GetTypeId())
            tipo_nombre = tipo.get_Parameter(
                BuiltInParameter.SYMBOL_NAME_PARAM
            ).AsString() if tipo else "N/A"

            record = {
                "element_id": elem.Id.IntegerValue,
                "type_name":  tipo_nombre,
            }
            for pname in PARAMETERS[category_name]:
                record[pname] = get_param_value(elem, pname)

            records.append(record)

        results[category_name] = records
        print("  {} → {} elementos".format(category_name, len(records)))

    return results