import csv
import json
import re

# Questo file consente all'utente di gestire, in un comodo file foglio di calcolo, 
# la lista infinita di incantesimi di D&D.

with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

# Aggiunge altri incantesimi standard che mancavano al file (come richiesto)
more_spells = {
    "Level 1": {
        "Dardo Incantato": {"classes": ["Sorcerer", "Wizard"], "description": "Lanci 3 dardi di energia magica. Ogni dardo infligge 1d4+1 danni da forza."},
        "Sonno": {"classes": ["Bard", "Sorcerer", "Wizard"], "description": "Fai addormentare creature per un totale di 5d8 Punti Ferita."},
        "Caduta Piumata": {"classes": ["Bard", "Sorcerer", "Wizard"], "description": "Fino a 5 creature cadono lentamente senza subire danni."},
        "Mani Brucianti": {"classes": ["Sorcerer", "Wizard"], "description": "Cono di fuoco 4.5m che infligge 3d6 danni da fuoco."},
        "Charme su Persone": {"classes": ["Bard", "Druid", "Sorcerer", "Warlock", "Wizard"], "description": "Affascini un umanoide che ti considera amichevole."},
        "Luce": {"classes": ["Bard", "Cleric", "Sorcerer", "Wizard"], "description": "Fai emettere luce a un oggetto."}
    },
    "Level 2": {
        "Frantumare": {"classes": ["Bard", "Sorcerer", "Warlock", "Wizard"], "description": "Un forte rumore infligge 3d8 danni da tuono in un raggio di 3 metri."},
        "Passo Senza Tracce": {"classes": ["Druid", "Ranger"], "description": "+10 a Furtività per te e i tuoi alleati."},
        "Arma Spirituale": {"classes": ["Cleric"], "description": "Crei un'arma magica volante che attacca come azione bonus (1d8+mod forza/saggezza danni)."},
        "Oscurità": {"classes": ["Sorcerer", "Warlock", "Wizard"], "description": "Crei un'oscurità magica in un raggio di 4.5m."},
        "Ragnatela": {"classes": ["Druid", "Sorcerer", "Wizard"], "description": "Crei ragnatele appiccicose in un cubo di 6m."},
        "Blocca Persone": {"classes": ["Bard", "Cleric", "Druid", "Sorcerer", "Warlock", "Wizard"], "description": "Paralizzi un umanoide."}
    },
    "Level 3": {
        "Palla di Fuoco": {"classes": ["Sorcerer", "Wizard"], "description": "Esplosione di fuoco in 6 metri di raggio, infligge 8d6 danni da fuoco."},
        "Controincantesimo": {"classes": ["Sorcerer", "Warlock", "Wizard"], "description": "Interrompi una creatura mentre sta lanciando un incantesimo."},
        "Dissipare Magie": {"classes": ["Bard", "Cleric", "Druid", "Paladin", "Sorcerer", "Warlock", "Wizard"], "description": "Poni fine agli incantesimi attivi su una creatura, oggetto o effetto."},
        "Volare": {"classes": ["Sorcerer", "Warlock", "Wizard"], "description": "La creatura ottiene velocità di volare 18m."},
        "Velocità": {"classes": ["Sorcerer", "Wizard"], "description": "La velocità del bersaglio raddoppia, +2 CA, vantaggio su TS Destrezza e un'azione aggiuntiva."},
        "Rianimare Morti": {"classes": ["Cleric", "Paladin"], "description": "Riporti in vita una creatura morta da non più di 1 minuto."}
    }
}

for lvl, sp in more_spells.items():
    if lvl not in rules['spells']:
        rules['spells'][lvl] = {}
    for name, data in sp.items():
        rules['spells'][lvl][name] = data

with open('data/rules_2024.json', 'w', encoding='utf-8') as f:
    json.dump(rules, f, indent=2, ensure_ascii=False)
    
with open('Lista_Incantesimi.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Livello", "Nome Incantesimo", "Classi", "Descrizione Base"])
    
    for level, spells in rules.get('spells', {}).items():
        for spell_name, spell_data in spells.items():
            classes = ", ".join(spell_data.get('classes', []))
            desc = spell_data.get('description', '')
            writer.writerow([level, spell_name, classes, desc])
            
print("File Lista_Incantesimi.csv generato e regole aggiornate con nuovi incantesimi base!")
