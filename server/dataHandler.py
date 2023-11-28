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
            {"role": "system", "content":
                '''
                Tu tarea principal es analizar fragmentos de texto para identificar si describen un evento.
                1. Si el texto no describe un evento o carece de fechas, responde con un objeto JSON vacío.
                2. Si el texto describe un evento, procede a extraer los detalles relevantes y formúlalos en un objeto JSON (sin espaciadores)siguiendo esta estructura específica:

                    titulo: El nombre o título del evento.
                    descripcion: Una breve descripción del evento, limitada a un máximo de 3 líneas de texto. Evita el uso de hashtags (#) en esta descripción.
                    fechas: Un arreglo de fechas relacionadas con el evento. Ejemplo: ["2023-11-27", "2023-11-28"]
                    horaInicio: Un arreglo de horas de inicio correspondientes a cada fecha del evento. Ejemplo: ["08:30", "09:00"]
                    horaTermino: Un arreglo de horas de término para cada fecha del evento. Ejemplo: ["18:00", "17:00"]
                    ubicacion: La ubicación específica del evento.

                En caso de que la información sobre horas o ubicación no esté disponible en el texto, deja esos campos como arreglos vacíos.
                '''  
             },
            
            {"role": "user", "content": texto}
        ]
    )
    return response.choices[0].message.content


# Función para obtener posts de Instagram y hacer consultas
def process_posts():
    today = datetime.date.today()

    for account in accounts:
        profile = instaloader.Profile.from_username(L.context, account)
        results = []

        for post in profile.get_posts():
            post_date = post.date.date()

            if post_date == today:
                description = post.caption.encode(encoding = 'UTF-8', errors = 'strict').decode(encoding='UTF-8',errors='strict')
                if description:
                    gpt_response = ask_chatgpt(description)
                    results.append(gpt_response)
            else: 
                break

    return results

upcomingEvents = process_posts()
print("Resultados:", upcomingEvents)
