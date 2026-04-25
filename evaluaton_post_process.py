import json
import re
from openpyxl import Workbook

# ---------------------------
# 📥 READ FILE
# ---------------------------

with open("output.json", "r", encoding="utf-8") as f:
    content = f.read()


# ---------------------------
# 🧠 EXTRACT SECTIONS
# ---------------------------

def split_sections(text):
    sections = {}

    parts = re.split(r'---\s*(.*?)\s*---', text)

    # parts structure:
    # [before, label1, content1, label2, content2, ...]

    for i in range(1, len(parts), 2):
        label = parts[i].strip()
        content = parts[i + 1].strip()
        sections[label] = content

    return sections


def extract_json_block(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print("⚠️ JSON parsing error:", e)

    return {"classes": [], "relationships": []}

sections = split_sections(content)

single_data = extract_json_block(sections.get("SINGLE PROMPT", ""))
multi_data = extract_json_block(sections.get("MULTI STEP", ""))
no_few_data = extract_json_block(sections.get("NO FEW SHOT", ""))


# ---------------------------
# 📊 WRITE TO EXCEL
# ---------------------------

wb = Workbook()

# Remove default sheet
wb.remove(wb.active)


def write_sheet(sheet_name, data):
    ws = wb.create_sheet(title=sheet_name)

    # Headers
    ws.append(["Class Name", "", "Source", "Relationship", "Target"])

    classes = data.get("classes", [])
    relationships = data.get("relationships", [])

    max_len = max(len(classes), len(relationships))

    for i in range(max_len):
        class_name = classes[i]["name"] if i < len(classes) else ""

        if i < len(relationships):
            r = relationships[i]
            source = r.get("source", "")
            rel = r.get("name", "")
            target = r.get("target", "")
        else:
            source = rel = target = ""

        ws.append([class_name, "", source, rel, target])


# Create 3 sheets
write_sheet("Single Prompt", single_data)
write_sheet("Multi Step", multi_data)
write_sheet("No Few Shot", no_few_data)


# ---------------------------
# 💾 SAVE
# ---------------------------

file_name = "domain_model_comparison.xlsx"
wb.save(file_name)

print(f"✅ Excel file created: {file_name}")