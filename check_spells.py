import json
with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Spells keys:', list(data.get('spells', {}).keys()))
cantrips = data.get('spells', {}).get('Cantrip', {})
print('Cantrip count:', len(cantrips))
if cantrips:
    print('Sample cantrip classes:', list(cantrips.values())[0]['classes'])
lvl1 = data.get('spells', {}).get('Level 1', {})
print('Level 1 count:', len(lvl1))
if lvl1:
    print('Sample Level 1 classes:', list(lvl1.values())[0]['classes'])
