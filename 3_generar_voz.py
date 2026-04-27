from elevenlabs.client import ElevenLabs
from elevenlabs import save

# Reemplaza 'tu_api_key_aqui' con tu clave real de ElevenLabs
API_KEY = "sk_6434f74995501dfaa95f9ddead5c5d57bce1a17dea55b6d0"
client = ElevenLabs(api_key=API_KEY)

def clonar_y_hablar(ruta_voz_limpia, texto_guion):
    print("🎙️ Subiendo muestra de voz para clonación...")
    
    try:
        # 1. Crear el Clon de Voz (Sintaxis actualizada - ivc = Instant Voice Clone)
        voz_clonada = client.voices.ivc.create(
            name="Locutora Calamar",
            description="Voz formal y fría para festividad académica",
            files=[ruta_voz_limpia]
        )
        print(f"✅ ¡Voz clonada en los servidores! ID interno: {voz_clonada.id}")
        
        print("🗣️ Generando el nuevo diálogo...")
        # 2. Generar el audio llamando al motor de Text-to-Speech
        audio_generado = client.text_to_speech.convert(
            text=texto_guion,
            voice_id=voz_clonada.id,
            model_id="eleven_multilingual_v2", # Fundamental para que hable en español perfecto
            output_format="mp3_44100_128"
        )
        
        # 3. Guardar el archivo de audio bit a bit
        archivo_final = "anuncio_festividad.mp3"
        with open(archivo_final, "wb") as f:
            for chunk in audio_generado:
                f.write(chunk)
                
        print(f"🎉 ¡Éxito! Tu audio final está guardado como '{archivo_final}'")
        
    except Exception as e:
        print(f"\n❌ Ocurrió un error con la API de ElevenLabs:")
        print(f"{e}")
        print("👉 Consejo: Verifica que tu plan de ElevenLabs permita clonación (Starter o superior) y que tu API Key tenga los permisos correctos.")

if __name__ == "__main__":
    ruta_vocals = "separated/htdemucs/audio_base/vocals.wav"
    
    mi_guion = """
    Atención, estudiantes del Colegio Villegas…
    de primero a sexto de secundaria…
    (tono pausado y firme)
    El tiempo ha comenzado.
    Tienen exactamente… 5 minutos
    para dirigirse a la pista de baile
    y acompañar a sus padres de familia.
    …..
    Este no es un juego cualquiera…
    es el desafío de la unión,
    la alegría… y el trabajo en equipo.
    Quienes acepten el reto,
    demostrarán valentía, entusiasmo
    y amor por su familia.
    Quienes no participen…
    simplemente perderán la oportunidad
    de vivir un momento único e inolvidable.
    ¡El reloj está corriendo!
    Reúnanse con sus padres,
    tomen su lugar en la pista…
    y prepárense para el gran baile sorpresa.
    (voz firme, cierre)
    Estudiantes del Colegio Villegas…
    ¿aceptan el desafío?
    ¡Que comience el juego!
    """
    
    clonar_y_hablar(ruta_vocals, mi_guion)