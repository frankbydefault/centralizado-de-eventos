from openai import OpenAI
client = OpenAI()

# Función para consultar a ChatGPT
def ask_chatgpt(texto):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content":
                '''
                Recibiras una lista objetos JSON, con los atributos "account" y "post", debes analizar el contenido de "post" para identificar si describen un evento.
                1. Si el contenido de "post" no describe un evento o carece de fechas, responde con un objeto JSON vacío.
                2. Si el contenido de "post" describe un evento, procede a extraer los detalles relevantes y formúlalos en un objeto JSON (sin espaciadores)siguiendo esta estructura específica:
                    cuenta: El nombre de la cuenta de instagram. Corresponde al campo "Account" del objeto JSON inicial.
                    titulo: El nombre o título del evento.
                    descripcion: Una breve descripción del evento, limitada a un máximo de 3 líneas de texto. Evita el uso de hashtags (#) en esta descripción.
                    fechas: Un arreglo de fechas relacionadas con el evento. Ejemplo: ["2023-11-27", "2023-11-28"]
                    horaInicio: Un arreglo de horas de inicio correspondientes a cada fecha del evento. Ejemplo: ["08:30", "09:00"]
                    horaTermino: Un arreglo de horas de término para cada fecha del evento. Ejemplo: ["18:00", "17:00"]
                    ubicacion: La ubicación específica del evento.

                En caso de que la información sobre horas o ubicación no esté disponible en el texto, deja esos campos como arreglos vacíos.
                
                Finalmente entrega una lista de los nuevos objetos JSON.
                '''  
             },
            
            {"role": "user", "content": texto}
        ]
    )
    return response.choices[0].message.content