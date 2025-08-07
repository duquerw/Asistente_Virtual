import random

respuestas_por_clase = {
    "saludo": [
        "¡Hola! ¿En qué puedo ayudarte hoy?",
        "¡Qué bueno verte! ¿Cómo estás?"
    ],
    "pregunta": [
        "Eso suena interesante, ¿puedes explicarlo mejor?",
        "Buena pregunta. Déjame pensar un segundo..."
    ],
    "clima": [
        "Parece que hace calor hoy. ¿Quieres que revise el pronóstico?",
        "El clima está cambiando bastante últimamente, ¿no crees?"
    ],
    "despedida": [
        "Nos vemos pronto.",
        "Cuídate mucho, ¡hasta luego!"
    ],
    "afición": [
        "Programar es una excelente manera de pasar el tiempo.",
        "Me gusta que tengas pasatiempos productivos."
    ],
    "respuesta": [
        "Gracias por compartir eso.",
        "Entiendo. ¿Y qué más?"
    ],
    "reflexión": [
        "Totalmente de acuerdo contigo.",
        "Esa es una gran forma de verlo."
    ],
    "pronóstico del tiempo": [
        "Creo que sí lloverá hoy. ¿Llevas paraguas?",
        "Dicen que el clima será soleado mañana."
    ]
}

def obtener_respuesta_por_clase(clase):
    respuestas = respuestas_por_clase.get(clase, [])
    if respuestas:
        return random.choice(respuestas)
    return "No entiendo bien eso."
