import pypdf

def extract_text(pdf_path, output_path, start_page, end_page):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for i in range(start_page, min(end_page, len(reader.pages))):
            try:
                text += f"\n--- PAGE {i} ---\n"
                text += reader.pages[i].extract_text()
            except:
                pass
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Saved {output_path}")
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

# In MotM, chapter 1 is usually Fantastical Races (pages 5-35 roughly)
extract_text("../Dati_Input/2 - Mostri del Multiverso -- Jeremy Crawford -- 2022 -- Wizards of the Coast.pdf", "races_motm.txt", 4, 40)

# In VRGtR, lineages are in Chapter 1 (pages 15-20 roughly)
extract_text("../Dati_Input/3 - Guida di Van Richten a Ravenloft.pdf", "races_vrgtr.txt", 10, 25)
