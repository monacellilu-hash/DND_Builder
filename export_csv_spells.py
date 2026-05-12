import json
import csv

def export_spells():
    with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
        rules = json.load(f)

    with open('Incantesimi_DND_2024.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Livello', 'Nome Incantesimo', 'Classi', 'Descrizione'])
        
        for lvl, spells in rules.get('spells', {}).items():
            for name, data in spells.items():
                classes = ', '.join(data.get('classes', []))
                desc = data.get('description', '')
                writer.writerow([lvl, name, classes, desc])
                
    print("CSV degli incantesimi generato con successo: Incantesimi_DND_2024.csv")

if __name__ == '__main__':
    export_spells()
