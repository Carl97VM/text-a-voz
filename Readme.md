# Proyecto: Generador de Voz - Clonación IA (Local y Cloud)

Este proyecto extrae una voz de un archivo de audio comprimido, la aísla mediante separación de pistas con IA (Demucs) y permite clonar la voz para generar nuevos diálogos. Soporta dos modalidades: generación local gratuita (Coqui XTTS) o mediante la API en la nube (ElevenLabs).

## Prerrequisitos
- **Python 3.8 a 3.11** (Versiones superiores pueden dar problemas con dependencias de IA).
- **FFmpeg** instalado en las variables de entorno (`winget install ffmpeg` en Windows).
- **Microsoft Visual C++ Build Tools**: Obligatorio para compilar las librerías locales de TTS. Seleccionar el paquete "Desarrollo para el escritorio con C++" en el instalador de Visual Studio.
- (Opcional) Una cuenta en [ElevenLabs](https://elevenlabs.io/) con suscripción de pago (Starter o superior) para usar el script en la nube.

## Estructura de Archivos
- `pista.m4a`: Audio fuente que contiene la voz de referencia.
- `requirements.txt`: Lista de dependencias con versiones específicas para evitar errores de PyTorch y C++ en Windows.
- `1_convertir.py`: Convierte el audio comprimido a WAV puro y de alta fidelidad.
- `2_aislar.py`: Utiliza `demucs` para separar la voz de la música de fondo (contiene parches para puentear `torchcodec`).
- `3_generar_voz.py`: (Opción Cloud) Se conecta a la API de ElevenLabs, clona la voz y genera el audio.
- `4_clonar_local.py`: (Opción Local) Utiliza el modelo Open-Source Coqui XTTSv2 para clonar la voz sin internet y sin costo, procesado directamente en tu hardware.

## Configuración del Entorno (Windows PowerShell)

1. **Crear el entorno virtual:**
   ```powershell
   python -m venv venv

   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

   # En PowerShell
    .\venv\Scripts\activate

    # En Git Bash (MINGW64)
    source venv/Scripts/activate
    ```

##  Instalacion
2. **Dependencias**
``` bash
pip install -r requirements.txt
```
## Ejecucion
3. **Ejecucion**
``` bash
# 1. Convierte a WAV
python 1_convertir.py

# 2. Extrae la voz limpia (Genera carpeta /separated/)
python 2_aislar.py

python 4_clonar_local.py
```