# core/contexto.py
import re
from datetime import datetime
import json

class GestorContexto:
    def __init__(self):
        self.contexto = {
            'usuario': {
                'nombre': None,
                'ubicacion': None,
                'intereses': set()
            },
            'conversacion': {
                'tema_actual': None,
                'tema_anterior': None,
                'historial_temas': [],
                'tono': 'neutral'  # puede ser 'formal', 'informal', 'técnico', etc.
            },
            'ultima_actualizacion': None
        }
    
    def actualizar_contexto(self, texto_usuario, respuesta_asistente):
        """Analiza el texto para extraer y actualizar información contextual"""
        self._extraer_datos_personales(texto_usuario)
        self._identificar_tema(texto_usuario, respuesta_asistente)
        self._detectar_tono(texto_usuario)
        self._identificar_intereses(texto_usuario)
        self.contexto['ultima_actualizacion'] = datetime.now().isoformat()
    
    def _extraer_datos_personales(self, texto):
        # Extraer nombre
        nombre_patterns = [
            r"me llamo ([a-záéíóúñü]+)",
            r"mi nombre es ([a-záéíóúñü]+)",
            r"soy ([a-záéíóúñü]+)"
        ]
        for pattern in nombre_patterns:
            match = re.search(pattern, texto.lower())
            if match and len(match.group(1).split()) == 1:  # Solo nombres simples
                self.contexto['usuario']['nombre'] = match.group(1).capitalize()
                break
        
        # Extraer ubicación
        ubicacion_patterns = [
            r"vivo en ([a-záéíóúñü\s]+)",
            r"estoy en ([a-záéíóúñü\s]+)",
            r"soy de ([a-záéíóúñü\s]+)"
        ]
        for pattern in ubicacion_patterns:
            match = re.search(pattern, texto.lower())
            if match:
                self.contexto['usuario']['ubicacion'] = match.group(1).capitalize()
                break
    
    def _identificar_tema(self, texto_usuario, respuesta_asistente):
        # Actualizar temas
        temas_clave = {
            'trabajo': ['trabajo', 'empleo', 'oficina', 'jefe'],
            'ocio': ['ocio', 'diversión', 'hobby', 'pasatiempo'],
            'tecnologia': ['python', 'programa', 'código', 'tecnología'],
            'clima': ['clima', 'tiempo', 'lluvia', 'soleado']
        }
        
        tema_actual = None
        for tema, palabras in temas_clave.items():
            if any(palabra in texto_usuario.lower() for palabra in palabras):
                tema_actual = tema
                break
        
        if tema_actual:
            if self.contexto['conversacion']['tema_actual'] != tema_actual:
                self.contexto['conversacion']['tema_anterior'] = self.contexto['conversacion']['tema_actual']
                self.contexto['conversacion']['tema_actual'] = tema_actual
                self.contexto['conversacion']['historial_temas'].append({
                    'tema': tema_actual,
                    'timestamp': datetime.now().isoformat()
                })
    
    def _detectar_tono(self, texto):
        # Analizar tono del usuario
        palabras_formales = ['por favor', 'gracias', 'le agradezco']
        palabras_informales = ['bro', 'holis', 'jaja', 'xD']
        palabras_tecnicas = ['algoritmo', 'red neuronal', 'pln', 'backend']
        
        if any(palabra in texto.lower() for palabra in palabras_formales):
            self.contexto['conversacion']['tono'] = 'formal'
        elif any(palabra in texto.lower() for palabra in palabras_informales):
            self.contexto['conversacion']['tono'] = 'informal'
        elif any(palabra in texto.lower() for palabra in palabras_tecnicas):
            self.contexto['conversacion']['tono'] = 'técnico'
    
    def _identificar_intereses(self, texto):
        intereses_clave = {
            'programación': ['programar', 'código', 'python', 'javascript'],
            'música': ['música', 'cantar', 'guitarra', 'canción'],
            'deportes': ['fútbol', 'deporte', 'ejercicio', 'correr']
        }
        
        for interes, palabras in intereses_clave.items():
            if any(palabra in texto.lower() for palabra in palabras):
                self.contexto['usuario']['intereses'].add(interes)
    
    def obtener_contexto_para_respuesta(self):
        """Prepara el contexto relevante para generar respuestas"""
        return {
            'nombre': self.contexto['usuario']['nombre'],
            'tema_actual': self.contexto['conversacion']['tema_actual'],
            'tema_anterior': self.contexto['conversacion']['tema_anterior'],
            'tono': self.contexto['conversacion']['tono'],
            'intereses': list(self.contexto['usuario']['intereses'])[-3:] if self.contexto['usuario']['intereses'] else None
        }
    
    def limpiar_contexto(self):
        """Reinicia el contexto manteniendo solo datos personales"""
        self.contexto['conversacion'] = {
            'tema_actual': None,
            'tema_anterior': None,
            'historial_temas': [],
            'tono': 'neutral'
        }
        self.contexto['ultima_actualizacion'] = datetime.now().isoformat()
    
    def guardar_contexto(self, archivo="contexto_conversacion.json"):
        """Guarda el contexto en un archivo JSON"""
        with open(archivo, 'w') as f:
            json.dump(self.contexto, f, indent=2, ensure_ascii=False)
    
    def cargar_contexto(self, archivo="contexto_conversacion.json"):
        """Carga el contexto desde un archivo JSON"""
        try:
            with open(archivo, 'r') as f:
                self.contexto = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.contexto = self._inicializar_contexto()