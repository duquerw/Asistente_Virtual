import json
from datetime import datetime

class MemoriaConversacional:
    def __init__(self, archivo="memoria_conversacion.json"):
        self.archivo = archivo
        self.historial = self.cargar_historial()
    
    def cargar_historial(self):
        try:
            with open(self.archivo, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def guardar_interaccion(self, usuario, asistente, contexto=None):
        interaccion = {
            "timestamp": datetime.now().isoformat(),
            "usuario": usuario,
            "asistente": asistente,
            "contexto": contexto or {}
        }
        self.historial.append(interaccion)
        self.persistir()
    
    def persistir(self):
        with open(self.archivo, "w") as f:
            json.dump(self.historial, f, indent=2)
    
    def obtener_ultimo_contexto(self):
        return self.historial[-1]["contexto"] if self.historial else {}