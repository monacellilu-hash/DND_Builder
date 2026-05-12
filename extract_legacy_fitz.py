import fitz

def extract_pages(pdf_path, output_name, start_page, end_page):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for i in range(start_page, min(end_page, len(doc))):
            text += f"\n--- PAGE {i} ---\n"
            text += doc[i].get_text()
            
        with open(f"{output_name}.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved {output_name}.txt")
    except Exception as e:
        print(f"Error on {output_name}: {e}")

extract_pages("../Dati_Input/2 - Mostri del Multiverso -- Jeremy Crawford -- 2022 -- Wizards of the Coast.pdf", "motm_pages", 0, 45)
extract_pages("../Dati_Input/3 - Guida di Van Richten a Ravenloft.pdf", "vrgtr_pages", 0, 30)
