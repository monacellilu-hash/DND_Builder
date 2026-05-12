import pypdf
import json

reader = pypdf.PdfReader('../Dati_Input/1- Manuale del giocatore 2014 5.0.pdf')
# Let's extract the Table of Contents or search for Chapter 2
text = ""
for i in range(15, 45): # Pages 15 to 45 should cover races
    try:
        text += reader.pages[i].extract_text() + "\n"
    except:
        pass

with open('races_2014.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Saved races_2014.txt")
