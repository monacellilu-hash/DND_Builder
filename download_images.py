import json
import os
import urllib.request

os.makedirs('images', exist_ok=True)
with open('data/rules_2024.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

req_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.dndbeyond.com/'
}

for cls, info in data['classes'].items():
    if 'image' in info and info['image'].startswith('http'):
        img_url = info['image']
        img_path = f"images/{cls.lower()}.jpeg"
        try:
            req = urllib.request.Request(img_url, headers=req_headers)
            with urllib.request.urlopen(req) as response, open(img_path, 'wb') as out_file:
                out_file.write(response.read())
            info['image'] = img_path
            print(f"Downloaded {img_url} to {img_path}")
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

with open('data/rules_2024.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
