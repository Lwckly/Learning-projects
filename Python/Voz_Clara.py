import speech_recognition as sr
import torch
import numpy as np
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from pydub import AudioSegment
import io
import librosa

# --- 1. CARREGAMENTO DO MODELO WHISPER ---
# Esta parte é a mesma do nosso servidor, carregamos o modelo uma vez.

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "openai/whisper-base"

print("--- Iniciando Script de Teste de Transcrição ---")
print(f"Usando dispositivo: {DEVICE}")
print(f"Carregando modelo Whisper: '{MODEL_NAME}'...")

try:
    processor = WhisperProcessor.from_pretrained(MODEL_NAME)
    model = WhisperForConditionalGeneration.from_pretrained(MODEL_NAME).to(DEVICE)
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"Erro fatal ao carregar o modelo: {e}")
    exit()

# --- 2. LÓGICA DE GRAVAÇÃO E TRANSCRIÇÃO ---

# Inicializa o reconhecedor de fala
recognizer = sr.Recognizer()

try:
    # Usa o microfone como fonte de áudio
    with sr.Microphone(sample_rate=16000) as source:
        print("\nAjustando para o ruído ambiente, por favor aguarde...")
        # Ajusta o nível de energia do reconhecedor para o ruído ambiente
        recognizer.adjust_for_ambient_noise(source, duration=2)
        
        # Aumenta o timeout e phrase_time_limit para capturar mais áudio
        print("\nPode falar! Estou ouvindo... (fale por pelo menos 2-3 segundos)")

        # Escuta o áudio do microfone com timeout maior
        audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=10)

        print("\nGravação concluída, processando...")

        # Converte o áudio gravado para o formato de bytes WAV
        wav_bytes = audio_data.get_wav_data()
        print(f"Tamanho do áudio capturado: {len(wav_bytes)} bytes")

        # Converte os bytes WAV para o formato que o Whisper precisa (array NumPy)
        # Usamos librosa para melhor processamento
        audio_segment = AudioSegment.from_file(io.BytesIO(wav_bytes), format="wav")
        
        # Debug: informações sobre o áudio
        print(f"Duração do áudio: {len(audio_segment) / 1000:.2f} segundos")
        print(f"Sample rate: {audio_segment.frame_rate} Hz")
        print(f"Canais: {audio_segment.channels}")
        
        # Converte para mono se necessário
        if audio_segment.channels > 1:
            audio_segment = audio_segment.set_channels(1)
        
        # Garante que o sample rate seja 16kHz
        if audio_segment.frame_rate != 16000:
            audio_segment = audio_segment.set_frame_rate(16000)
        
        # Converte para array numpy
        samples = np.array(audio_segment.get_array_of_samples()).astype(np.float32)
        
        # Normaliza o áudio corretamente
        if audio_segment.sample_width == 2:  # 16-bit
            samples = samples / 32768.0
        elif audio_segment.sample_width == 4:  # 32-bit
            samples = samples / 2147483648.0
        else:  # 8-bit
            samples = samples / 128.0
        
        print(f"Shape do array de áudio: {samples.shape}")
        print(f"Valores min/max do áudio: {samples.min():.4f} / {samples.max():.4f}")
        
        # Verifica se o áudio não está muito baixo
        if np.abs(samples).max() < 0.01:
            print("AVISO: Áudio muito baixo! Tente falar mais alto.")
        
        # Processa e transcreve o áudio com o Whisper
        print("Processando com Whisper...")
        input_features = processor(
            samples,
            sampling_rate=16000,
            return_tensors="pt"
        ).input_features.to(DEVICE)
        
        print(f"Shape das features de entrada: {input_features.shape}")

        # Gera a transcrição com parâmetros melhorados
        predicted_ids = model.generate(
            input_features,
            max_length=448,
            num_beams=5,
            do_sample=True,
            temperature=0.6,
            language="pt",  # Força português
            task="transcribe"
        )
        
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        # Imprime o resultado final
        print("-" * 50)
        print(f"TEXTO TRANSCRITO: '{transcription}'")
        print(f"Tamanho da transcrição: {len(transcription)} caracteres")
        print("-" * 50)

except sr.UnknownValueError:
    print("Não foi possível entender o áudio. Tente falar mais claramente.")
except sr.RequestError as e:
    print(f"Erro no serviço de reconhecimento; {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

#temos o modelo funcionando, estamos resolvendo a parte dos dados
