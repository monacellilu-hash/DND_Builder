import json
import re

def enrich_feats():
    with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Feats that are explicitly known for giving choices
    feat_meta = {
        "Skilled": {"skill_choices": 3},
        "Abile": {"skill_choices": 3}, # In case it's in Italian
        "Crafter": {"tool_choices": 3},
        "Musician": {"tool_choices": 3},
        "Magic Initiate (Cleric)": {"spell_choices": {"class": "Cleric", "cantrips": 2, "level_1": 1}},
        "Magic Initiate (Druid)": {"spell_choices": {"class": "Druid", "cantrips": 2, "level_1": 1}},
        "Magic Initiate (Wizard)": {"spell_choices": {"class": "Wizard", "cantrips": 2, "level_1": 1}},
        # Iniziato alla magia gives choices based on what they select, but we can simplify if needed.
    }

    it_to_en = {
        'Forza': 'Forza',
        'Destrezza': 'Destrezza',
        'Costituzione': 'Costituzione',
        'Intelligenza': 'Intelligenza',
        'Saggezza': 'Saggezza',
        'Carisma': 'Carisma'
    }

    for name, f_data in data.get('feats', {}).items():
        desc = f_data.get('description', '')
        # Check for ASI
        m = re.search(r'punteggio di ([A-Za-z, o]+) aumenta di 1', desc)
        if m:
            raw_stats = m.group(1).replace(' e ', ' o ').split(' o ')
            stats = [s.strip().capitalize() for s in raw_stats if s.strip().capitalize() in it_to_en]
            if stats:
                f_data['asi_choices'] = stats

        if name in feat_meta:
            f_data.update(feat_meta[name])
            
        if "Iniziato alla magia" in name:
            f_data['spell_choices'] = "Any" # Special handling

    with open('data/rules_2024.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print("Feats enriched.")

if __name__ == "__main__":
    enrich_feats()
