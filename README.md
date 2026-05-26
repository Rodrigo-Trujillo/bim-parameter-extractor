# BIM Parameter Extractor & QA System

A pyRevit extension that connects to the Revit API to automatically extract structural element data, validate model quality, and send data to a Django REST API.

## What it does

- Extracts structural columns, beams, and walls from active Revit models
- Exports data to timestamped JSON and CSV files
- Validates model quality against configurable JSON rules
- Colors failing elements red and passing elements green directly in Revit
- Generates QA reports in JSON format
- Sends extracted data to a Django REST API endpoint

## Tech Stack

- Python (IronPython 2.7 via pyRevit)
- Revit API — FilteredElementCollector, BuiltInCategory, LookupParameter, OverrideGraphicSettings
- pyRevit framework
- JSON / CSV export (standard library)
- HTTP integration with Django REST API

## Project structure
BIM_Extractor.extension/
└── BIM_Extractor.tab/
└── BIM_Extractor.panel/
└── Extract.pushbutton/
└── script.py        # Entry point
lib/
├── extractor.py                 # Revit API logic
├── exporter.py                  # JSON and CSV export
├── validator.py                 # QA validation with color override
└── rules.json                   # Configurable validation rules

## How to use

1. Install pyRevit from https://github.com/eirannejad/pyRevit/releases
2. Clone this repository
3. In pyRevit Settings → Custom Extension Directories → add the repo folder
4. Click Save Settings and Reload
5. Open a Revit model with structural elements
6. Go to the BIM_Extractor tab and click Extract
7. JSON and CSV files are saved to D:\BIM_Exports\

## QA Validation

Rules are defined in `lib/rules.json`. Example:

```json
{
  "rules": [
    {
      "category": "Columns",
      "parameter": "Mark",
      "check": "not_null",
      "description": "All columns must have a Mark value"
    }
  ]
}
```

Elements that fail validation are colored red in the Revit model. A full QA report is exported to JSON.

## Django Integration

This extension sends extracted BIM data to the Infrastructure Asset Management System API:
POST http://127.0.0.1:8000/api/v1/bim/import/

## Author

Rodrigo Trujillo — Civil Engineer & BIM Developer
GitHub: https://github.com/Rodrigo-Trujillo
LinkedIn: https://linkedin.com/in/rodrigo-andrés-trujillo-cortés-02255b267