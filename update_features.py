import json

with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

asi_levels = [4, 8, 12, 16, 19]

def add_asi(features, class_name):
    levels = asi_levels.copy()
    if class_name == "Fighter":
        levels.extend([6, 14])
    elif class_name == "Rogue":
        levels.append(10)
    
    for lvl in levels:
        if str(lvl) in features and features[str(lvl)]:
            if "Miglioramento dei Punteggi di Caratteristica" not in features[str(lvl)]:
                features[str(lvl)] += ", Miglioramento dei Punteggi di Caratteristica o Talento"
        else:
            features[str(lvl)] = "Miglioramento dei Punteggi di Caratteristica o Talento"

classes_progression = {
    "Barbarian": {
        1: "Ira (Rage), Difesa Senza Armatura, Padronanza delle Armi",
        2: "Senso del Pericolo, Attacco Irruento",
        3: "Sottoclasse Barbarica, Conoscenza Primordiale",
        5: "Attacco Extra, Movimento Veloce",
        6: "Privilegio di Sottoclasse",
        7: "Istinto Feroce",
        9: "Critico Brutale (1 dado)",
        10: "Privilegio di Sottoclasse",
        11: "Ira Implacabile",
        13: "Critico Brutale (2 dadi)",
        14: "Privilegio di Sottoclasse",
        15: "Ira Persistente",
        17: "Critico Brutale (3 dadi)",
        18: "Potenza Indomita",
        20: "Campione Primordiale (+4 Forza e Costituzione)"
    },
    "Bard": {
        1: "Ispirazione Bardica, Incantesimi",
        2: "Tuttofare, Canto di Riposo",
        3: "Sottoclasse Bardica, Maestria",
        5: "Fonte di Ispirazione",
        6: "Controfascinazione, Privilegio di Sottoclasse",
        10: "Segreti Magici, Maestria",
        14: "Segreti Magici, Privilegio di Sottoclasse",
        18: "Segreti Magici",
        20: "Ispirazione Superiore"
    },
    "Cleric": {
        1: "Incantesimi",
        2: "Incanalare Divinità",
        3: "Sottoclasse Chierico (Dominio Divino)",
        5: "Distruggere Non Morti",
        6: "Incanalare Divinità (2 usi), Privilegio di Dominio",
        8: "Distruggere Non Morti Migliorato",
        10: "Intervento Divino",
        14: "Distruggere Non Morti",
        17: "Privilegio di Dominio",
        18: "Incanalare Divinità (3 usi)",
        20: "Intervento Divino Infallibile"
    },
    "Druid": {
        1: "Druidico, Incantesimi",
        2: "Forma Selvatica",
        3: "Sottoclasse Druidica (Circolo)",
        6: "Privilegio di Circolo",
        10: "Privilegio di Circolo",
        14: "Privilegio di Circolo",
        18: "Incantesimi Bestiali",
        20: "Arcidruido"
    },
    "Fighter": {
        1: "Stile di Combattimento, Recuperare Energie, Padronanza delle Armi",
        2: "Azione Impetuosa",
        3: "Sottoclasse Guerriero (Archetipo Marziale)",
        5: "Attacco Extra (1)",
        7: "Privilegio di Archetipo",
        9: "Indomito (1 uso)",
        10: "Privilegio di Archetipo",
        11: "Attacco Extra (2)",
        13: "Indomito (2 usi)",
        15: "Privilegio di Archetipo",
        17: "Azione Impetuosa (2 usi), Indomito (3 usi)",
        18: "Privilegio di Archetipo",
        20: "Attacco Extra (3)"
    },
    "Monk": {
        1: "Arti Marziali, Difesa Senza Armatura",
        2: "Ki, Movimento Senza Armatura",
        3: "Sottoclasse Monaco (Tradizione Monastica), Deviare Proiettili",
        4: "Caduta Lenta",
        5: "Attacco Extra, Colpo Stordente",
        6: "Colpi Ki-Migliorati, Privilegio di Tradizione",
        7: "Elusione, Mente Lucida",
        10: "Purezza del Corpo",
        11: "Privilegio di Tradizione",
        13: "Linguaggio del Sole e della Luna",
        14: "Anima di Diamante",
        15: "Corpo Senza Tempo",
        17: "Privilegio di Tradizione",
        18: "Corpo Vuoto",
        20: "Perfezione Perfetta"
    },
    "Paladin": {
        1: "Senso Divino, Imposizione delle Mani, Padronanza delle Armi",
        2: "Stile di Combattimento, Punizione Divina, Incantesimi",
        3: "Salute Divina, Sottoclasse Paladino (Giuramento Sacro)",
        5: "Attacco Extra",
        6: "Aura di Protezione",
        7: "Privilegio di Giuramento",
        10: "Aura di Coraggio",
        11: "Punizione Divina Migliorata",
        14: "Tocco Purificatore",
        15: "Privilegio di Giuramento",
        18: "Estensione delle Auree",
        20: "Privilegio di Giuramento Supremo"
    },
    "Ranger": {
        1: "Nemico Prescelto, Esploratore Naturale, Padronanza delle Armi",
        2: "Stile di Combattimento, Incantesimi",
        3: "Sottoclasse Ranger (Archetipo), Consapevolezza Primordiale",
        5: "Attacco Extra",
        7: "Privilegio di Archetipo",
        8: "Andatura sul Terreno",
        10: "Mimetismo Naturale",
        11: "Privilegio di Archetipo",
        14: "Svanire",
        15: "Privilegio di Archetipo",
        18: "Sensi Ferini",
        20: "Uccisore di Nemici"
    },
    "Rogue": {
        1: "Maestria, Attacco Furtivo, Gergo dei Ladri, Padronanza delle Armi",
        2: "Azione Scaltra",
        3: "Sottoclasse Ladro (Archetipo Ladresco), Mira Stabile",
        5: "Schivata Prodigiosa",
        7: "Elusione",
        9: "Privilegio di Archetipo",
        11: "Dote Affidabile",
        13: "Privilegio di Archetipo",
        14: "Senso Cieco",
        15: "Mente Sfuggente",
        17: "Privilegio di Archetipo",
        18: "Sfuggente",
        20: "Colpo di Fortuna"
    },
    "Sorcerer": {
        1: "Magia Innata, Incantesimi",
        2: "Fonte di Magia",
        3: "Sottoclasse Stregone (Origine Stregonesca), Metamagia (2 opzioni)",
        6: "Privilegio di Origine",
        10: "Metamagia (3a opzione)",
        14: "Privilegio di Origine",
        17: "Metamagia (4a opzione)",
        18: "Privilegio di Origine",
        20: "Ripristino Stregonesco"
    },
    "Warlock": {
        1: "Magia del Patto, Suppliche Occulte (Eldritch Invocations)",
        2: "Magical Cunning",
        3: "Sottoclasse Warlock (Patrono Ultraterreno)",
        6: "Privilegio del Patrono",
        10: "Privilegio del Patrono",
        11: "Arcanum Mistico (6° livello)",
        13: "Arcanum Mistico (7° livello)",
        14: "Privilegio del Patrono",
        15: "Arcanum Mistico (8° livello)",
        17: "Arcanum Mistico (9° livello)",
        20: "Maestro Occulto (Eldritch Master)"
    },
    "Wizard": {
        1: "Recupero Arcano, Incantesimi",
        2: "Studioso",
        3: "Sottoclasse Mago (Tradizione Arcana)",
        6: "Privilegio di Tradizione",
        10: "Privilegio di Tradizione",
        14: "Privilegio di Tradizione",
        18: "Padronanza degli Incantesimi",
        20: "Firma Magica"
    }
}

for cls in data['classes']:
    prog = classes_progression.get(cls, {})
    features = {}
    for lvl in range(1, 21):
        if lvl in prog:
            features[str(lvl)] = prog[lvl]
        else:
            features[str(lvl)] = ""
    add_asi(features, cls)
    data['classes'][cls]['features'] = features

data['classes']['Warlock']['subclasses'] = {
    "Il Fiend (Immondo)": {
        "description": "Fai un patto con un essere dei piani inferiori. Ottieni punti ferita temporanei quando uccidi un nemico (Benedizione dell'Oscuro).",
        "level_features": {
            "3": "Benedizione dell'Oscuro (Dark One's Blessing)",
            "6": "Fortuna dell'Oscuro (Dark One's Own Luck)",
            "10": "Resistenza Immonda (Fiendish Resilience)",
            "14": "Scagliare all'Inferno (Hurl Through Hell)"
        }
    },
    "Il Grande Antico (Great Old One)": {
        "description": "Un'entità misteriosa e lontana ti conferisce poteri telepatici e magia mentale.",
        "level_features": {
            "3": "Mente Risvegliata (Awakened Mind)",
            "6": "Protezione Entropica (Entropic Ward)",
            "10": "Scudo di Pensieri (Thought Shield)",
            "14": "Creare Schiavo (Create Thrall)"
        }
    }
}

data['classes']['Warlock']['pact_boons'] = {
    "Patto della Lama (Pact of the Blade)": "Puoi creare un'arma magica dal nulla. Diventi competente e puoi usare Carisma per i tiri per colpire e danni.",
    "Patto del Tomo (Pact of the Tome)": "Ottieni un Grimorio con 3 trucchetti extra di qualsiasi classe.",
    "Patto della Catena (Pact of the Chain)": "Impari l'incantesimo Trova Famiglio e puoi scegliere forme speciali come Imp, Quasit o Pseudodrago."
}

with open('data/rules_2024.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
