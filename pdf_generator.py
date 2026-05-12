import fitz
from fpdf import FPDF
import math

def calculate_modifier(score):
    return (score - 10) // 2

def generate_spells_pdf(char, rules):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(139, 0, 0)
    
    name = char.get("name", "Eroe")
    cls_name = char.get("class", "")
    
    pdf.cell(0, 10, f"Incantesimi: {name}", ln=True, align='C')
    pdf.ln(5)
    
    # 1. Incantesimi Scelti
    pdf.set_font("helvetica", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, "Incantesimi Conosciuti (Scelti)", ln=True)
    pdf.ln(2)
    
    char_spells_grouped = { 'Cantrips': char.get('cantrips', []) }
    for i in range(1, 10):
        char_spells_grouped[f'Level {i}'] = []
    
    for s in char.get('spells', []):
        if ": " in s:
            lvl, sname = s.split(": ", 1)
            if lvl in char_spells_grouped:
                char_spells_grouped[lvl].append(sname)
                
    has_spells = False
    for lvl_name in ['Cantrips', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 9']:
        spells_in_lvl = char_spells_grouped.get(lvl_name, [])
        if spells_in_lvl:
            has_spells = True
            pdf.set_font("helvetica", 'B', 12)
            pdf.set_text_color(139, 0, 0)
            pdf.cell(0, 6, f"--- {lvl_name} ---", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
            
            for s_name in sorted(spells_in_lvl):
                desc = rules.get('spells', {}).get(lvl_name, {}).get(s_name, {}).get('description', '')
                pdf.set_font("helvetica", 'B', 11)
                clean_s_name = s_name.encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(0, 6, clean_s_name, ln=True)
                pdf.set_font("helvetica", '', 10)
                clean_desc = desc.encode('latin-1', 'replace').decode('latin-1')
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(0, 6, clean_desc)
                pdf.ln(2)
                
    if not has_spells:
        pdf.set_font("helvetica", '', 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, "Nessun incantesimo conosciuto.", ln=True)
        pdf.ln(2)
        
    pdf.ln(5)
    
    # 2. Tutti gli incantesimi disponibili per la classe
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Lista Completa Incantesimi Disponibili ({cls_name})", ln=True)
    pdf.ln(2)
    
    if cls_name == "Seleziona..." or not cls_name:
        pdf.set_font("helvetica", '', 11)
        pdf.cell(0, 8, "Nessuna classe selezionata.", ln=True)
    else:
        for lvl_name in ['Cantrips', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 9']:
            spells_in_lvl = []
            for s_name, s_dict in rules.get('spells', {}).get(lvl_name, {}).items():
                if cls_name in s_dict.get('classes', []):
                    spells_in_lvl.append((s_name, s_dict.get('description', '')))
            
            if spells_in_lvl:
                pdf.set_font("helvetica", 'B', 12)
                pdf.set_text_color(139, 0, 0)
                pdf.cell(0, 6, f"--- {lvl_name} ---", ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(2)
                
                for s_name, s_desc in sorted(spells_in_lvl, key=lambda x: x[0]):
                    pdf.set_font("helvetica", 'B', 11)
                    clean_s_name = s_name.encode('latin-1', 'replace').decode('latin-1')
                    pdf.cell(0, 6, clean_s_name, ln=True)
                    pdf.set_font("helvetica", '', 10)
                    clean_desc = s_desc.encode('latin-1', 'replace').decode('latin-1')
                    pdf.set_x(pdf.l_margin)
                    pdf.multi_cell(0, 6, clean_desc)
                    pdf.ln(2)
                    
    out = pdf.output()
    if isinstance(out, str):
        return out.encode('latin-1')
    return bytes(out)

def generate_progression_pdf(char, rules):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(139, 0, 0)
    
    name = char.get("name", "Eroe")
    cls_name = char.get("class", "")
    subclass = char.get("subclass", "")
    
    pdf.cell(0, 10, f"Progressione: {name} - {cls_name} {subclass if subclass != 'Seleziona...' else ''}", ln=True, align='C')
    pdf.ln(10)
    
    if cls_name == "Seleziona...":
        pdf.set_font("helvetica", '', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "Nessuna classe selezionata.", ln=True)
        return bytes(pdf.output())
        
    cdata = rules['classes'].get(cls_name, {})
    
    for l in range(1, 21):
        pdf.set_font("helvetica", 'B', 12)
        pdf.set_text_color(139, 0, 0)
        pdf.cell(0, 8, f"Livello {l}", ln=True, border='B')
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("helvetica", '', 10)
        
        feat = cdata.get("features", {}).get(str(l), "")
        if feat:
            pdf.set_x(pdf.l_margin)
            clean_feat = feat.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 6, f"Privilegi: {clean_feat}")
            
        if l == 3 and subclass == "Seleziona..." and "subclasses" in cdata:
            sub_names = list(cdata["subclasses"].keys())
            pdf.set_x(pdf.l_margin)
            clean_sub_names = ", ".join(sub_names).encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 6, f"Sottoclassi disponibili da sbloccare: {clean_sub_names}")
            
        if subclass != "Seleziona...":
            sub_feat = cdata.get("subclasses", {}).get(subclass, {}).get("level_features", {}).get(str(l), "")
            if sub_feat:
                pdf.set_x(pdf.l_margin)
                clean_sub_feat = sub_feat.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 6, f"Sottoclasse ({subclass}): {clean_sub_feat}")
                
        pdf.ln(3)

    out = pdf.output()
    if isinstance(out, str):
        return out.encode('latin-1')
    return bytes(out)

def generate_pdf(char, rules):
    try:
        doc = fitz.open('DND_2024_Sheet_Compilabile.pdf')
    except Exception:
        doc = fitz.open('../Dati_Input/scheda-personaggio.pdf')
    
    level = char.get('level', 1)
    prof_bonus = 2 + ((level - 1) // 4)
    final_abilities = {ab: char['abilities'].get(ab, 8) + char['background_boosts'].get(ab, 0) for ab in rules['abilities']}
    mods = {ab: calculate_modifier(final_abilities[ab]) for ab in rules['abilities']}
    
    cls_name = char.get("class", "Seleziona...")
    bg = char.get("background", "Seleziona...")
    species = char.get("species", "Seleziona...")
    
    hit_die = rules['classes'].get(cls_name, {}).get('hit_die', 8) if cls_name != "Seleziona..." else 8
    max_hp = math.floor((hit_die + mods["Costituzione"]) + ((hit_die / 2 + 1) + mods["Costituzione"]) * (level - 1))
    
    origin_feat = rules['backgrounds'].get(bg, {}).get('origin_feat', '') if bg != "Seleziona..." else ""
    if origin_feat == "Tough" or "Tough" in char.get('feats', []):
        max_hp += 2 * level
        
    ac = 10 + mods["Destrezza"]
    if cls_name == "Barbarian": ac = 10 + mods["Destrezza"] + mods["Costituzione"]
    elif cls_name == "Monk": ac = 10 + mods["Destrezza"] + mods["Saggezza"]
    elif char.get("subclass") == "Stregoneria Draconica": ac = 13 + mods["Destrezza"]
    
    initiative = mods["Destrezza"]
    if origin_feat == "Alert" or "Alert" in char.get('feats', []): initiative += prof_bonus
    
    speed = rules['species'].get(species, {}).get('speed', 30) if species != "Seleziona..." else 30
    passive_perception = 10 + mods["Saggezza"] + (prof_bonus if "Percezione" in char.get('skills', []) else 0)
    
    class_level_str = f"{rules['classes'].get(cls_name, {}).get('name_it', cls_name)} {level}" if cls_name != "Seleziona..." else ""
    
    field_map = {
        'CharacterName': char.get('name', ''),
        'ClassLevel': class_level_str,
        'Background': rules['backgrounds'].get(bg, {}).get('name_it', bg) if bg != "Seleziona..." else "",
        'Race ': rules['species'].get(species, {}).get('name_it', species) if species != "Seleziona..." else "",
        'STR': str(final_abilities['Forza']),
        'DEX': str(final_abilities['Destrezza']),
        'CON': str(final_abilities['Costituzione']),
        'INT': str(final_abilities['Intelligenza']),
        'WIS': str(final_abilities['Saggezza']),
        'CHA': str(final_abilities['Carisma']),
        'STRmod': f"{mods['Forza']:+}",
        'DEXmod': f"{mods['Destrezza']:+}",
        'CONmod': f"{mods['Costituzione']:+}",
        'INTmod': f"{mods['Intelligenza']:+}",
        'WISmod': f"{mods['Saggezza']:+}",
        'CHAmod': f"{mods['Carisma']:+}",
        'ProfBonus': f"+{prof_bonus}",
        'AC': str(ac),
        'Initiative': f"{initiative:+}",
        'Speed': str(speed),
        'HPMax': str(max_hp),
        'HPCurrent': str(max_hp),
        'HDTotal': str(level),
        'HD': f"d{hit_die}",
        'Passive': str(passive_perception)
    }
    
    skills = char.get('skills', [])
    skill_fields = {
        'Acrobazia': 'ACRO', 'Addestrare Animali': 'ANIM', 'Arcano': 'ARC', 'Atletica': 'ATH',
        'Furtività': 'STLTH', 'Indagare': 'INV', 'Inganno': 'DEC', 'Intimidire': 'INTI',
        'Intrattenere': 'PERF', 'Intuizione': 'INS', 'Medicina': 'MED', 'Natura': 'NAT',
        'Percezione': 'PERC', 'Persuasione': 'PERS', 'Rapidità di Mano': 'SLE',
        'Religione': 'REL', 'Sopravvivenza': 'SURV', 'Storia': 'HIST'
    }
    
    for skill_name, field_prefix in skill_fields.items():
        if skill_name in rules['skills']:
            base_stat = rules['skills'][skill_name]
            is_prof = skill_name in skills
            val = mods[base_stat] + (prof_bonus if is_prof else 0)
            field_map[field_prefix] = f"{val:+}"
            if is_prof:
                field_map[f"{field_prefix}P"] = True

    # Saving Throws
    cdata = rules['classes'].get(cls_name, {})
    saving_throws = cdata.get('saving_throws', [])
    st_fields = {
        'Forza': 'ST Strength', 'Destrezza': 'ST Dexterity', 'Costituzione': 'ST Constitution',
        'Intelligenza': 'ST Intelligence', 'Saggezza': 'ST Wisdom', 'Carisma': 'ST Charisma'
    }
    for st_name, field_name in st_fields.items():
        is_prof = st_name in saving_throws
        val = mods[st_name] + (prof_bonus if is_prof else 0)
        field_map[field_name] = f"{val:+}"
            
    traits_text = ""
    for t in rules['species'].get(species, {}).get('traits', []):
            t_desc = rules.get('trait_descriptions', {}).get(t, '')
            if t_desc:
                traits_text += f"- {t}: {t_desc}\n"
            else:
                traits_text += f"- {t}\n"
    if origin_feat:
        traits_text += f"- {origin_feat}\n"
    for f in char.get('feats', []):
        traits_text += f"- {f}\n"
        
    for l in range(1, level + 1):
        feat = cdata.get("features", {}).get(str(l), "")
        if feat and not feat.startswith("Privilegio di"):
            traits_text += f"Lv {l}: {feat}\n"
    field_map['Features and Traits'] = traits_text
    
    field_map['Equipment'] = cdata.get('equipment', '')
    
    prof_text = ""
    armor_prof = cdata.get('armor_prof', [])
    weapon_prof = cdata.get('weapon_prof', [])
    langs = rules['species'].get(species, {}).get('languages', [])
    
    prof_text += f"Armature: {', '.join(armor_prof)}\n\n"
    prof_text += f"Armi: {', '.join(weapon_prof)}\n\n"
    prof_text += f"Lingue: {', '.join(langs)}\n"
    field_map['ProficienciesLang'] = prof_text
    
    spellcasting = cdata.get('spellcasting', 'none')
    if spellcasting != 'none':
        sa = ""
        if cls_name in ["Bard", "Paladin", "Sorcerer", "Warlock"]: sa = "Carisma"
        elif cls_name in ["Cleric", "Druid", "Ranger"]: sa = "Saggezza"
        elif cls_name == "Wizard": sa = "Intelligenza"
        
        if sa:
            dc = 8 + prof_bonus + mods.get(sa, 0)
            atk = prof_bonus + mods.get(sa, 0)
            field_map['Spellcasting Class 2'] = cls_name
            field_map['SpellcastingAbility 2'] = sa
            field_map['SpellSaveDC  2'] = str(dc)
            field_map['SpellAtkBonus 2'] = f"+{atk}"
            
        # Spells fields mapping
        spell_field_mapping = {
            'Cantrips': [f'Spells 10{i}' for i in range(14, 23)],
            'Level 1': [f'Spells 10{i}' for i in range(23, 34)],
            'Level 2': [f'Spells 10{i}' for i in range(34, 47)],
            'Level 3': [f'Spells 10{i}' for i in range(47, 60)],
            'Level 4': [f'Spells 10{i}' for i in range(60, 73)],
            'Level 5': [f'Spells 10{i}' for i in range(73, 82)],
            'Level 6': [f'Spells 10{i}' for i in range(82, 91)],
            'Level 7': [f'Spells 10{i}' for i in range(91, 100)],
            'Level 8': [f'Spells 10{i}' for i in range(100, 107)],
            'Level 9': [f'Spells 10{i}' for i in range(107, 115)]
        }
        
        char_spells_grouped = { 'Cantrips': char.get('cantrips', []) }
        for i in range(1, 10):
            char_spells_grouped[f'Level {i}'] = []
        
        for s in char.get('spells', []):
            if ": " in s:
                lvl, sname = s.split(": ", 1)
                if lvl in char_spells_grouped:
                    char_spells_grouped[lvl].append(sname)
                    
        for lvl, f_names in spell_field_mapping.items():
            spells_for_lvl = char_spells_grouped.get(lvl, [])
            for i, s_name in enumerate(spells_for_lvl):
                if i < len(f_names):
                    field_map[f_names[i]] = s_name

    for page in doc:
        for field in page.widgets():
            if field.field_name in field_map:
                try:
                    val = field_map[field.field_name]
                    if type(val) == bool:
                        field.field_value = val
                    else:
                        field.field_value = str(val)
                    field.update()
                except:
                    pass
                    
    return doc.tobytes()
