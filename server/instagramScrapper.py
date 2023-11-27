import instaloader
import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

L = instaloader.Instaloader()
client = OpenAI()

L.login(os.getenv('insta_username'), os.getenv('insta_pass'))
accounts = ["hubprovidencia"]

# Función para consultar a ChatGPT
def ask_chatgpt(texto):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu tarea es analizar fragmentos de texto para determinar si describen un evento. Si no describe un evento o no contiene fechas, responde un JSON vacio. Si el texto describe un evento, extrae y proporciona los detalles en formato JSON. Incluye el título del evento, fecha y hora, ubicación y una breve descripción de qué trata el evento."},
            {"role": "user", "content": texto}
        ]
    )
    return response.choices[0].message


# Función para obtener posts de Instagram y hacer consultas
def process_posts():
    today = datetime.date.today()

    for account in accounts:
        profile = instaloader.Profile.from_username(L.context, account)

        for post in profile.get_posts():
            post_date = post.date.date()

            if post_date == today:
                try:
                    description = post.caption
                except UnicodeEncodeError as e:
                    description = post.caption.encode('ascii', 'ignore').decode('ascii')

                if description:
                    gpt_response = ask_chatgpt(description)
                    print("Respuesta de GPT-3:", gpt_response)

process_posts()

