import fitz
import re
import csv
import json

pdf_path = r"C:\Users\Luca\Desktop\Visual Studio Code\Progetti\D&D\Dati_Input\Manuale Del Giocatore - 2024 Player’s Handbook (Dungeons & -- Wizards of the Coast -- 2025 -- Wizards of the Coast).pdf"
doc = fitz.open(pdf_path)

lines = []
# Spells are roughly between pages 238 and 348
for page_num in range(237, 348):
    page = doc[page_num]
    text = page.get_text()
    for line in text.split('\n'):
        l = line.strip()
        if l:
            lines.append(l)

# Merge spell headers that span multiple lines
merged_lines = []
skip_next = 0
for i, line in enumerate(lines):
    if skip_next > 0:
        skip_next -= 1
        continue
    
    if re.search(r'livello\s*\([^)]*$', line, re.IGNORECASE) or re.search(r'Trucchetto\s+di\s+[^\(]+\s*\([^)]*$', line, re.IGNORECASE):
        merged = line
        j = i + 1
        while j < len(lines) and ')' not in merged:
            merged += ' ' + lines[j]
            skip_next += 1
            j += 1
        merged_lines.append(merged)
    else:
        merged_lines.append(line)

spell_boundaries = []
for i, line in enumerate(merged_lines):
    m_level = re.search(r"^([^\(]+)\s+di\s+(\d+)\D*\s+livello\s*\((.*?)\)$", line, re.IGNORECASE)
    m_cantrip = re.search(r"^Trucchetto\s+di\s+([^\(]+)\s*\((.*?)\)$", line, re.IGNORECASE)
    
    if m_level or m_cantrip:
        # Trova il nome andando all'indietro
        name_parts = []
        name_idx_start = i - 1
        for j in range(i-1, max(-1, i-6), -1):
            cand = merged_lines[j]
            if cand.isdigit() or cand.startswith("CAPITOLO") or "INCANTESIMI" in cand or cand == "DESCRIZIONI DEGLI" or len(cand) <= 2:
                continue
            if cand.isupper():
                name_parts.insert(0, cand)
                name_idx_start = j
            else:
                if not name_parts:
                    name_parts.insert(0, cand)
                    name_idx_start = j
                break
        
        name = " ".join(name_parts)
        if not name:
            name = merged_lines[i-1]
            name_idx_start = i - 1
            
        level = m_level.group(2) if m_level else "0"
        school = m_level.group(1).strip() if m_level else m_cantrip.group(1).strip()
        classes = m_level.group(3).strip() if m_level else m_cantrip.group(2).strip()
        
        spell_boundaries.append({
            "Nome": name.replace("\ufffd", "'").strip(),
            "Livello": level,
            "Scuola": school,
            "Classi": classes,
            "header_idx": i,
            "name_idx": name_idx_start
        })

spells = []
for k, b in enumerate(spell_boundaries):
    start_idx = b["header_idx"] + 1
    end_idx = spell_boundaries[k+1]["name_idx"] if k + 1 < len(spell_boundaries) else len(merged_lines)
    
    spell_dict = {
        "Nome": b["Nome"],
        "Livello": b["Livello"],
        "Scuola": b["Scuola"],
        "Classi": b["Classi"],
        "Tempo di lancio": "",
        "Gittata": "",
        "Componenti": "",
        "Durata": "",
        "Descrizione": []
    }
    
    current_field = None
    for idx in range(start_idx, end_idx):
        line = merged_lines[idx]
        
        # Skip headers/footers/page numbers
        if line.isdigit() or line.startswith("CAPITOLO") or "INCANTESIMI" in line or line == "DESCRIZIONI DEGLI":
            continue
            
        if line.startswith("Tempo di lancio:"):
            spell_dict["Tempo di lancio"] = line.replace("Tempo di lancio:", "").strip()
            current_field = "Tempo di lancio"
        elif line.startswith("Gittata:"):
            spell_dict["Gittata"] = line.replace("Gittata:", "").strip()
            current_field = "Gittata"
        elif line.startswith("Componenti:"):
            spell_dict["Componenti"] = line.replace("Componenti:", "").strip()
            current_field = "Componenti"
        elif line.startswith("Durata:"):
            spell_dict["Durata"] = line.replace("Durata:", "").strip()
            current_field = "Descrizione"
        else:
            if current_field == "Tempo di lancio":
                spell_dict["Tempo di lancio"] += " " + line.replace("\ufffd", "'")
            elif current_field == "Gittata":
                spell_dict["Gittata"] += " " + line.replace("\ufffd", "'")
            elif current_field == "Componenti":
                spell_dict["Componenti"] += " " + line.replace("\ufffd", "'")
            else:
                current_field = "Descrizione"
                spell_dict["Descrizione"].append(line.replace("\ufffd", "'"))
                
    spell_dict["Descrizione"] = " ".join(spell_dict["Descrizione"]).strip()
    spells.append(spell_dict)

print(f"Total spells found: {len(spells)}")

csv_file = r"C:\Users\Luca\Desktop\Visual Studio Code\Progetti\D&D\DND_Builder\Incantesimi_Tutti.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Nome", "Livello", "Scuola", "Classi", "Tempo di lancio", "Gittata", "Componenti", "Durata", "Descrizione"])
    writer.writeheader()
    for sp in spells:
        writer.writerow(sp)

print(f"File salvato in {csv_file}")

# Facciamo un controllo su SCRITTO ILLUSORIO
print("\\nVerifica Scritto Illusorio:")
for sp in spells:
    if "SCRITTO ILLUSORIO" in sp["Nome"].upper():
        print(f"Nome: {sp['Nome']}")
        print(f"Descrizione: {sp['Descrizione'][-150:]}")
        print("---")
    if "SCRUTARE" in sp["Nome"].upper():
        print(f"Nome: {sp['Nome']}")
        print(f"Descrizione: {sp['Descrizione'][:150]}")
        print("---")
