import json
import os

path = 'data/rules_2024.json'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

legacy_species = {
  'Aasimar': {
    'name_it': 'Aasimar',
    'speed': 30,
    'traits': ['Scurovisione (Darkvision)', 'Resistenza Celestiale (Celestial Resistance)', 'Mani Guaritrici (Healing Hands)', 'Portatore di Luce (Light Bearer)', 'Rivelazione Celestiale (Celestial Revelation)'],
    'description': 'Mortali dal retaggio celestiale, dotati di ali luminose o poteri divini latenti. (Manuale 2024)'
  },
  'Half-Elf': {
    'name_it': 'Mezzelfo',
    'speed': 30,
    'traits': ['Scurovisione (Darkvision)', 'Ascendenza Fatata (Fey Ancestry - Regole 2024)', 'Versatilità nelle Abilità (Skill Versatility)'],
    'description': 'Camminano tra due mondi, possedendo la creatività umana e la grazia elfica. (Legacy 2014)'
  },
  'Half-Orc': {
    'name_it': 'Mezzorco',
    'speed': 30,
    'traits': ['Scurovisione (Darkvision)', 'Tenacia Implacabile (Relentless Endurance)', 'Attacchi Selvaggi (Savage Attacks)'],
    'description': 'Fieri e resistenti, uniscono la determinazione umana con la forza orchesca. (Legacy 2014)'
  },
  'Genasi (Air)': {
    'name_it': 'Genasi dell\'Aria',
    'speed': 35,
    'traits': ['Scurovisione (Darkvision)', 'Respiro Inesauribile (Unending Breath)', 'Resistenza al Fulmine', 'Mescolarsi con il Vento (Mingle with the Wind)'],
    'description': 'Umanoidi con retaggio elementale dell\'Aria, agili e capaci di trattenere il respiro all\'infinito. (MotM)'
  },
  'Genasi (Earth)': {
    'name_it': 'Genasi della Terra',
    'speed': 30,
    'traits': ['Scurovisione (Darkvision)', 'Camminare sulla Terra (Earth Walk)', 'Fondersi con la Pietra (Merge with Stone)'],
    'description': 'Umanoidi con retaggio elementale della Terra, robusti e stabili. (MotM)'
  },
  'Genasi (Fire)': {
    'name_it': 'Genasi del Fuoco',
    'speed': 30,
    'traits': ['Scurovisione (Darkvision)', 'Resistenza al Fuoco', 'Tendere alla Fiamma (Reach to the Blaze)'],
    'description': 'Umanoidi con retaggio elementale del Fuoco, dal temperamento ardente. (MotM)'
  },
  'Genasi (Water)': {
    'name_it': 'Genasi dell\'Acqua',
    'speed': 30,
    'traits': ['Scurovisione (Darkvision)', 'Resistenza all\'Acido', 'Anfibio (Amphibious)', 'Velocità di Nuoto 30 ft', 'Richiamo dell\'Onda (Call to the Wave)'],
    'description': 'Umanoidi con retaggio elementale dell\'Acqua, nati per nuotare e dominare le onde. (MotM)'
  },
  'Tabaxi': {
    'name_it': 'Tabaxi',
    'speed': 30,
    'traits': ['Scurovisione (Darkvision)', 'Agilità Felina (Feline Agility)', 'Artigli del Gatto (Cat\'s Claws)', 'Talento del Gatto (Cat\'s Talent)'],
    'description': 'Umanoidi felini guidati dalla curiosità e un forte desiderio di scoprire antichi segreti. (MotM)'
  },
  'Goblin': {
    'name_it': 'Goblin',
    'speed': 30,
    'traits': ['Scurovisione (Darkvision)', 'Ascendenza Fatata (Fey Ancestry - Regole 2024)', 'Fuga Agile (Nimble Escape)', 'Furia dei Piccoli (Fury of the Small)'],
    'description': 'Piccoli umanoidi furbi e sfuggenti, spesso associati a creature fatate. (MotM)'
  },
  'Changeling': {
    'name_it': 'Cangiante (Changeling)',
    'speed': 30,
    'traits': ['Mutaforma (Shapechanger)', 'Istinti Cangianti (Changeling Instincts)'],
    'description': 'Maestri del travestimento in grado di mutare il proprio aspetto a piacimento. (MotM)'
  },
  'Dhampir': {
    'name_it': 'Dhampir',
    'speed': 35,
    'traits': ['Scurovisione (Darkvision)', 'Movimenti del Ragno (Spider Climb)', 'Morso Vampirico (Vampiric Bite)'],
    'description': 'Creature a metà tra i vivi e i non morti, guidate da una fame inesauribile. (VRGtR)'
  },
  'Hexblood': {
    'name_it': 'Sangue Malefico (Hexblood)',
    'speed': 30,
    'traits': ['Scurovisione (Darkvision)', 'Ascendenza Fatata (Fey Ancestry - Regole 2024)', 'Pegno Inquietante (Eerie Token)', 'Magia Malefica (Hex Magic)'],
    'description': 'Umanoidi intrisi di magia fatata o stregonesca. (VRGtR)'
  },
  'Reborn': {
    'name_it': 'Rinato (Reborn)',
    'speed': 30,
    'traits': ['Scurovisione (Darkvision)', 'Natura Immortale (Deathless Nature)', 'Conoscenza da una Vita Passata (Knowledge from a Past Life)'],
    'description': 'Individui tornati dalla morte ma che conservano ancora frammenti della vita passata. (VRGtR)'
  }
}

for k, v in legacy_species.items():
    data['species'][k] = v

species_extras = {
    'Human': {'size': 'Media', 'languages': ['Comune', '1 Lingua a scelta']},
    'Elf': {'size': 'Media', 'languages': ['Comune', 'Elfico']},
    'Dwarf': {'size': 'Media', 'languages': ['Comune', 'Nanico']},
    'Halfling': {'size': 'Piccola', 'languages': ['Comune', 'Halfling']},
    'Dragonborn': {'size': 'Media', 'languages': ['Comune', 'Draconico']},
    'Orc': {'size': 'Media', 'languages': ['Comune', 'Orchesco']},
    'Tiefling': {'size': 'Media', 'languages': ['Comune', 'Infernale']},
    'Gnome': {'size': 'Piccola', 'languages': ['Comune', 'Gnomesco']},
    'Goliath': {'size': 'Media', 'languages': ['Comune', 'Gigante']},
    'Aasimar': {'size': 'Media', 'languages': ['Comune', 'Celestiale']},
    'Half-Elf': {'size': 'Media', 'languages': ['Comune', 'Elfico', '1 Lingua a scelta']},
    'Half-Orc': {'size': 'Media', 'languages': ['Comune', 'Orchesco']},
    'Genasi (Air)': {'size': 'Media', 'languages': ['Comune', 'Primordiale']},
    'Genasi (Earth)': {'size': 'Media', 'languages': ['Comune', 'Primordiale']},
    'Genasi (Fire)': {'size': 'Media', 'languages': ['Comune', 'Primordiale']},
    'Genasi (Water)': {'size': 'Media', 'languages': ['Comune', 'Primordiale']},
    'Tabaxi': {'size': 'Media', 'languages': ['Comune', '1 Lingua a scelta']},
    'Goblin': {'size': 'Piccola', 'languages': ['Comune', 'Goblin']},
    'Changeling': {'size': 'Media', 'languages': ['Comune', '2 Lingue a scelta']},
    'Dhampir': {'size': 'Media o Piccola', 'languages': ['Comune', '1 Lingua a scelta']},
    'Hexblood': {'size': 'Media o Piccola', 'languages': ['Comune', 'Silvano']},
    'Reborn': {'size': 'Media o Piccola', 'languages': ['Comune', '1 Lingua a scelta']}
}

for k, v in species_extras.items():
    if k in data['species']:
        data['species'][k].update(v)

class_extras = {
    'Barbarian': {'armor_prof': ['Armature Leggere', 'Armature Medie', 'Scudi'], 'weapon_prof': ['Armi Semplici', 'Armi da Guerra'], 'equipment': 'Ascia Bipenne, 2 Asce, Zaino da Esploratore, 4 Dardi'},
    'Bard': {'armor_prof': ['Armature Leggere'], 'weapon_prof': ['Armi Semplici', 'Spade Corte', 'Stocchi', 'Balestre a Mano', 'Spade Lunghe'], 'equipment': 'Stocco, Abiti Pregiati, Strumento Musicale, Zaino da Intrattenitore'},
    'Cleric': {'armor_prof': ['Armature Leggere', 'Armature Medie', 'Scudi'], 'weapon_prof': ['Armi Semplici'], 'equipment': 'Mazza, Armatura a Scaglie, Balestra Leggera, Zaino da Sacerdote, Simbolo Sacro'},
    'Druid': {'armor_prof': ['Armature Leggere', 'Armature Medie (non di metallo)', 'Scudi (non di metallo)'], 'weapon_prof': ['Armi Semplici', 'Scimitarre'], 'equipment': 'Scudo di Legno, Scimitarra, Armatura di Cuoio, Zaino da Esploratore, Focus Druidico'},
    'Fighter': {'armor_prof': ['Tutte le Armature', 'Scudi'], 'weapon_prof': ['Armi Semplici', 'Armi da Guerra'], 'equipment': 'Cotta di Maglia, Spadone, Scudo, Balestra Leggera, Zaino da Dungeoneer'},
    'Monk': {'armor_prof': ['Nessuna'], 'weapon_prof': ['Armi Semplici', 'Spade Corte'], 'equipment': 'Spada Corta, 10 Dardi, Zaino da Esploratore'},
    'Paladin': {'armor_prof': ['Tutte le Armature', 'Scudi'], 'weapon_prof': ['Armi Semplici', 'Armi da Guerra'], 'equipment': 'Spada Lunga, Scudo, Giaco di Maglia, Zaino da Sacerdote, Simbolo Sacro'},
    'Ranger': {'armor_prof': ['Armature Leggere', 'Armature Medie', 'Scudi'], 'weapon_prof': ['Armi Semplici', 'Armi da Guerra'], 'equipment': 'Armatura a Scaglie, Due Spade Corte, Arco Lungo, Zaino da Esploratore'},
    'Rogue': {'armor_prof': ['Armature Leggere'], 'weapon_prof': ['Armi Semplici', 'Spade Corte', 'Stocchi', 'Balestre a Mano'], 'equipment': 'Stocco, Arco Corto, Armatura di Cuoio, Arnesi da Scasso, Zaino da Scassinatore'},
    'Sorcerer': {'armor_prof': ['Nessuna'], 'weapon_prof': ['Pugnali', 'Dardi', 'Fionde', 'Bastoni Ferrati', 'Balestre Leggere'], 'equipment': 'Balestra Leggera, Focus Arcano, Zaino da Esploratore, 2 Pugnali'},
    'Warlock': {'armor_prof': ['Armature Leggere'], 'weapon_prof': ['Armi Semplici'], 'equipment': 'Balestra Leggera, Focus Arcano, Zaino da Studioso, Armatura di Cuoio, 2 Pugnali'},
    'Wizard': {'armor_prof': ['Nessuna'], 'weapon_prof': ['Pugnali', 'Dardi', 'Fionde', 'Bastoni Ferrati', 'Balestre Leggere'], 'equipment': 'Bastone Ferrato, Focus Arcano, Libro degli Incantesimi, Zaino da Studioso'}
}

for k, v in class_extras.items():
    if k in data['classes']:
        data['classes'][k].update(v)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
