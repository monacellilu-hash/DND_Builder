import fitz

def extract_spells():
    pdf_path = '../Dati_Input/Manuale Del Giocatore - 2024 Player’s Handbook (Dungeons & -- Wizards of the Coast -- 2025 -- Wizards of the Coast).pdf'
    try:
        doc = fitz.open(pdf_path)
        text = ""
        # Il capitolo Incantesimi è circa dalla pagina 234 in poi (probabilmente tra la 230 e la 345)
        for i in range(230, min(345, len(doc))):
            text += f"\n--- Pagina {i} ---\n"
            text += doc[i].get_text()
            
        with open('incantesimi_estratti_grezzi.txt', 'w', encoding='utf-8') as f:
            f.write(text)
            
        print("Ho estratto il testo grezzo in 'incantesimi_estratti_grezzi.txt'.")
        print("Poiché l'estrazione precisa di centinaia di incantesimi in un CSV richiede un parser avanzato (a causa dell'impaginazione a colonne del PDF), puoi esaminare questo file di testo per controllare gli incantesimi che mancano e poi aggiungerli al JSON.")
    except Exception as e:
        print(f"Errore durante l'estrazione: {e}")

if __name__ == "__main__":
    extract_spells()