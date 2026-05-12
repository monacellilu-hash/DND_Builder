import json
import traceback
from pdf_generator import generate_pdf

try:
    with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
        rules = json.load(f)

    char = {
        'name': 'Test',
        'level': 1,
        'class': 'Seleziona...',
        'subclass': 'Seleziona...',
        'species': 'Seleziona...',
        'background': 'Seleziona...',
        'abilities': {ab: 8 for ab in ['Forza', 'Destrezza', 'Costituzione', 'Intelligenza', 'Saggezza', 'Carisma']},
        'background_boosts': {},
        'skills': [],
        'spells': [],
        'feats': [],
        'pact': 'Seleziona...'
    }
    
    generate_pdf(char, rules)
    print("Full generation passed")
except Exception as e:
    traceback.print_exc()
