# -*- coding: utf-8 -*-
# validator.py — Validates Revit elements against rules defined in rules.json

import clr
import os
import json

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    BuiltInCategory,
    BuiltInParameter,
    StorageType,
    Color,
    OverrideGraphicSettings,
    Transaction,
)

CATEGORIES = {
    "Columns": BuiltInCategory.OST_StructuralColumns,
    "Beams":   BuiltInCategory.OST_StructuralFraming,
    "Walls":   BuiltInCategory.OST_Walls,
}

FAIL_COLOR = Color(255, 0, 0)    # Red
PASS_COLOR = Color(0, 200, 0)    # Green


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


def check_rule(value, rule):
    check = rule["check"]
    if check == "not_null":
        return value is not None and value != "" and value != "None"
    elif check == "greater_than":
        try:
            return float(value) > float(rule["value"])
        except:
            return False
    return True


def apply_color(doc, element, color):
    ogs = OverrideGraphicSettings()
    ogs.SetProjectionLineColor(color)
    ogs.SetSurfaceForegroundPatternColor(color)
    doc.ActiveView.SetElementOverrides(element.Id, ogs)


def validate(doc, rules_path):
    with open(rules_path, "r") as f:
        rules_data = json.load(f)

    rules = rules_data["rules"]
    results = {"passed": [], "failed": []}

    t = Transaction(doc, "BIM QA - Color Override")
    t.Start()

    for category_name, bic in CATEGORIES.items():
        collector = (
            FilteredElementCollector(doc)
            .OfCategory(bic)
            .WhereElementIsNotElementType()
            .ToElements()
        )

        category_rules = [r for r in rules if r["category"] == category_name]

        for elem in collector:
            elem_failed = False

            for rule in category_rules:
                value = get_param_value(elem, rule["parameter"])
                if not check_rule(value, rule):
                    elem_failed = True
                    results["failed"].append({
                        "element_id": elem.Id.IntegerValue,
                        "category":   category_name,
                        "rule":       rule["description"],
                        "value":      str(value)
                    })

            if elem_failed:
                apply_color(doc, elem, FAIL_COLOR)
            else:
                apply_color(doc, elem, PASS_COLOR)

    t.Commit()

    return results