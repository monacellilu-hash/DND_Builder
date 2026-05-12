import json
import codecs

path = 'data/rules_2024.json'
with codecs.open(path, 'r', 'utf-8') as f:
    data = json.load(f)

if 'Cantrip' in data.get('spells', {}):
    if 'Cantrips' not in data['spells']:
        data['spells']['Cantrips'] = {}
    for k, v in data['spells']['Cantrip'].items():
        data['spells']['Cantrips'][k] = v
    del data['spells']['Cantrip']

with codecs.open(path, 'w', 'utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("Merged Cantrips.")
