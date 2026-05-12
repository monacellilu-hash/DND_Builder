import fitz
import re
import csv

def extract_all_spells():
    pdf_path = '../Dati_Input/Manuale Del Giocatore - 2024 Player’s Handbook (Dungeons & -- Wizards of the Coast -- 2025 -- Wizards of the Coast).pdf'
    doc = fitz.open(pdf_path)
    
    text_lines = []
    # Spells start around page 240 and go up to around 343
    for i in range(240, 344):
        try:
            page_text = doc[i].get_text()
            for line in page_text.split('\n'):
                line = line.strip()
                if not line: continue
                if "CAPITOLO 7" in line.upper() or "INCANTESIMI" in line.upper() or line.isdigit():
                    continue
                if "--- PAGE" in line:
                    continue
                text_lines.append(line)
        except:
            pass
            
    spells = []
    current_spell = None
    
    for i, line in enumerate(text_lines):
        # Match level: "Divinazione di 2° livello (mago, stregone, warlock)"
        m_level = re.search(r"^([A-Za-z\s]+)\s+di\s+(\d+)°\s+livello\s+\((.*?)\)", line, re.IGNORECASE)
        # Match cantrip: "Trucchetto di Ammaliamento (bardo, mago, stregone, warlock)"
        m_cantrip = re.search(r"^Trucchetto\s+di\s+([A-Za-z\s]+)\s+\((.*?)\)", line, re.IGNORECASE)
        
        if m_level or m_cantrip:
            # The previous line is usually the spell name
            name = text_lines[i-1]
            if len(name) < 3 or name.islower() or "Tempo di" in name: 
                # It might be split on two lines
                if i >= 2:
                    name = text_lines[i-2] + " " + text_lines[i-1]
            
            # Clean up name if it accidentally picked up previous spell's end
            name = name.split('.')[-1].strip()
            
            if m_level:
                level = f"Level {m_level.group(2)}"
                classes = m_level.group(3)
            else:
                level = "Cantrip"
                classes = m_cantrip.group(2)
                
            if current_spell:
                spells.append(current_spell)
                
            current_spell = {
                'name': name,
                'level': level,
                'classes': classes.title(),
                'desc_lines': []
            }
        elif current_spell:
            # Don't add structural lines to description if we don't want them, but let's just add everything for now
            current_spell['desc_lines'].append(line)
            
    if current_spell:
        spells.append(current_spell)
        
    # Write to CSV
    with open('Lista_Tutti_Incantesimi_2024.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Livello", "Nome Incantesimo", "Classi", "Descrizione Base"])
        for sp in spells:
            # Join the description lines, filter out standard headers
            raw_desc = " ".join(sp['desc_lines'])
            # We can optionally remove "Tempo di lancio: ... Durata: ..." from the preview if we want it cleaner
            # For now let's just put the first 300 characters as a base description
            desc = raw_desc[:300] + ("..." if len(raw_desc) > 300 else "")
            writer.writerow([sp['level'], sp['name'].upper(), sp['classes'], desc])
            
    print(f"Estratti {len(spells)} incantesimi in Lista_Tutti_Incantesimi_2024.csv")

if __name__ == "__main__":
    extract_all_spells()
