import streamlit as st
import json
import os

# Configurazione della pagina
st.set_page_config(
    page_title="D&D 5e (2024) Character Builder",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caricamento dei dati delle regole
@st.cache_data
def load_rules():
    with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    st.title("🐉 Costruttore di Personaggi - D&D 2024")
    st.markdown("Benvenuto! Usa questa applicazione per creare il tuo personaggio seguendo le **nuove regole del 2024**.")
    
    rules = load_rules()
    
    # Inizializziamo lo stato della sessione per salvare le scelte
    if 'character' not in st.session_state:
        st.session_state.character = {
            'name': '',
            'class': None,
            'species': None,
            'background': None,
            'abilities': {ab: 8 for ab in rules['abilities']},
            'background_boosts': {},
            'skills': []
        }
    
    char = st.session_state.character

    # Struttura base a tab per separare la pre-page e la scheda
    tab_creator, tab_sheet = st.tabs(["Crea Personaggio", "Scheda Personaggio"])
    
    with tab_creator:
        st.header("1. Identità e Origini")
        
        char['name'] = st.text_input("Nome del Personaggio", char['name'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Classe")
            class_options = ["Seleziona..."] + list(rules['classes'].keys())
            selected_class = st.selectbox(
                "Scegli la tua Classe", 
                options=class_options,
                help="La tua classe determina le tue abilità in combattimento, i punti ferita e la magia."
            )
            if selected_class != "Seleziona...":
                char['class'] = selected_class
                class_data = rules['classes'][selected_class]
                st.info(f"**{class_data['name_it']}**: {class_data['description']}")
                if "image" in class_data:
                    st.image(class_data["image"], use_column_width=True)
            else:
                char['class'] = None

        with col2:
            st.subheader("Specie (Razza)")
            species_options = ["Seleziona..."] + list(rules['species'].keys())
            selected_species = st.selectbox(
                "Scegli la tua Specie", 
                options=species_options,
                help="La specie fornisce tratti razziali come la velocità o la visione notturna."
            )
            if selected_species != "Seleziona...":
                char['species'] = selected_species
                st.info(f"**{rules['species'][selected_species]['name_it']}**: {rules['species'][selected_species]['description']}")
            else:
                char['species'] = None

        with col3:
            st.subheader("Background")
            bg_options = ["Seleziona..."] + list(rules['backgrounds'].keys())
            selected_bg = st.selectbox(
                "Scegli il tuo Background", 
                options=bg_options,
                help="Nelle regole 2024, il Background determina i tuoi incrementi alle caratteristiche (+2/+1 o tre +1), un talento di origine e due competenze."
            )
            if selected_bg != "Seleziona...":
                char['background'] = selected_bg
                bg_data = rules['backgrounds'][selected_bg]
                st.info(f"**{bg_data['name_it']}**: {bg_data['description']}")
                if "origin_feat" in bg_data:
                    feat_name = bg_data["origin_feat"]
                    feat_desc = rules.get("feats", {}).get(feat_name, {}).get("description", "")
                    st.markdown(f"**Talento di Origine:** {feat_name} - *{feat_desc}*")
            else:
                char['background'] = None
                
        st.divider()
        
        # Logica Condizionale: Caratteristiche
        st.header("2. Punteggi di Caratteristica")
        gen_method = st.radio("Metodo di Generazione", ["Point Buy (max 15)", "Standard Array", "Manuale / Lancio Dadi"], horizontal=True)
        
        if gen_method == "Point Buy (max 15)":
            st.markdown("Hai 27 punti. Costi: 8=0, 9=1, 10=2, 11=3, 12=4, 13=5, 14=7, 15=9. Min 8, Max 15 prima dei bonus razziali/background.")
            min_v, max_v = 8, 15
        elif gen_method == "Standard Array":
            st.markdown("Assegna liberamente i valori **15, 14, 13, 12, 10, 8** alle caratteristiche qui sotto.")
            min_v, max_v = 8, 15
        else:
            st.markdown("Inserisci liberamente i tuoi punteggi (es. se hai tirato i dadi).")
            min_v, max_v = 3, 18

        cols = st.columns(6)
        for i, ab in enumerate(rules['abilities']):
            with cols[i]:
                curr_val = char['abilities'][ab]
                if curr_val < min_v: curr_val = min_v
                if curr_val > max_v: curr_val = max_v
                char['abilities'][ab] = st.number_input(f"{ab}", min_value=min_v, max_value=max_v, value=curr_val)

        if gen_method == "Point Buy (max 15)":
            costs = {8:0, 9:1, 10:2, 11:3, 12:4, 13:5, 14:7, 15:9}
            spent = sum(costs.get(char['abilities'][ab], 0) for ab in rules['abilities'])
            if spent > 27:
                st.error(f"Punti spesi: {spent}/27. Hai superato il limite!")
            else:
                st.success(f"Punti spesi: {spent}/27.")
                
        # Bonus dal Background (Regole 2024)
        if char['background']:
            st.subheader("Bonus dal Background")
            bg_data = rules['backgrounds'][char['background']]
            st.markdown(f"Il background **{bg_data['name_it']}** ti permette di aumentare alcune di queste caratteristiche: {', '.join(bg_data['ability_boosts'])}")
            
            boost_type = st.radio("Come vuoi distribuire i bonus?", ["Un +2 e un +1", "Tre +1"], horizontal=True)
            
            boost_cols = st.columns(3)
            char['background_boosts'] = {}
            
            if boost_type == "Un +2 e un +1":
                with boost_cols[0]:
                    plus_two = st.selectbox("Statistica per il +2", ["Seleziona..."] + bg_data['ability_boosts'])
                with boost_cols[1]:
                    avail_plus_one = [s for s in bg_data['ability_boosts'] if s != plus_two]
                    plus_one = st.selectbox("Statistica per il +1", ["Seleziona..."] + avail_plus_one)
                
                if plus_two != "Seleziona...": char['background_boosts'][plus_two] = 2
                if plus_one != "Seleziona...": char['background_boosts'][plus_one] = 1
                    
            elif boost_type == "Tre +1":
                st.success(f"Ottieni +1 a: {', '.join(bg_data['ability_boosts'])}")
                for ab in bg_data['ability_boosts']:
                    char['background_boosts'][ab] = 1
        
        st.divider()
        st.header("3. Competenze (Skills)")
        if char['background'] and char['class']:
            bg_skills = rules['backgrounds'][char['background']]['skills']
            st.markdown(f"Dal tuo background ottieni: **{', '.join(bg_skills)}**")
            
            class_data = rules['classes'][char['class']]
            num_choices = class_data['skill_choices']
            avail_class_skills = [s for s in class_data['skill_options'] if s not in bg_skills]
            
            st.markdown(f"Dalla tua classe ({class_data['name_it']}) puoi scegliere **{num_choices}** abilità tra: {', '.join(avail_class_skills)}")
            selected_class_skills = st.multiselect("Scegli le abilità di classe", options=avail_class_skills, max_selections=num_choices)
            
            char['skills'] = bg_skills + selected_class_skills

    with tab_sheet:
        st.header("Scheda Finale")
        if not (char['name'] and char['class'] and char['species'] and char['background']):
            st.warning("Completa la prima pagina per generare la scheda.")
        else:
            st.success(f"Scheda di {char['name']}")
            
            # Calcolo finali
            final_abilities = {ab: char['abilities'][ab] + char['background_boosts'].get(ab, 0) for ab in rules['abilities']}
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Caratteristiche")
                for ab in rules['abilities']:
                    val = final_abilities[ab]
                    mod = (val - 10) // 2
                    mod_str = f"+{mod}" if mod >= 0 else f"{mod}"
                    st.markdown(f"**{ab}:** {val} ({mod_str})")
            
            with col_b:
                st.subheader("Tratti Generali")
                st.write(f"**Classe:** {char['class']}")
                st.write(f"**Specie:** {char['species']}")
                st.write(f"**Background:** {char['background']}")
                
                if char['background']:
                    bg_data = rules['backgrounds'][char['background']]
                    if "origin_feat" in bg_data:
                        st.write(f"**Talento di Origine:** {bg_data['origin_feat']}")

                st.subheader("Abilità (Skills)")
                for skill in char['skills']:
                    st.write(f"- {skill}")

if __name__ == "__main__":
    main()
