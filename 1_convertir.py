from pydub import AudioSegment

def preparar_audio(archivo_entrada):
    archivo_salida = "audio_base.wav"
    print(f"🔄 Convirtiendo {archivo_entrada} a WAV...")
    
    formato = archivo_entrada.split('.')[-1]
    audio = AudioSegment.from_file(archivo_entrada, format=formato)
    
    audio.export(archivo_salida, format="wav", parameters=["-ar", "44100"])
    print(f"✅ Audio listo: {archivo_salida}")

if __name__ == "__main__":
    # Actualizado a tu archivo existente
    preparar_audio("pista.m4a")