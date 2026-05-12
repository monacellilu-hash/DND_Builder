import fitz
import re

def extract():
    doc = fitz.open('../Dati_Input/Manuale Del Giocatore - 2024 Player’s Handbook (Dungeons & -- Wizards of the Coast -- 2025 -- Wizards of the Coast).pdf')
    text = ""
    for i in range(235, 245):
        text += f"\n--- PAGE {i} ---\n"
        text += doc[i].get_text()
    
    with open('spell_format_test.txt', 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    extract()
