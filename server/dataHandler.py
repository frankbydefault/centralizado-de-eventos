from instagramScraper import fetch_posts
from chatGPT import ask_chatgpt
import json

# Categorizando y transformando data usando chatgpt
posts = fetch_posts()
events = ask_chatgpt(json.dumps(posts))
print(events)

data = json.loads(events)

# Agregando data a un archivo JSON
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)