import re
from collections import defaultdict

def mejorar_tokenizacion(texto):
    texto = texto.lower().strip()
    
    # Normalización avanzada
    normalizaciones = {
        r'cómo': 'como',
        r'qué': 'que',
        r'dónde': 'donde',
        r'clima': 'tiempo',
        r'cómo está el': 'como esta',
        r'[\W]': ' '
    }
    
    for pat, repl in normalizaciones.items():
        texto = re.sub(pat, repl, texto)
    
    # Eliminar stopwords personalizadas
    stopwords = {'el', 'la', 'los', 'de', 'que', 'en'}
    palabras = [p for p in texto.split() if p not in stopwords]
    
    return palabras

def crear_vocabulario(datos):
    vocabulario = defaultdict(lambda: len(vocabulario))
    vocabulario['<UNK>']  # Para palabras desconocidas
    
    for frase, _ in datos:
        for palabra in mejorar_tokenizacion(frase):
            vocabulario[palabra]
    
    return dict(vocabulario)

def vectorizar_frases(frase, vocabulario):
    vector = [0] * len(vocabulario)
    palabras = mejorar_tokenizacion(frase)
    
    for palabra in palabras:
        idx = vocabulario.get(palabra, vocabulario.get('<UNK>'))
        vector[idx] += 1  # Usamos conteo en lugar de one-hot
    
    return vector
def clase_a_vector(clases, lista_clases):
    vector = [0] * len(lista_clases)
    idx = lista_clases.index(clases)
    vector[idx] = 1
    return vector
