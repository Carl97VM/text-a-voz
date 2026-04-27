import os
import sys
import torch
import torchaudio
import soundfile as sf

# --- PARCHE 1: SEGURIDAD DE PYTORCH 2.6+ ---
_original_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = _patched_load

# --- PARCHE 2: PUENTEAR TORCHCODEC Y LEER AUDIO DIRECTO ---
def_original_audio_load = torchaudio.load
def _patched_audio_load(filepath, *args, **kwargs):
    # Convertimos la ruta a un formato absoluto nativo de Windows (E:\...)
    filepath_absoluto = os.path.abspath(filepath)
    
    # Usamos soundfile directo para ignorar a torchcodec
    data, sr = sf.read(filepath_absoluto, dtype='float32')
    tensor = torch.from_numpy(data)
    
    # Ajustamos la forma del audio al formato exacto que pide la IA
    if tensor.ndim == 1:
        tensor = tensor.unsqueeze(0)
    else:
        tensor = tensor.t()
    return tensor, sr
torchaudio.load = _patched_audio_load
# --------------------------------------------------------

from TTS.api import TTS

os.environ["COQUI_TOS_AGREED"] = "1"

def clonar_voz_local(ruta_referencia, texto, archivo_salida):
    print("📥 Cargando el modelo XTTSv2...")
    
    dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"⚙️ Procesando con: {dispositivo.upper()}")
    
    try:
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(dispositivo)
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")
        return

    print("\n🗣️ Generando la voz clonada... (El procesador está trabajando, no lo cierres ☕)")
    
    tts.tts_to_file(
        text=texto,
        speaker_wav=ruta_referencia,
        language="es",
        file_path=archivo_salida
    )
    print(f"\n🎉 ¡Hack completado! Tu audio final está listo en: {archivo_salida}")

if __name__ == "__main__":
    # Construimos la ruta de forma segura para Windows
    ruta_vocals = os.path.join("separated", "htdemucs", "audio_base", "vocals.wav")
    ruta_absoluta = os.path.abspath(ruta_vocals)
    
    # Verificación de seguridad antes de arrancar la IA
    if not os.path.exists(ruta_absoluta):
        print(f"❌ ERROR CRÍTICO: No se encontró el archivo de audio en:\n{ruta_absoluta}")
        print("Asegúrate de que el script de Demucs (2_aislar.py) se ejecutó correctamente y generó la carpeta.")
        sys.exit(1)
        
    mi_guion = """
    Atención, estudiantes del Colegio Villegas… 
    de primero a sexto de secundaria… 
    (tono pausado y firme) 
    El tiempo ha comenzado. 
    Tienen exactamente… 5 minutos 
    para dirigirse a la pista de baile 
    y acompañar a sus padres de familia. 
    …. 
    . 
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
    
    archivo_final = "anuncio_calamar_local.wav"
    
    clonar_voz_local(ruta_absoluta, mi_guion, archivo_final)