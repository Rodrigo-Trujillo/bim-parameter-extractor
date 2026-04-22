# BIM Parameter Extractor

A pyRevit extension that connects to the Revit API to automatically extract structural element data from BIM models and export it to JSON and CSV formats.

## What it does

- Collects all structural columns, beams, and walls from an active Revit model
- Extracts key parameters: element ID, type name, mark, length, volume, and structural material
- Exports results to timestamped JSON and CSV files
- Runs directly inside Revit via a custom pyRevit button — no external scripts needed

## Tech stack

- Python (IronPython 2.7 via pyRevit)
- Revit API — FilteredElementCollector, BuiltInCategory, LookupParameter
- pyRevit framework
- JSON / CSV export (standard library)

## How to use

1. Install pyRevit from https://github.com/eirannejad/pyRevit/releases
2. Clone this repository to your local machine
3. In pyRevit Settings, Custom Extension Directories, add the repo folder
4. Click Save Settings and Reload
5. Open a Revit model with structural elements
6. Go to the BIM_Extractor tab and click Extract
7. Output files are saved to D:\BIM_Exports\

## Why this project

BIM models store enormous amounts of engineering data that is rarely used outside of Revit. This tool is a foundation for automating data extraction pipelines — feeding model data into databases, dashboards, or QA systems without manual input.

## Author

Rodrigo Trujillo — Civil Engineer and BIM Developer
GitHub: https://github.com/Rodrigo-Trujillo
LinkedIn: https://linkedin.com/in/rodrigo-andrés-trujillo-cortés-02255b267