import json
import re

def parse_feats():
    with open('test_feats.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    lines = text.split('\n')
    feats = {}
    current_feat_name = None
    current_feat_desc = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # A new feat usually starts with its name in ALL CAPS
        # followed by "Talento Origine", "Talento Generale", "Talento Stile di combattimento", "Talento Dono epico"
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            if next_line.startswith("Talento Origine") or next_line.startswith("Talento Generale") or next_line.startswith("Talento Stile") or next_line.startswith("Talento Dono"):
                if current_feat_name:
                    feats[current_feat_name] = " ".join(current_feat_desc).strip()
                
                current_feat_name = line.title()
                current_feat_desc = [next_line]
                continue
                
        if current_feat_name:
            if line == "Stile di combattimento." and "Tiratore" in current_feat_name:
                continue
            # Skip page headers/footers
            if "CAPITOLO 5" in line or "TALENTI" in line or line.isdigit():
                continue
            current_feat_desc.append(line)
            
    if current_feat_name:
        feats[current_feat_name] = " ".join(current_feat_desc).strip()
        
    with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if 'feats' not in data:
        data['feats'] = {}
        
    for name, desc in feats.items():
        data['feats'][name] = {
            "description": desc
        }
        
    with open('data/rules_2024.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Added {len(feats)} feats to rules_2024.json")

if __name__ == "__main__":
    parse_feats()
