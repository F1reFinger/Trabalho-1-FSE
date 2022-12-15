import RPi.GPIO as GPIO
import _signal
from _signal import *
import json
from time import sleep
import board
import adafruit_dht

# Define o padrao de numeracao das portas como BCM
# A outra opcap e GPIO.BOARD para usar o numero dos pinos fisicos da placa
GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM) 

# Configuracao dos pinos do botao e dos LEDs

luz1 = 18
luz2 = 23
air = 24
projetor = 25
alarme = 8
pir = 7
SFum = 1
SJan = 12
SPor = 16
SC_in = 20
SC_out = 21
DHT22 = 4



def LeData():
    with open('configuracao_sala_02.json', 'r') as f:
        data = json.load(f)
    
    print(data["nome"])

    # Closing file
    f.close()

def IniciaPinos():
    # Configuracao dos Pinos como Entradas / Saidas
    GPIO.setup(luz1, GPIO.OUT)#
    GPIO.setup(luz2, GPIO.OUT)#
    GPIO.setup(air, GPIO.OUT)#
    GPIO.setup(projetor, GPIO.OUT)# Saidas
    GPIO.setup(alarme, GPIO.OUT)#

    GPIO.setup(pir, GPIO.IN)#
    GPIO.setup(SFum, GPIO.IN)#
    GPIO.setup(SJan, GPIO.IN)#  Entradas
    GPIO.setup(SPor, GPIO.IN)# 
    GPIO.setup(SC_in, GPIO.IN)#
    GPIO.setup(SC_out, GPIO.IN)#/

def Menu():
    print("1 - Ativar/desativar Todas as Lampadas.") 
    print("2 - Ativar/desativar ar condicionado.")
    print("3 - Ativar/desativar Projetor.")
    print("4 - Ativar/Desativar ar condicionado.")
    print("5 - Ligar alarmes.")
    print("6 - Desligar Sistema e sair.")
    sel = int(input())
    if sel == 1:
        print('Lampadas:', GPIO.output(luz1), GPIO.output(luz2))
    elif sel == 2:
        print('Lampadas:', GPIO.output(luz1), GPIO.output(luz2))
    elif sel == 3:
        print('Lampadas:', GPIO.output(luz1), GPIO.output(luz1))
    elif sel == 4:
        print('Lampadas:', GPIO.output(luz1), GPIO.output(luz1))
    elif sel == 5:
        print('Lampadas:', GPIO.output(luz1), GPIO.output(luz1))
    elif sel == 6:
        print('Bye Bye!')
        SystemExit
    else:
        print('Opção invalida!')
        Menu()