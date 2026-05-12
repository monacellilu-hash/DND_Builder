import csv
import json

def update_rules():
    # Load existing rules
    with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Read the spells from CSV
    spells_by_level = {}
    with open('Lista_Tutti_Incantesimi_2024.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            level = row['Livello']
            name = row['Nome Incantesimo'].title()
            
            classes_str = row['Classi']
            if classes_str:
                classes = [c.strip() for c in classes_str.split(',')]
            else:
                classes = []
                
            desc = row['Descrizione Base']
            
            if level not in spells_by_level:
                spells_by_level[level] = {}
                
            spells_by_level[level][name] = {
                "classes": classes,
                "description": desc
            }

    if 'spells' not in data:
        data['spells'] = {}
        
    for lvl, spells in spells_by_level.items():
        if lvl not in data['spells']:
            data['spells'][lvl] = {}
        for name, s_data in spells.items():
            data['spells'][lvl][name] = s_data

    # Complete 2024 Backgrounds
    backgrounds = {
        "Acolyte": {
          "name_it": "Accolito",
          "ability_boosts": ["Intelligenza", "Saggezza", "Carisma"],
          "skills": ["Intuizione", "Religione"],
          "tools": ["Calligrapher's Supplies"],
          "origin_feat": "Magic Initiate (Cleric)",
          "description": "Hai dedicato la tua vita al servizio di un tempio, imparando segreti magici."
        },
        "Artisan": {
          "name_it": "Artigiano",
          "ability_boosts": ["Forza", "Destrezza", "Intelligenza"],
          "skills": ["Indagare", "Persuasione"],
          "tools": ["Artisan's Tools"],
          "origin_feat": "Crafter",
          "description": "Hai imparato un mestiere e sei abile nel contrattare."
        },
        "Charlatan": {
          "name_it": "Ciarlatano",
          "ability_boosts": ["Destrezza", "Costituzione", "Carisma"],
          "skills": ["Inganno", "Rapidità di Mano"],
          "tools": ["Forgery Kit"],
          "origin_feat": "Skilled",
          "description": "Un esperto di inganni e manipolazioni."
        },
        "Farmer": {
          "name_it": "Contadino",
          "ability_boosts": ["Forza", "Costituzione", "Saggezza"],
          "skills": ["Addestrare Animali", "Natura"],
          "tools": ["Carpenter's Tools"],
          "origin_feat": "Tough",
          "description": "Hai coltivato la terra e lavorato duramente."
        },
        "Criminal": {
          "name_it": "Criminale",
          "ability_boosts": ["Destrezza", "Costituzione", "Intelligenza"],
          "skills": ["Furtività", "Rapidità di Mano"],
          "tools": ["Thieves' Tools", "Gaming Set"],
          "origin_feat": "Alert",
          "description": "Hai vissuto al di fuori della legge, sopravvivendo con l'astuzia."
        },
        "Entertainer": {
          "name_it": "Intrattenitore",
          "ability_boosts": ["Destrezza", "Forza", "Carisma"],
          "skills": ["Acrobazia", "Intrattenere"],
          "tools": ["Musical Instrument", "Disguise Kit"],
          "origin_feat": "Musician",
          "description": "Hai trascorso la tua vita esibendoti per il pubblico."
        },
        "Guard": {
          "name_it": "Guardia",
          "ability_boosts": ["Forza", "Intelligenza", "Saggezza"],
          "skills": ["Atletica", "Percezione"],
          "tools": ["Gaming Set"],
          "origin_feat": "Alert",
          "description": "Hai protetto persone o luoghi."
        },
        "Guide": {
          "name_it": "Guida",
          "ability_boosts": ["Destrezza", "Costituzione", "Saggezza"],
          "skills": ["Furtività", "Sopravvivenza"],
          "tools": ["Cartographer's Tools"],
          "origin_feat": "Magic Initiate (Druid)",
          "description": "Hai guidato viandanti attraverso terre selvagge."
        },
        "Hermit": {
          "name_it": "Eremita",
          "ability_boosts": ["Costituzione", "Saggezza", "Carisma"],
          "skills": ["Medicina", "Religione"],
          "tools": ["Herbalism Kit"],
          "origin_feat": "Healer",
          "description": "Hai vissuto in isolamento, riflettendo sui misteri della vita."
        },
        "Merchant": {
          "name_it": "Mercante",
          "ability_boosts": ["Costituzione", "Intelligenza", "Carisma"],
          "skills": ["Addestrare Animali", "Persuasione"],
          "tools": ["Navigator's Tools"],
          "origin_feat": "Lucky",
          "description": "Hai viaggiato commerciando beni e servizi."
        },
        "Noble": {
          "name_it": "Nobile",
          "ability_boosts": ["Forza", "Intelligenza", "Carisma"],
          "skills": ["Storia", "Persuasione"],
          "tools": ["Gaming Set"],
          "origin_feat": "Skilled",
          "description": "Sei cresciuto in una famiglia agiata e influente, abituato al potere e al privilegio."
        },
        "Sage": {
          "name_it": "Saggio",
          "ability_boosts": ["Costituzione", "Intelligenza", "Saggezza"],
          "skills": ["Arcano", "Storia"],
          "tools": ["Calligrapher's Supplies"],
          "origin_feat": "Magic Initiate (Wizard)",
          "description": "Hai speso anni imparando il sapere del mondo antico, studiando manoscritti e pergamene."
        },
        "Sailor": {
          "name_it": "Marinaio",
          "ability_boosts": ["Forza", "Destrezza", "Saggezza"],
          "skills": ["Acrobazia", "Percezione"],
          "tools": ["Navigator's Tools", "Water Vehicles"],
          "origin_feat": "Tavern Brawler",
          "description": "Hai navigato in mare aperto per anni, affrontando tempeste e mostri marini."
        },
        "Scribe": {
          "name_it": "Scriba",
          "ability_boosts": ["Destrezza", "Intelligenza", "Saggezza"],
          "skills": ["Indagare", "Percezione"],
          "tools": ["Calligrapher's Supplies"],
          "origin_feat": "Skilled",
          "description": "Hai documentato la storia e trascritto testi importanti."
        },
        "Soldier": {
          "name_it": "Soldato",
          "ability_boosts": ["Forza", "Destrezza", "Costituzione"],
          "skills": ["Atletica", "Intimidire"],
          "tools": ["Gaming Set", "Land Vehicles"],
          "origin_feat": "Savage Attacker",
          "description": "Sei stato addestrato per la guerra e hai visto innumerevoli battaglie."
        },
        "Wayfarer": {
          "name_it": "Viandante",
          "ability_boosts": ["Destrezza", "Saggezza", "Carisma"],
          "skills": ["Intuizione", "Furtività"],
          "tools": ["Thieves' Tools"],
          "origin_feat": "Lucky",
          "description": "Un viaggiatore nomade abituato alla vita sulla strada."
        }
    }

    for k, v in backgrounds.items():
        data['backgrounds'][k] = v
        
    # Also add the new Feats
    new_feats = {
        "Healer": {"description": "Ottieni competenza con il Kit da Guaritore. Puoi usare il kit per curare 1d6 + tuo bonus competenza Punti Ferita."},
        "Magic Initiate (Druid)": {"description": "Impari due trucchetti e un incantesimo di 1° livello dalla lista del Druido."},
        "Lucky": {"description": "Ottieni Punti Fortuna pari al tuo Bonus Competenza. Puoi spenderli per ottenere vantaggio a un d20 o svantaggio a un attacco contro di te."}
    }
    
    for k, v in new_feats.items():
        data['feats'][k] = v

    with open('data/rules_2024.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
if __name__ == "__main__":
    update_rules()
