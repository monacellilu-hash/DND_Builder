import json
import codecs

path = 'data/rules_2024.json'
with codecs.open(path, 'r', 'utf-8') as f:
    data = json.load(f)

it_to_en = {
    'barbaro': 'Barbarian',
    'bardo': 'Bard',
    'chierico': 'Cleric',
    'druido': 'Druid',
    'guerriero': 'Fighter',
    'monaco': 'Monk',
    'paladino': 'Paladin',
    'ranger': 'Ranger',
    'ladro': 'Rogue',
    'stregone': 'Sorcerer',
    'warlock': 'Warlock',
    'mago': 'Wizard'
}

count = 0
for lvl, spells in data.get('spells', {}).items():
    for s_name, s_data in spells.items():
        new_classes = []
        for c in s_data.get('classes', []):
            # c could be something like "Mago", " Stregone", "Warlock"
            for c_part in c.split(','):
                c_lower = c_part.lower().strip()
                if c_lower in it_to_en:
                    new_classes.append(it_to_en[c_lower])
                elif c_lower == 'artificer' or c_lower == 'artefice':
                    new_classes.append('Artificer')
                else:
                    for en_val in it_to_en.values():
                        if c_lower == en_val.lower():
                            new_classes.append(en_val)
                            break
        s_data['classes'] = list(set(new_classes))
        count += 1

with codecs.open(path, 'w', 'utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f'Fixed classes for {count} spells.')
