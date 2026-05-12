import streamlit as st
import json
import math
import copy
from pdf_generator import generate_pdf, generate_progression_pdf, generate_spells_pdf

st.set_page_config(page_title="D&D 5e (2024) Character Builder", page_icon="🐉", layout="wide")

def add_custom_css():
    st.markdown("""
        <style>
        .stApp { background-color: #fdfbf7; color: #3e2723; }
        h1, h2, h3 { color: #b71c1c; font-family: 'Georgia', serif; }
        .stat-box { background-color: #fffaf0; border: 2px solid #b71c1c; border-radius: 10px; padding: 10px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px; }
        .stat-value { font-size: 24px; font-weight: bold; color: #b71c1c; }
        .stat-label { font-size: 12px; font-weight: bold; text-transform: uppercase; }
        hr { border-top: 2px solid #b71c1c; opacity: 0.3; }
        </style>
    """, unsafe_allow_html=True)

def load_rules():
    import csv
    with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
        rules = json.load(f)
        
    rules['spells'] = {'Cantrips': {}}
    for i in range(1, 10):
        rules['spells'][f'Level {i}'] = {}
        
    class_mapping = {
        "bardo": "Bard",
        "chierico": "Cleric",
        "druido": "Druid",
        "paladino": "Paladin",
        "ranger": "Ranger",
        "stregone": "Sorcerer",
        "warlock": "Warlock",
        "mago": "Wizard",
        "artefice": "Artificer"
    }
        
    try:
        with open('Incantesimi_Tutti.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lvl_val = str(row.get('Livello', '')).strip()
                if lvl_val == '0':
                    lvl = 'Cantrips'
                elif lvl_val.isdigit():
                    lvl = f'Level {lvl_val}'
                else:
                    lvl = 'Cantrips'
                    
                name = row.get('Nome', '').strip()
                classes_str = row.get('Classi', '')
                classes = []
                if classes_str:
                    for c in classes_str.split(','):
                        c_it = c.strip().lower()
                        if c_it in class_mapping:
                            classes.append(class_mapping[c_it])
                            
                desc = row.get('Descrizione', '')
                if lvl not in rules['spells']:
                    rules['spells'][lvl] = {}
                rules['spells'][lvl][name] = {
                    'classes': classes,
                    'description': desc
                }
    except Exception as e:
        print("Errore caricamento CSV Incantesimi:", e)
        
    try:
        if 'feats' not in rules:
            rules['feats'] = {}
            
        feat_mapping = {
            "Magic Initiate (Cleric)": "INIZIATO ALLA MAGIA",
            "Crafter": "LAVORO MANUALE",
            "Skilled": "ABILE",
            "Alert": "ALLERTA",
            "Tough": "ROBUSTO",
            "Savage Attacker": "AGGRESSORE SELVAGGIO",
            "Musician": "MUSICISTA",
            "Magic Initiate (Wizard)": "INIZIATO ALLA MAGIA",
            "Tavern Brawler": "LOTTATORE DA TAVERNA",
            "Healer": "GUARITORE",
            "Magic Initiate (Druid)": "INIZIATO ALLA MAGIA",
            "Lucky": "FORTUNATO"
        }
        
        csv_feats = {}
        with open('Talenti_Tutti.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('Nome', '').strip()
                csv_feats[name.upper()] = {
                    'category': row.get('Categoria', '').strip(),
                    'prereq': row.get('Prerequisito', '').strip(),
                    'description': row.get('Descrizione', '').strip()
                }
                
        for f_key, f_data in rules['feats'].items():
            csv_key = feat_mapping.get(f_key, f_key.upper())
            if csv_key in csv_feats:
                f_data['description'] = csv_feats[csv_key]['description']
                f_data['category'] = csv_feats[csv_key]['category']
                
        for c_name, c_data in csv_feats.items():
            title_name = c_name.title()
            if not any(feat_mapping.get(k) == c_name for k in feat_mapping.keys()):
                if title_name not in rules['feats']:
                    rules['feats'][title_name] = {
                        'description': c_data['description'],
                        'category': c_data['category']
                    }
    except Exception as e:
        print("Errore caricamento CSV Talenti:", e)
        
    return rules

def init_session_state():
    defaults = {
        'char_name': '',
        'char_level': 1,
        'char_class': 'Seleziona...',
        'char_subclass': 'Seleziona...',
        'char_species': 'Seleziona...',
        'char_background': 'Seleziona...',
        'char_gen_method': "Point Buy (max 15)",
        'char_boost_type': "Un +2 e un +1",
        'char_p2': '-',
        'char_p1': '-',
        'char_skills': [],
        'char_feats': [],
        'char_spells': [],
        'char_cantrips': [],
        'char_pact': 'Seleziona...',
        'roster': []
    }
    for ab in ["Forza", "Destrezza", "Costituzione", "Intelligenza", "Saggezza", "Carisma"]:
        defaults[f"char_ab_{ab}"] = 8

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_current_char(rules):
    char = {
        'name': st.session_state.char_name,
        'level': st.session_state.char_level,
        'class': st.session_state.char_class,
        'subclass': st.session_state.char_subclass,
        'species': st.session_state.char_species,
        'background': st.session_state.char_background,
        'abilities': {ab: st.session_state[f"char_ab_{ab}"] for ab in ["Forza", "Destrezza", "Costituzione", "Intelligenza", "Saggezza", "Carisma"]},
        'background_boosts': {},
        'skills': st.session_state.char_skills.copy(),
        'spells': st.session_state.char_spells.copy(),
        'cantrips': st.session_state.char_cantrips.copy(),
        'feats': st.session_state.char_feats.copy(),
        'pact': st.session_state.char_pact
    }
    
    bg_name = char['background']
    if bg_name != "Seleziona...":
        bg = rules['backgrounds'].get(bg_name, {})
        char['skills'].extend(bg.get('skills', []))
        
        if st.session_state.char_boost_type == "Un +2 e un +1":
            p2 = st.session_state.char_p2
            p1 = st.session_state.char_p1
            if p2 != "-": char['background_boosts'][p2] = 2
            if p1 != "-": char['background_boosts'][p1] = 1
        else:
            for ab in bg.get('ability_boosts', []):
                char['background_boosts'][ab] = 1
                
    all_feats = []
    if bg_name != "Seleziona...":
        origin_feat = rules['backgrounds'].get(bg_name, {}).get('origin_feat', '')
        if origin_feat: all_feats.append(origin_feat)
    all_feats.extend(char['feats'])
    
    sp_name = char['species']
    if sp_name != "Seleziona...":
        sp_traits = rules['species'][sp_name].get('traits', [])
        for t in sp_traits:
            t_data = rules.get('trait_options', {}).get(t, {})
            # automatically granted skills/cantrips
            char['skills'].extend(t_data.get('skills_granted', []))
            char['cantrips'].extend(t_data.get('cantrips_granted', []))
            
            # user choices
            if t_data.get('origin_feat', 0) > 0:
                t_feat = st.session_state.get(f"trait_feat_{t}")
                if t_feat and t_feat != "Seleziona...":
                    all_feats.append(t_feat)
                    char['feats'].append(t_feat)
            
            if t_data.get('skill_choices', 0) > 0:
                t_skills = st.session_state.get(f"trait_skills_{t}", [])
                char['skills'].extend(t_skills)

    for f in all_feats:
        asi_sel = st.session_state.get(f"feat_asi_{f}")
        if asi_sel and asi_sel != "Seleziona...":
            char['background_boosts'][asi_sel] = char['background_boosts'].get(asi_sel, 0) + 1
            
        skill_sel = st.session_state.get(f"feat_skills_{f}", [])
        char['skills'].extend(skill_sel)
        
        c_sel = st.session_state.get(f"feat_cantrips_{f}", [])
        l1_sel = st.session_state.get(f"feat_lvl1_{f}", [])
        char['cantrips'].extend(c_sel)
        char['spells'].extend(l1_sel)
        
    return char

def main():
    add_custom_css()
    st.title("🐉 Costruttore di Personaggi - D&D 2024")
    
    rules = load_rules()
    init_session_state()

    tab_base, tab_stats, tab_adv, tab_sheet, tab_roster = st.tabs([
        "1. Identità", "2. Caratteristiche & Talenti", "3. Magia & Livelli", "4. Scheda Personaggio", "5. I Miei PG (Max 6)"
    ])
    
    with tab_base:
        if st.button("🔄 Resetta Personaggio Corrente"):
            for key in list(st.session_state.keys()):
                if key.startswith("char_") or key.startswith("feat_") or key.startswith("trait_"):
                    del st.session_state[key]
            init_session_state()
            st.rerun()
            
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Nome", key="char_name")
            st.number_input("Livello", min_value=1, max_value=20, key="char_level")
            
            opts_class = ["Seleziona..."] + list(rules['classes'].keys())
            if st.session_state.char_class not in opts_class:
                st.session_state.char_class = "Seleziona..."
            st.selectbox("Classe", options=opts_class, key="char_class")
            
            cls_name = st.session_state.char_class
            cdata = rules['classes'].get(cls_name, {}) if cls_name != "Seleziona..." else {}
            
            if st.session_state.char_level >= 3 and "subclasses" in cdata:
                opts_sub = ["Seleziona..."] + list(cdata['subclasses'].keys())
                if st.session_state.char_subclass not in opts_sub:
                    st.session_state.char_subclass = "Seleziona..."
                st.selectbox("Sottoclasse (Livello 3+)", options=opts_sub, key="char_subclass")
            else:
                st.session_state.char_subclass = "Seleziona..."
                
            if cls_name == "Warlock" and st.session_state.char_level >= 1 and "pact_boons" in cdata:
                opts_pact = ["Seleziona..."] + list(cdata['pact_boons'].keys())
                if st.session_state.char_pact not in opts_pact:
                    st.session_state.char_pact = "Seleziona..."
                st.selectbox("Patto del Warlock", options=opts_pact, key="char_pact")
                
        with col2:
            opts_species = ["Seleziona..."] + list(rules['species'].keys())
            if st.session_state.char_species not in opts_species:
                st.session_state.char_species = "Seleziona..."
            st.selectbox("Specie", options=opts_species, key="char_species")
            sp_name = st.session_state.char_species
            if sp_name != "Seleziona...":
                st.info(rules['species'][sp_name].get('description', ''))
            
            opts_bg = ["Seleziona..."] + list(rules['backgrounds'].keys())
            if st.session_state.char_background not in opts_bg:
                st.session_state.char_background = "Seleziona..."
            st.selectbox("Background", options=opts_bg, key="char_background")
            bg_name = st.session_state.char_background
            if bg_name != "Seleziona...":
                bg = rules['backgrounds'][bg_name]
                st.info(bg.get('description', ''))
                st.write(f"**Talento di Origine:** {bg.get('origin_feat', '')}")
                st.write(f"**Competenze (Skills) da BG:** {', '.join(bg.get('skills', []))}")
                
    with tab_stats:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Generazione Punteggi Base")
            gen_opts = ["Point Buy (max 15)", "Standard Array", "Manuale"]
            if st.session_state.char_gen_method not in gen_opts:
                st.session_state.char_gen_method = gen_opts[0]
            gen_method = st.radio("Metodo", gen_opts, horizontal=True, key="char_gen_method")
            
            ab_cols = st.columns(2)
            options = list(range(8, 16)) if gen_method == "Point Buy (max 15)" else ([8, 10, 12, 13, 14, 15] if gen_method == "Standard Array" else list(range(3, 19)))
            
            for i, ab in enumerate(rules['abilities']):
                with ab_cols[i % 2]:
                    if gen_method == "Manuale":
                        st.number_input(f"{ab} (Base)", min_value=3, max_value=18, key=f"char_ab_{ab}")
                    else:
                        if st.session_state[f"char_ab_{ab}"] not in options:
                            st.session_state[f"char_ab_{ab}"] = options[0]
                        st.selectbox(f"{ab} (Base)", options=options, key=f"char_ab_{ab}")

            if gen_method == "Point Buy (max 15)":
                costs = {8:0, 9:1, 10:2, 11:3, 12:4, 13:5, 14:7, 15:9}
                spent = sum(costs.get(st.session_state[f"char_ab_{ab}"], 0) for ab in rules['abilities'])
                if spent > 27: st.error(f"Punti spesi: {spent}/27. Hai superato il limite!")
                else: st.success(f"Punti spesi: {spent}/27.")
                
        with col2:
            st.subheader("Bonus dal Background")
            bg_name = st.session_state.char_background
            if bg_name != "Seleziona...":
                bg = rules['backgrounds'][bg_name]
                boost_opts = bg.get('ability_boosts', [])
                
                st.markdown(f"Il Background conferisce bonus a: **{', '.join(boost_opts)}**.")
                b_opts = ["Un +2 e un +1", "Tre +1"]
                if st.session_state.char_boost_type not in b_opts:
                    st.session_state.char_boost_type = b_opts[0]
                boost_type = st.radio("Distribuzione", b_opts, horizontal=True, key="char_boost_type")
                
                if boost_type == "Un +2 e un +1":
                    p2_opts = ["-"] + boost_opts
                    if st.session_state.char_p2 not in p2_opts:
                        st.session_state.char_p2 = p2_opts[0]
                    p2 = st.selectbox("+2 a:", p2_opts, key="char_p2")
                    
                    avail_1 = [s for s in boost_opts if s != p2]
                    p1_opts = ["-"] + avail_1
                    if st.session_state.char_p1 not in p1_opts:
                        st.session_state.char_p1 = p1_opts[0]
                    st.selectbox("+1 a:", p1_opts, key="char_p1")
            else:
                st.warning("Seleziona un Background per assegnare i bonus alle caratteristiche.")

            st.divider()
            st.subheader("Competenze di Classe")
            cls_name = st.session_state.char_class
            if cls_name != "Seleziona..." and bg_name != "Seleziona...":
                bg_skills = rules['backgrounds'][bg_name].get('skills', [])
                cdata = rules['classes'][cls_name]
                n_choices = cdata.get('skill_choices', 0)
                avail = [s for s in cdata.get('skill_options', []) if s not in bg_skills]
                
                valid_selections = [s for s in st.session_state.char_skills if s in avail]
                if len(valid_selections) != len(st.session_state.char_skills):
                    st.session_state.char_skills = valid_selections
                st.multiselect(f"Scegli {n_choices} abilità di classe", options=avail, max_selections=n_choices, key="char_skills")
                
        st.divider()
        st.subheader("🎯 Talenti (Feats) e le loro opzioni")
        st.write("Qui puoi scegliere i talenti aggiuntivi derivanti dall'avanzamento di classe, e compilare le opzioni specifiche fornite dai tuoi talenti (es. Abilità extra fornite da 'Abile').")
        
        cls_name = st.session_state.char_class
        extra_feats_count = 0
        if cls_name != "Seleziona...":
            cdata = rules['classes'][cls_name]
            for l in range(1, st.session_state.char_level + 1):
                feat_str = cdata.get("features", {}).get(str(l), "")
                if "Punteggi di Caratteristica o Talento" in feat_str:
                    extra_feats_count += 1
                    
        avail_feats = list(rules.get('feats', {}).keys())
        if extra_feats_count > 0:
            valid_feats = [f for f in st.session_state.char_feats if f in avail_feats]
            if len(valid_feats) != len(st.session_state.char_feats):
                st.session_state.char_feats = valid_feats
            st.multiselect(f"Scegli {extra_feats_count} talenti extra (Avanzamenti di Classe)", options=avail_feats, max_selections=extra_feats_count, key="char_feats")
            
        sp_name = st.session_state.char_species
        species_feats = []
        if sp_name != "Seleziona...":
            sp_traits = rules.get('species', {}).get(sp_name, {}).get('traits', [])
            for t in sp_traits:
                t_data = rules.get('trait_options', {}).get(t, {})
                
                if t_data.get('origin_feat', 0) > 0:
                    avail_origin_feats = [f for f, d in rules.get('feats', {}).items() if 'origin' in d.get('category', '').lower() or 'origine' in d.get('category', '').lower()]
                    if not avail_origin_feats:
                        avail_origin_feats = avail_feats
                        
                    opts = ["Seleziona..."] + avail_origin_feats
                    key_trait_feat = f"trait_feat_{t}"
                    if st.session_state.get(key_trait_feat) not in opts:
                        st.session_state[key_trait_feat] = opts[0]
                        
                    sel_feat = st.selectbox(f"Scegli un Talento di Origine extra ({t})", options=opts, key=key_trait_feat)
                    if sel_feat and sel_feat != "Seleziona...":
                        species_feats.append(sel_feat)
                        
                skill_choices_count = t_data.get('skill_choices', 0)
                if skill_choices_count > 0:
                    avail_skills = list(rules.get('skills', {}).keys())
                    key_trait_skills = f"trait_skills_{t}"
                    prev_skills = st.session_state.get(key_trait_skills, [])
                    valid_skills = [x for x in prev_skills if x in avail_skills]
                    if len(valid_skills) != len(prev_skills):
                        st.session_state[key_trait_skills] = valid_skills
                        
                    st.multiselect(f"Scegli {skill_choices_count} Abilità extra ({t})", options=avail_skills, max_selections=skill_choices_count, key=key_trait_skills)
            
        bg_name = st.session_state.char_background
        origin_feat = rules['backgrounds'].get(bg_name, {}).get('origin_feat', '') if bg_name != "Seleziona..." else ""
        
        all_char_feats = []
        if origin_feat: all_char_feats.append(origin_feat)
        all_char_feats.extend(st.session_state.char_feats)
        all_char_feats.extend(species_feats)

        if all_char_feats:
            for f in all_char_feats:
                f_data = rules.get('feats', {}).get(f, {})
                asi_choices = f_data.get('asi_choices', [])
                skill_choices = f_data.get('skill_choices', 0)
                spell_choices = f_data.get('spell_choices', {})
                tool_choices = f_data.get('tool_choices', 0)
                
                if asi_choices or skill_choices > 0 or spell_choices or tool_choices > 0:
                    with st.expander(f"⚙️ Opzioni per il talento: {f}", expanded=True):
                        st.write(f"*{f_data.get('description', '')}*")
                        if asi_choices:
                            opts = ["Seleziona..."] + asi_choices
                            key_asi = f"feat_asi_{f}"
                            if st.session_state.get(key_asi) not in opts:
                                st.session_state[key_asi] = opts[0]
                            st.selectbox(f"Aumento (+1):", options=opts, key=key_asi)
                            
                        if skill_choices > 0:
                            all_skills = list(rules.get('skills', {}).keys())
                            key_sk = f"feat_skills_{f}"
                            prev = st.session_state.get(key_sk, [])
                            valid_prev = [x for x in prev if x in all_skills]
                            if len(valid_prev) != len(prev):
                                st.session_state[key_sk] = valid_prev
                            st.multiselect(f"Scegli {skill_choices} Abilità:", options=all_skills, max_selections=skill_choices, key=key_sk)
                            
                        if tool_choices > 0:
                            tools_list = ["Strumenti da Artigiano", "Strumenti Musicali", "Borsa del Guaritore", "Arnesi da Scasso", "Kit da Trucco", "Kit da Falsario"]
                            key_tool = f"feat_tools_{f}"
                            prev = st.session_state.get(key_tool, [])
                            valid_prev = [x for x in prev if x in tools_list]
                            if len(valid_prev) != len(prev):
                                st.session_state[key_tool] = valid_prev
                            st.multiselect(f"Scegli {tool_choices} Strumenti:", options=tools_list, max_selections=tool_choices, key=key_tool)
                            
                        if spell_choices:
                            sc_class = spell_choices.get('class', 'Wizard')
                            sc_cantrips = spell_choices.get('cantrips', 0)
                            sc_lvl1 = spell_choices.get('level_1', 0)
                            if sc_cantrips > 0:
                                avail_c = [s for s, d in rules.get('spells', {}).get('Cantrips', {}).items() if sc_class in d.get('classes', [])]
                                key_c = f"feat_cantrips_{f}"
                                prev = st.session_state.get(key_c, [])
                                valid_prev = [x for x in prev if x in avail_c]
                                if len(valid_prev) != len(prev):
                                    st.session_state[key_c] = valid_prev
                                st.multiselect(f"Scegli {sc_cantrips} Trucchetti ({sc_class}):", options=avail_c, max_selections=sc_cantrips, key=key_c)
                            if sc_lvl1 > 0:
                                avail_l1 = [s for s, d in rules.get('spells', {}).get('Level 1', {}).items() if sc_class in d.get('classes', [])]
                                key_l1 = f"feat_lvl1_{f}"
                                prev = st.session_state.get(key_l1, [])
                                valid_prev = [x for x in prev if x in avail_l1]
                                if len(valid_prev) != len(prev):
                                    st.session_state[key_l1] = valid_prev
                                st.multiselect(f"Scegli {sc_lvl1} Incantesimo Lv1 ({sc_class}):", options=avail_l1, max_selections=sc_lvl1, key=key_l1)

        st.divider()
        st.subheader("💡 Riepilogo Dinamico Caratteristiche e Abilità")
        st.info("I punteggi e le competenze mostrati qui si aggiornano in tempo reale in base a Metodo di Generazione, Background, Sottoclasse e Talenti scelti qui sopra!")
        preview_cols = st.columns(6)
        temp_char = get_current_char(rules)
        prof_bonus = 2 + ((temp_char['level'] - 1) // 4)
        for i, ab in enumerate(rules['abilities']):
            val = temp_char['abilities'][ab] + temp_char['background_boosts'].get(ab, 0)
            mod = (val - 10) // 2
            with preview_cols[i]:
                st.markdown(f"<div class='stat-box'><div class='stat-label'>{ab}</div><div class='stat-value'>{val}</div><div style='font-size: 14px;'>Mod: {mod:+}</div></div>", unsafe_allow_html=True)
                ab_skills = [s for s, base_ab in rules.get('skills', {}).items() if base_ab == ab]
                for s in ab_skills:
                    if s in temp_char['skills']:
                        st.markdown(f"<div style='font-size: 12px;'>✅ **{s}**: {mod + prof_bonus:+}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='font-size: 12px; color: gray;'>⬜ {s}: {mod:+}</div>", unsafe_allow_html=True)

    with tab_adv:
        st.header("Avanzamento di Livello")
        cls_name = st.session_state.char_class
        if cls_name != "Seleziona...":
            cdata = rules['classes'][cls_name]
            
            st.subheader("Privilegi di Classe Sbloccati")
            feats_list = []
            for l in range(1, st.session_state.char_level + 1):
                feat = cdata.get("features", {}).get(str(l), "")
                if feat:
                    feats_list.append((l, feat))
                
                subclass = st.session_state.char_subclass
                if subclass != "Seleziona...":
                    sub_feat = cdata.get("subclasses", {}).get(subclass, {}).get("level_features", {}).get(str(l), "")
                    if sub_feat:
                        feats_list.append((l, f"[Sottoclasse] {sub_feat}"))
            
            st.table([{"Livello": l, "Privilegio": f} for l, f in feats_list])

            spellcasting = cdata.get('spellcasting', 'none')
            if spellcasting != 'none':
                st.divider()
                st.subheader("Incantesimi (Dal manuale 2024)")
                st.markdown(f"Come incantatore ({cls_name}), scegli i tuoi incantesimi. Sono tutti ordinati e presi dal CSV ufficiale!")
                
                avail_cantrips = sorted([s for s, d in rules.get('spells', {}).get('Cantrips', {}).items() if cls_name in d.get('classes', [])])
                
                avail_spells = []
                for lvl_name in ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 9']:
                    for s, d in rules.get('spells', {}).get(lvl_name, {}).items():
                        if cls_name in d.get('classes', []):
                            avail_spells.append(f"{lvl_name}: {s}")
                avail_spells = sorted(avail_spells)
                
                valid_c = [s for s in st.session_state.char_cantrips if s in avail_cantrips]
                if len(valid_c) != len(st.session_state.char_cantrips):
                    st.session_state.char_cantrips = valid_c
                st.multiselect(f"Trucchetti conosciuti ({len(avail_cantrips)} disponibili per {cls_name})", options=avail_cantrips, key="char_cantrips")
                
                valid_s = [s for s in st.session_state.char_spells if s in avail_spells]
                if len(valid_s) != len(st.session_state.char_spells):
                    st.session_state.char_spells = valid_s
                st.multiselect(f"Incantesimi conosciuti Livelli 1-9 ({len(avail_spells)} disponibili per {cls_name})", options=avail_spells, key="char_spells")
        else:
            st.warning("Seleziona una classe nella scheda Identità.")

    with tab_sheet:
        char = get_current_char(rules)
        bg_name = char['background']
        
        if not char['name'] or char['class'] == "Seleziona..." or char['species'] == "Seleziona..." or bg_name == "Seleziona...":
            st.warning("Completa la scheda Identità per generare la Scheda Personaggio.")
        else:
            level = char['level']
            prof_bonus = 2 + ((level - 1) // 4)
            final_abilities = {ab: char['abilities'][ab] + char['background_boosts'].get(ab, 0) for ab in rules['abilities']}
            mods = {ab: (final_abilities[ab] - 10) // 2 for ab in rules['abilities']}
            
            hit_die = rules['classes'][char['class']]['hit_die']
            max_hp = math.floor((hit_die + mods["Costituzione"]) + ((hit_die / 2 + 1) + mods["Costituzione"]) * (level - 1))
            
            origin_feat = rules['backgrounds'][bg_name].get('origin_feat', '')
            if origin_feat == "Tough" or "Tough" in char['feats']:
                max_hp += 2 * level
                
            ac = 10 + mods["Destrezza"]
            if char['class'] == "Barbarian": ac = 10 + mods["Destrezza"] + mods["Costituzione"]
            elif char['class'] == "Monk": ac = 10 + mods["Destrezza"] + mods["Saggezza"]
            elif char.get('subclass') == "Stregoneria Draconica": ac = 13 + mods["Destrezza"]
            
            initiative = mods["Destrezza"]
            if origin_feat == "Alert" or "Alert" in char['feats']: initiative += prof_bonus
            
            speed = rules['species'][char['species']].get('speed', 30)
            passive_perception = 10 + mods["Saggezza"] + (prof_bonus if "Percezione" in char['skills'] else 0)
            
            st.markdown(f'''
            <div style="background-color: #fffaf0; border: 2px solid #8b0000; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h1 style="text-align: center; color: #8b0000; margin: 0;">{char['name']}</h1>
                <p style="text-align: center; font-size: 1.2em; font-style: italic; color: #3e2723; margin-top: 5px;">
                    {rules['species'][char['species']]['name_it']} {rules['classes'][char['class']]['name_it']} {char['subclass'] if char['subclass']!="Seleziona..." else ""} (Livello {level}) <br>
                    Background: {rules['backgrounds'][bg_name]['name_it']}
                </p>
            </div>
            ''', unsafe_allow_html=True)
            
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            with c1: st.markdown(f"<div class='stat-box'><div class='stat-label'>CA</div><div class='stat-value'>{ac}</div></div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='stat-box'><div class='stat-label'>Iniziativa</div><div class='stat-value'>{'+'+str(initiative) if initiative>=0 else initiative}</div></div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='stat-box'><div class='stat-label'>Velocità</div><div class='stat-value'>{speed} ft</div></div>", unsafe_allow_html=True)
            with c4: st.markdown(f"<div class='stat-box'><div class='stat-label'>HP Max</div><div class='stat-value'>{max_hp}</div></div>", unsafe_allow_html=True)
            with c5: st.markdown(f"<div class='stat-box'><div class='stat-label'>Prof Bonus</div><div class='stat-value'>+{prof_bonus}</div></div>", unsafe_allow_html=True)
            with c6: st.markdown(f"<div class='stat-box'><div class='stat-label'>Percezione Passiva</div><div class='stat-value'>{passive_perception}</div></div>", unsafe_allow_html=True)
            
            col_l, col_r = st.columns([1, 2])
            with col_l:
                st.subheader("Caratteristiche e Abilità")
                for ab in rules['abilities']:
                    val = final_abilities[ab]
                    m = mods[ab]
                    st.markdown(f"### **{ab}** &nbsp; `{val}` &nbsp; ({'+'+str(m) if m>=0 else m})")
                    ab_skills = [s for s, base_ab in rules.get('skills', {}).items() if base_ab == ab]
                    for s in ab_skills:
                        if s in char['skills']:
                            st.markdown(f"- ✅ **{s}** *(+{m + prof_bonus})*")
                        else:
                            st.markdown(f"- ⬜ {s} *({'+'+str(m) if m>=0 else m})*")
                
            with col_r:
                st.subheader("Tratti & Privilegi")
                st.markdown(f"**Specie ({rules['species'][char['species']]['name_it']}):**")
                for t in rules['species'][char['species']].get('traits', []):
                    t_desc = rules.get('trait_descriptions', {}).get(t, '')
                    if t_desc:
                        st.write(f"- **{t}**: {t_desc}")
                    else:
                        st.write(f"- {t}")
                
                st.markdown(f"**Talenti:**")
                st.write(f"- {origin_feat} (Origine)")
                for f in char.get('feats', []): st.write(f"- {f}")
                
                spellcasting = rules['classes'][char['class']].get('spellcasting', 'none')
                if spellcasting != 'none':
                    st.subheader("Incantesimi Conosciuti")
                    sa = ""
                    if char['class'] in ["Bard", "Paladin", "Sorcerer", "Warlock"]: sa = "Carisma"
                    elif char['class'] in ["Cleric", "Druid", "Ranger"]: sa = "Saggezza"
                    elif char['class'] == "Wizard": sa = "Intelligenza"
                    
                    if sa:
                        dc = 8 + prof_bonus + mods[sa]
                        atk = prof_bonus + mods[sa]
                        st.markdown(f"**Caratteristica:** {sa} | **CD Salvezza:** {dc} | **Bonus Attacco:** +{atk}")
                        
                    for c in char.get('cantrips', []):
                        desc = rules.get('spells', {}).get('Cantrips', {}).get(c, {}).get('description', '')[:100] + '...'
                        st.write(f"- **{c}** (Trucchetto): {desc}")
                    for s in char.get('spells', []):
                        desc = ""
                        spell_name = s.split(": ")[1] if ": " in s else s
                        for s_lvl, d in rules.get('spells', {}).items():
                            if spell_name in d: desc = d[spell_name].get('description', '')[:100] + '...'
                        st.write(f"- **{s}**: {desc}")

            st.info("💡 Scarica il PDF del tuo personaggio usando i tasti sottostanti (la scheda grafica D&D ufficiale verrà compilata automaticamente!).")
            
            try:
                pdf_bytes = generate_pdf(char, rules)
                st.download_button(
                    label="📥 Scarica PDF Grafico Scheda Personaggio (Ufficiale)",
                    data=pdf_bytes,
                    file_name=f"{char['name'].replace(' ', '_')}_Scheda.pdf",
                    mime="application/pdf",
                    key="dl_scheda"
                )
            except Exception as e:
                st.error(f"Errore nella generazione del PDF: {e}")
                
            try:
                prog_bytes = generate_progression_pdf(char, rules)
                st.download_button(
                    label="📈 Scarica PDF Tabella Avanzamento Completa",
                    data=prog_bytes,
                    file_name=f"{char['name'].replace(' ', '_')}_Avanzamento.pdf",
                    mime="application/pdf",
                    key="dl_prog"
                )
            except Exception as e:
                st.error(f"Errore nella generazione del PDF Avanzamento: {e}")
                
            try:
                spells_bytes = generate_spells_pdf(char, rules)
                st.download_button(
                    label="📜 Scarica PDF Lista Incantesimi (Scelti e Disponibili)",
                    data=spells_bytes,
                    file_name=f"{char['name'].replace(' ', '_')}_Incantesimi.pdf",
                    mime="application/pdf",
                    key="dl_spells"
                )
            except Exception as e:
                st.error(f"Errore nella generazione del PDF Incantesimi: {e}")

    with tab_roster:
        st.header("I Miei Personaggi Salvati (Max 6)")
        if st.button("💾 Salva Personaggio Corrente", key="ui_btn_save"):
            if not st.session_state.char_name:
                st.error("Il personaggio deve avere un nome per essere salvato.")
            else:
                char_data = get_current_char(rules)
                char_data['_raw_state'] = {
                    'char_name': st.session_state.char_name,
                    'char_level': st.session_state.char_level,
                    'char_class': st.session_state.char_class,
                    'char_subclass': st.session_state.char_subclass,
                    'char_species': st.session_state.char_species,
                    'char_background': st.session_state.char_background,
                    'char_gen_method': st.session_state.char_gen_method,
                    'char_boost_type': st.session_state.char_boost_type,
                    'char_p2': st.session_state.char_p2,
                    'char_p1': st.session_state.char_p1,
                    'char_skills': st.session_state.char_skills.copy(),
                    'char_feats': st.session_state.char_feats.copy(),
                    'char_cantrips': st.session_state.char_cantrips.copy(),
                    'char_spells': st.session_state.char_spells.copy(),
                    'char_pact': st.session_state.char_pact
                }
                for ab in rules['abilities']:
                    char_data['_raw_state'][f'char_ab_{ab}'] = st.session_state[f'char_ab_{ab}']
                for k, v in st.session_state.items():
                    if k.startswith("feat_") or k.startswith("trait_"):
                        char_data['_raw_state'][k] = copy.deepcopy(v)
                    
                existing = [i for i, c in enumerate(st.session_state.roster) if c['name'] == char_data['name']]
                if existing:
                    st.session_state.roster[existing[0]] = copy.deepcopy(char_data)
                    st.success(f"Personaggio {char_data['name']} aggiornato!")
                elif len(st.session_state.roster) >= 6:
                    st.error("Hai raggiunto il limite massimo di 6 personaggi salvati.")
                else:
                    st.session_state.roster.append(copy.deepcopy(char_data))
                    st.success(f"Personaggio {char_data['name']} salvato!")
                    
        st.divider()
        if not st.session_state.roster:
            st.info("Nessun personaggio salvato. Creane uno e salvalo!")
        else:
            for idx, c in enumerate(st.session_state.roster):
                class_name_it = rules['classes'].get(c['class'], {}).get('name_it', c['class'])
                st.markdown(f"### {c['name']} - {class_name_it} (Livello {c['level']})")
                col_btn1, col_btn2 = st.columns([1, 10])
                with col_btn1:
                    if st.button("Carica", key=f"load_{idx}"):
                        for k, v in c['_raw_state'].items():
                            st.session_state[k] = v
                        st.rerun()
                with col_btn2:
                    if st.button("Elimina", key=f"del_{idx}"):
                        st.session_state.roster.pop(idx)
                        st.rerun()
                st.markdown("---")

if __name__ == "__main__":
    main()
