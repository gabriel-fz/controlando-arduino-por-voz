import speech_recognition as sr
import spacy
from pyfirmata import Arduino, util
import time
board = Arduino('COM4')


nlp = spacy.load('pt')

coresLed = ['verde', 'vermelho', 'amarelo', 'branco', 'vermelha', 'amarela', 'branca', 'todos']

comandosLed = ['acender', 'apagar', 'ligar', 'desligar', 'animar', 'brincar']

def cor_equivalente(cor):
    if cor == "verde":
        return 5
    elif cor == "vermelho" or cor == "vermelha":
        return 3
    elif cor == "amarelo" or cor == "amarala":
        return 4
    elif cor == "branco" or cor == "branca":
        return 2
    elif cor == "todos":
        return "10"

def execucao(instrucao,cor):
    num_cor = cor_equivalente(cor)
    if (instrucao == "acender" or instrucao == "ligar"):
        print("LED ", num_cor, " aceso")
        board.digital[num_cor].write(1)
    elif (instrucao == "apagar" or instrucao == "desligar"):
        print("LED ", num_cor, " apagado")
        board.digital[num_cor].write(0)
    elif (instrucao == "animar" or instrucao == "brincar"):
        print("LED ", num_cor, "animado")
        for i in range(5):
            board.digital[num_cor].write(1)
            time.sleep(0.3)
            board.digital[num_cor].write(0)
            time.sleep(0.3)


def ouvir_microfone():
	microfone = sr.Recognizer()
	with sr.Microphone() as source:
		microfone.adjust_for_ambient_noise(source)
		print("Diga alguma coisa: ")
		audio = microfone.listen(source)
	try:
		frase = microfone.recognize_google(audio,language='pt-BR')
		print("Você disse: " + frase.lower())
	except sr.UnkownValueError:
		print("Não entendi")
	return frase.lower()

def reconhecer_comandos(instrucao, corDetectada):
        for token in doc:
                for comando in comandosLed:
                        if (comando == token.lemma_) and ((token.pos_) == 'VERB'):
                                print("comando: ",token.lemma_)
                                instrucao = token.lemma_
                for cor in coresLed:
                        if cor == token.text:
                                execucao(instrucao,cor)
                                corDetectada = cor
        if instrucao == "":
            print("Não detectei algum comando correspondente")
        if corDetectada == "":
            print("Não detectei nenhuma cor dos LEDs correspondentes")
            

print("Bem vindo ao controle de voz")

condicao = True
while(condicao):
    decisao = input('\nDigite ENTER para falar e Q para sair: ')
    if(decisao == "Q" or decisao == "q"):
        print("\nFim do programa")
        break
    frase = ouvir_microfone()
    doc = nlp(frase)
    reconhecer_comandos("","")
