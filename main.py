from core.neuronas import Neurona
from core.procesamiento import crear_vocabulario, vectorizar_frases, clase_a_vector
from data.respuestas import obtener_respuesta_por_clase
from core.logs import MemoriaConversacional
from core.contexto import GestorContexto
from data.datos import datatabase, clases
import json

class AsistenteVirtual:
    def __init__(self):
        # Inicializar componentes
        self.vocabulario = crear_vocabulario(datatabase)
        self.modelo = self._cargar_modelo()
        self.memoria = MemoriaConversacional()
        self.contexto = GestorContexto()
        
        # Configuración
        self.umbral_confianza = 0.4
        
    def _cargar_modelo(self):
        try:
            return Neurona.load("modelo_chat.json")
        except (FileNotFoundError, json.JSONDecodeError):
            print("Entrenando modelo por primera vez...")
            return self._entrenar_modelo()
    
    def _entrenar_modelo(self):
        X = [vectorizar_frases(frase, self.vocabulario) for frase, _ in datatabase]
        Y = [clase_a_vector(clase, clases) for _, clase in datatabase]
        
        modelo = Neurona(len(self.vocabulario), 5, len(clases), lr=0.2)
        modelo.train(X, Y, epochs=1000)
        modelo.save("modelo_chat.json")
        return modelo
    
    def predecir_clase(self, texto):
        vector = vectorizar_frases(texto, self.vocabulario)
        salida = self.modelo.forward(vector)
        confianza = max(salida)
        clase_pred = clases[salida.index(confianza)]
        
        # Mapeo de clases relacionadas
        if confianza < self.umbral_confianza:
            if "clima" in texto.lower() or "tiempo" in texto.lower():
                return "pronóstico del tiempo", 0.4
            if "llamar" in texto.lower() or "nombre" in texto.lower():
                return "saludo", 0.8
        
        return clase_pred, confianza
    def generar_respuesta(self, texto_usuario):
        # Preprocesar entrada
        texto_usuario = texto_usuario.strip()
        
        # Predecir clase y obtener respuesta base
        clase, confianza = self.predecir_clase(texto_usuario)
        respuesta_base = obtener_respuesta_por_clase(clase)
        
        # Actualizar contexto
        self.contexto.actualizar_contexto(texto_usuario, respuesta_base)
        ctx = self.contexto.obtener_contexto_para_respuesta()
        
        # Personalizar respuesta
        respuesta = self._personalizar_respuesta(respuesta_base, ctx, confianza)
        
        # Registrar en memoria
        self.memoria.guardar_interaccion(
            usuario=texto_usuario,
            asistente=respuesta,
            contexto=ctx
        )
        
        return respuesta
    
    def _personalizar_respuesta(self, respuesta, contexto, confianza):
        # Personalización basada en nombre
        if contexto['nombre']:
            respuesta = respuesta.replace("Hola", f"Hola {contexto['nombre']}")
            respuesta = respuesta.replace("tú", contexto['nombre'])
        
        # Personalización basada en tema
        if contexto['tema_actual']:
            if contexto['tema_actual'] == 'programación':
                respuesta += " ¿Estás trabajando en algún proyecto interesante?"
            elif contexto['tema_actual'] == 'música':
                respuesta += " ¿Qué género musical prefieres?"
        
        # Manejo de baja confianza
        if confianza < self.umbral_confianza:
            respuesta += " No estoy seguro de entender completamente. ¿Podrías explicarlo de otra manera?"
        
        # Ajuste de tono
        if contexto['tono'] == 'formal':
            respuesta = respuesta.replace("!", ".").replace("¿", "").capitalize()
        elif contexto['tono'] == 'informal':
            respuesta += " 😊"
        
        return respuesta
    
    def obtener_historial_reciente(self, n=3):
        return self.memoria.historial[-n:] if len(self.memoria.historial) >= n else self.memoria.historial

def iniciar_chat():
    asistente = AsistenteVirtual()
    print("\nAsistente: ¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?")
    print("(Escribe 'salir', 'adiós' o 'chao' para terminar la conversación)\n")
    
    while True:
        try:
            user_input = input("Tú: ")
            
            # Verificar comando de salida
            if user_input.lower() in ['salir', 'adiós', 'chao', 'hasta luego']:
                print("\nAsistente: ¡Hasta luego! Fue un gusto ayudarte.")
                if hasattr(asistente.contexto, 'nombre'):
                    print(f"Asistente: ¡Que tengas un buen día, {asistente.contexto.contexto['usuario']['nombre']}!")
                break
            
            # Generar y mostrar respuesta
            respuesta = asistente.generar_respuesta(user_input)
            print(f"Asistente: {respuesta}")
            
            # Mostrar contexto (opcional, para depuración)
            if "--debug" in user_input:
                print("\n[DEBUG] Contexto actual:")
                print(json.dumps(asistente.contexto.obtener_contexto_para_respuesta(), indent=2))
                print("Últimas interacciones:")
                for i, interaccion in enumerate(asistente.obtener_historial_reciente(2)):
                    print(f"{i+1}. Usuario: {interaccion['usuario']}")
                    print(f"   Asistente: {interaccion['asistente']}\n")
            
        except KeyboardInterrupt:
            print("\nAsistente: ¡Vaya! Parece que quieres interrumpir la conversación. ¿Necesitas algo más?")
        except Exception as e:
            print(f"\nAsistente: ¡Ups! Algo salió mal: {str(e)}")
            print("Por favor, intenta formular tu pregunta de otra manera.")

if __name__ == "__main__":
    iniciar_chat()