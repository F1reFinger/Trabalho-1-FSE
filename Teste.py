#import RPi.GPIO as GPIO
import _signal
from _signal import *
import json
from time import sleep

# Define o padrao de numeracao das portas como BCM
# A outra opcap e GPIO.BOARD para usar o numero dos pinos fisicos da placa
GPIO.setmode(GPIO.BCM) 

# Configuracao dos pinos do botao e dos LEDs
botao = 3 # (GPIO 3) - Pino 5
lampadas = [18, 23] # (GPIO 13, 19, 26) - Pinos 33, 35, 37
air = 24
projetor = 25
alarme = 8
pir = 7
SFum = 1
SJan = [12, 16]
SC_in = 20
SC_out = 21
DHT22 = 4



# Configuracao dos Pinos como Entradas / Saidas
GPIO.setup(lampadas, GPIO.OUT)#
GPIO.setup(air, GPIO.OUT)#
GPIO.setup(projetor, GPIO.OUT)# Saidas
GPIO.setup(alarme, GPIO.OUT)#

GPIO.setup(pir, GPIO.IN)#
GPIO.setup(SFum, GPIO.IN)#
GPIO.setup(SJan, GPIO.IN)#  Entradas
GPIO.setup(SC_in, GPIO.IN)#
GPIO.setup(SC_out, GPIO.IN)#

def LeData():
    # Opening JSON file
    f = open('data.json')
  
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
  
    # Iterating through the json
    # list
    for i in data['emp_details']:
        print(i)
  
    # Closing file
    f.close()

def escreveData():
    # Data to be written
    dictionary = {
        "Lampadas": lampadas,
        "AC": 1,
        "TEmperatura": 25.3
    }
 
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
 
    # Writing to sample.json
    with open("Data.json", "w") as outfile:
        outfile.write(json_object)

    
# Configura deteccao de acao do Botao
GPIO.add_event_detect(botao, GPIO.FALLING) # GPIO.RISING

# conta de 0 a 7
while True:
    escreveData()
    a = input()
    if(a):
        print("parabens pelo true statement")
    else:
        exit