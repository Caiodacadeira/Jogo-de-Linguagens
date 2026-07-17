import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import time

erros = 0
pontos = 0

words_by_level = {
    "fácil": ["gato", "cachorro", "maçã", "leite", "sol"],
    "médio": ["casa", "escola", "amigo", "janela", "amarelo"],
    "difícil": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação"]
}

duration = 5  # segundos de gravação
sample_rate = 44100
linguas = {
    "Inglês": "en",
    "Espanhol": "es",
    "Russo": "ru",
    "Indonésio": "id",
    "Polonês": "pl",
    "Italiano": "it",
    "Turco": "tr"
}

print("🤩 Bem-vindo(a) ao jogo de pronúncia! 🤩")

while True:
    time.sleep(1)
    while True:
        time.sleep(1)
        print("Idiomas disponíveis:")
        time.sleep(1)
        for l in linguas.keys():
            print("-", l)
        time.sleep(1)
        idioma = input("Escolha o idioma de fala: ")
        if idioma in linguas:
            break
        else:
            print("⚠️ O Idioma selecionado não está disponível ou foi escrito incorretamente. Tente novamente.⚠️")
    while True:
        time.sleep(1)
        print("Níveis de dificuldade disponíveis:")
        time.sleep(1)
        for n in words_by_level.keys():
            print("-", n)
        time.sleep(1)
        nivel = input("Escolha o nível de dificuldade: ")
        if nivel in words_by_level:
            break
        else:
            print("⚠️ O nível selecionado não está disponível ou foi escrito incorretamente. Tente novamente.⚠️")
    for i in range(len(words_by_level[nivel])):
        time.sleep(1)
        print("A palavra a ser pronunciada é:", words_by_level[nivel][i])
        time.sleep(1)
        print("Começando a gravação de áudio em 3 segundos...")
        time.sleep(1)
        for t in range(3):
            print(3 - t)
            time.sleep(1)
        print("Fale agora...")
        recording = sd.rec(
        int(duration * sample_rate), # o número de amostras a serem registradas
        samplerate=sample_rate,      # taxa de amostras
        channels=1,                  # 1 significa gravação mono
        dtype="int16")               # tipo de dados para as amostras registradas
        sd.wait()  # aguardando o término da gravação

        wav.write("output.wav", sample_rate, recording)
        print("Gravação concluída, comparando resultados...")
        time.sleep(1)

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio, language=linguas[idioma]).lower()
            translator = Translator()
            translated = translator.translate(text, dest="pt")  # O 'en' aqui é um código para inglês
            if translated.text == words_by_level[nivel][i]:
                print("✅ Parabéns! Você pronunciou a palavra corretamente.✅")
                pontos += 1
            else:
                print("❌ A palavra pronunciada não corresponde à palavra esperada.❌")
                time.sleep(1)
                print("Palavra reconhecida:", translated.text)
                erros += 1
        except sr.UnknownValueError:             # - se o Google não conseguiu entender a fala devido a ruídos ou silêncio
            print("⚠️ A fala não pôde ser reconhecida devido a ruídos ou silêncio. Verifique se o microfone está funcionando corretamente e tente novamente.⚠️")
            break
        except sr.RequestError as e:             # - se não houver conexão com a Internet ou a API estiver indisponível
            print(f"Service error: {e}")
            print("⚠️ Ocorreu um erro ao tentar se conectar ao serviço de reconhecimento de fala. Verifique sua conexão com a Internet e tente novamente.⚠️")
            break
        if i == len(words_by_level[nivel]) - 1 or erros >= 3:
            print("Fim do jogo!")
            time.sleep(1)
            print("Pontuação final:", pontos)
            print("Número de erros:", erros)
            tent = input("Deseja rejogar? (s/n): ")
            if tent.lower() == "s":
                erros = 0
                pontos = 0
                break
            else:
                print("😁 Obrigado por jogar!😁")
                exit()
