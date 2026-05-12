import fitz
import re
import csv
import json

def extract_all_feats():
    pdf_path = '../Dati_Input/Manuale Del Giocatore - 2024 Player’s Handbook (Dungeons & -- Wizards of the Coast -- 2025 -- Wizards of the Coast).pdf'
    doc = fitz.open(pdf_path)
    
    text_lines = []
    for i in range(198, 212):
        try:
            page_text = doc[i].get_text()
            for line in page_text.split('\n'):
                line = line.strip()
                if not line: continue
                if "CAPITOLO 5" in line.upper() or "TALENTI" in line.upper() or line.isdigit():
                    continue
                text_lines.append(line)
        except Exception as e:
            print(e)
            
    feats = {}
    current_feat = None
    
    # We will look for lines that look like "Talento Origine", "Talento Generale", "Talento Stile di Combattimento", "Talento Dono Epico"
    # Wait, usually the feat name is in ALL CAPS or specific formatting, followed by the category.
    # Let's try to capture lines that end with specific categories or just dump the text and use some heuristics.
    
    full_text = "\n".join(text_lines)
    with open('test_feats.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)
        
if __name__ == "__main__":
    extract_all_feats()
