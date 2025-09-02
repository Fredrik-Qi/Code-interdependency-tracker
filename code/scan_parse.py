import os
import re
import pandas as pd
import json

def scan_code_folder(folder_path, extensions=None):
    if extensions is None:
        extensions = ['.py', '.R', '.ipynb']
    code_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                code_files.append(os.path.join(root, file))
    return code_files
def parse_cit_block(file_path):
    cit_data = {}
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == ".ipynb":
            with open(file_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            lines = []
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") == "code":
                    lines.extend(cell.get("source", []))
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        return None

    in_cit_block = False
    for line in lines:
        line = line.strip()
        if line.startswith("# CIT"):
            in_cit_block = True
            continue
        if in_cit_block:
            if line.startswith("# END"):
                break
            if line.startswith("#"):
                line_content = line[1:].strip()
                if ':' in line_content:
                    key, value = map(str.strip, line_content.split(":", 1))
                    values = [v.strip() for v in value.split(',')] if value else []
                    cit_data[key.lower()] = values
    if cit_data:
        cit_data['file'] = file_path
    return cit_data if cit_data else None

def build_cit_table(folder_path):
    files = scan_code_folder(folder_path)
    all_data = []
    for f in files:
        parsed = parse_cit_block(f)
        if parsed:
            all_data.append(parsed)
    df = pd.DataFrame(all_data)
    return df
