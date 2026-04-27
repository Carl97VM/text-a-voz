import sys
import torchaudio
import soundfile as sf

# --- PARCHE MAESTRO: GUARDAR AUDIO SIN TORCHCODEC ---
def _patched_audio_save(filepath, src, sample_rate, *args, **kwargs):
    # Demucs entrega el audio al revés de lo que espera Windows. 
    # Lo transponemos (.t()) y lo pasamos a un arreglo básico (.numpy())
    data = src.t().cpu().numpy()
    # Guardamos usando soundfile directamente
    sf.write(str(filepath), data, sample_rate, subtype='PCM_16')

torchaudio.save = _patched_audio_save
# ----------------------------------------------------

from demucs.separate import main

def aislar_voz(archivo_wav):
    print("🧠 Iniciando Demucs (Versión Parcheada) para separar la voz...")
    
    # Engañamos a Python inyectando el comando como si lo hubieras escrito en la terminal
    sys.argv = ["demucs", archivo_wav]
    
    try:
        main()
        print("\n✅ ¡Separación completada y guardada con éxito!")
        print("El archivo 'vocals.wav' ya está listo en 'separated/htdemucs/audio_base/'")
    except SystemExit as e:
        # Demucs tiene la costumbre de cerrar el programa entero al terminar (SystemExit).
        # Si el código es 0, significa que terminó perfectamente bien.
        if e.code == 0:
            print("\n✅ ¡Separación completada y guardada con éxito!")
            print("El archivo 'vocals.wav' ya está listo para ser clonado.")
        else:
            print(f"❌ Ocurrió un error inesperado al salir de Demucs: {e.code}")

if __name__ == "__main__":
    aislar_voz("audio_base.wav")