import json

with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

if 'trait_options' not in rules:
    rules['trait_options'] = {}

rules['trait_options']["Versatile"] = {
    "origin_feat": 1,
    "skill_choices": 1
}
rules['trait_options']["Versatilità nelle Abilità (Skill Versatility)"] = {
    "skill_choices": 2
}
rules['trait_options']["Istinti Cangianti (Changeling Instincts)"] = {
    "skill_options": ["Inganno", "Intimidire", "Intuizione", "Persuasione"],
    "skill_choices": 2
}
rules['trait_options']["Talento del Gatto (Cat's Talent)"] = {
    "skills_granted": ["Percezione", "Furtività"]
}
rules['trait_options']["Keen Senses"] = {
    "skills_granted": ["Percezione"]
}
rules['trait_options']["Portatore di Luce (Light Bearer)"] = {
    "cantrips_granted": ["Luce"]
}

with open('data/rules_2024.json', 'w', encoding='utf-8') as f:
    json.dump(rules, f, indent=2, ensure_ascii=False)
