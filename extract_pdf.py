import pypdf
import sys

try:
    reader = pypdf.PdfReader('../Dati_Input/Manuale Del Giocatore - 2024 Player’s Handbook (Dungeons & -- Wizards of the Coast -- 2025 -- Wizards of the Coast).pdf')
    text = []
    # Exploring pages around 33-37 based on the table of contents index for Character Creation
    for i in range(32, 38):
        try:
            text.append(f"--- PAGE {i} ---")
            text.append(reader.pages[i].extract_text())
        except Exception as e:
            text.append(f"Error on page {i}: {e}")

    with open('pdf_pages.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(text))
    print("Estrazione completata in pdf_pages.txt")
except Exception as e:
    print(f"Errore: {e}")