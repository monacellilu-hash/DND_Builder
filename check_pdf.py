import fitz

doc = fitz.open('../Dati_Input/DnD_2024_Character-Sheet.pdf')
page = doc[0]
widgets = list(page.widgets())
print(f"Widgets found on page 1: {len(widgets)}")
if widgets:
    for w in widgets[:10]:
        print(f"Field: {w.field_name}, Rect: {w.rect}")
