import pypdf
import os

files_to_extract = [
    {"path": "../Dati_Input/2 - Mostri del Multiverso -- Jeremy Crawford -- 2022 -- Wizards of the Coast.pdf", "out": "motm_races.txt", "start": 5, "end": 40},
    {"path": "../Dati_Input/3 - Guida di Van Richten a Ravenloft.pdf", "out": "vrgtr_races.txt", "start": 10, "end": 30}
]

for item in files_to_extract:
    try:
        reader = pypdf.PdfReader(item["path"])
        text = ""
        for i in range(item["start"], min(item["end"], len(reader.pages))):
            text += f"\n--- PAGE {i} ---\n"
            try:
                text += reader.pages[i].extract_text()
            except:
                pass
        with open(item["out"], "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted {item['out']}")
    except Exception as e:
        print(f"Failed {item['out']}: {e}")
