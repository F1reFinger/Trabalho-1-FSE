import RPi.GPIO as GPIO
from socket import *
import _signal
from _signal import *
import json
import time
import datetime
import csv
import Adafruit_dht

# Define o padrao de numeracao das portas como BCM
# A outra opcap e GPIO.BOARD para usar o numero dos pinos fisicos da placa
GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM) 

global NumSala

#inicializa o sensor de dht 
DHT_SENSOR = Adafruit_DHT.DHT22

# Configuracao dos pinos do botao e dos LEDs
luz1 = -1
luz2 = -1
air = 1
projetor = -1
alarme = -1
pir = -1
SFum = -1
SJan = -1
SPor = -1
SC_in = -1
SC_out = -1
DHT_PIN = -1

light1 = 0 # 0 é desligada e 1 é ligada
light2 = 0 # 0 é desligada e 1 é ligada

def Temp():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    
        if humidity is not None and temperature is not None:
            return humidity, temperature
        else:
            print("Não foram encontrados dados do sensor!!")

##########################################################################################

def Board1():
    with open('configuracao_sala_01.json', 'r') as f:
        data = json.load(f)
        host = data["ip_servidor_distribuido"]
        port = data["porta_servidor_distribuido"]
    f.close()
    global server1
    server1 = socket(AF_INET, SOCK_STREAM)
    server1.bind((host, port))
    server1.listen()
    global porta1
    global cliente1
    porta1, cliente1 = server1.accept()

def PlacasImpares():
    global mensageiro1
    with open('configuracao_sala_01.json', 'r') as f:
        data = json.load(f)
        IPrincipal = data["ip_servidor_distribuido"]
        porta = data["porta_servidor_distribuido"]
    f.close()
    mensageiro1 = socket(AF_INET, SOCK_STREAM)
    destino = (IPrincipal, porta)
    mensageiro1.connect(destino)

##########################################################################################    

def Board2():
    with open('configuracao_sala_02.json', 'r') as f:
        data = json.load(f)
        host = data["ip_servidor_distribuido"]
        port = data["porta_servidor_distribuido"]
    f.close()
    global server2
    server2 = socket(AF_INET, SOCK_STREAM)
    server2.bind((host, port))
    server2.listen()
    global porta2
    global cliente2
    porta2, cliente2 = server2.accept()

def PlacasPares():
    global mensageiro2
    with open('configuracao_sala_02.json', 'r') as f:
        data = json.load(f)
        IPrincipal = data["ip_servidor_distribuido"]
        porta = data["porta_servidor_distribuido"]
    f.close()
    mensageiro2 = socket(AF_INET, SOCK_STREAM)
    destino = (IPrincipal, porta)
    mensageiro2.connect(destino)

##########################################################################################

def IniciaPinos():

    global luz1
    global luz2 
    global air
    global projetor
    global alarme
    global pir
    global SFum
    global SJan
    global SPor
    global SC_in
    global SC_out
    global DHT_PIN
    #-----------------------------------------------------------------------------------------

    if NumSala ==1:
        Board1()
        with open('configuracao_sala_01.json', 'r') as f:
            data = json.load(f)
            luz1 = data["outputs"][0]["gpio"]
            luz2 = data["outputs"][1]["gpio"]
            projetor = data["outputs"][2]["gpio"]
            air = data["outputs"][3]["gpio"]
            
            alarme = data["outputs"][4]["gpio"]
            pir = data["inputs"][0]["gpio"]
            SFum = data["inputs"][1]["gpio"]
            SJan = data["inputs"][2]["gpio"]
            SPor = data["inputs"][3]["gpio"]
            SC_in = data["inputs"][4]["gpio"]
            SC_out = data["inputs"][5]["gpio"]
            DHT_PIN = data["sensor_temperatura"][0]["gpio"]
        f.close()
    elif NumSala ==2 :
        Board2()
        with open('configuracao_sala_02.json', 'r') as f:
            data = json.load(f)
            luz1 = data["outputs"][0]["gpio"]
            luz2 = data["outputs"][1]["gpio"]
            projetor = data["outputs"][2]["gpio"]
            air = data["outputs"][3]["gpio"]
            
            alarme = data["outputs"][4]["gpio"]
            pir = data["inputs"][0]["gpio"]
            SFum = data["inputs"][1]["gpio"]
            SJan = data["inputs"][2]["gpio"]
            SPor = data["inputs"][3]["gpio"]
            SC_in = data["inputs"][4]["gpio"]
            SC_out = data["inputs"][5]["gpio"]
            DHT_PIN = data["sensor_temperatura"][0]["gpio"]
        f.close()

    #-----------------------------------------------------------------------------------------
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

    #-----------------------------------------------------------------------------------------

    GPIO.add_event_detect(SJan, GPIO.BOTH)#
    GPIO.add_event_detect(SPor, GPIO.BOTH)#
    GPIO.add_event_detect(pir, GPIO.BOTH)#   Eventos
    GPIO.add_event_detect(SFum, GPIO.RISING)#
    GPIO.add_event_detect(SC_in, GPIO.RISING)#
    GPIO.add_event_detect(SC_out, GPIO.RISING)#

##########################################################################################

def leituraSensor():
    if GPIO.event_detected(SJan):
        if GPIO.input(SJan)==1:
            return 11

    if GPIO.event_detected(SPor):
        if GPIO.input(SPor)==1:
            return 12

    if GPIO.event_detected(pir):
        if GPIO.input(pir)==1:
            return 13
    
    return 0

    #-------------------------------------------------------------------------------------------

## Funcoes Ligar e desligar luzes e sensores
def Luz01():
    if light1 == 0:
        GPIO.output(luz1, GPIO.HIGH)
        print("Luz 01 ligada")
        light1 = 1

    if light1 == 1:
        GPIO.output(luz1, GPIO.LOW)
        print("Luz 01 ligada")
        light1 = 0 

def Luz02():
    if light2 == 0:
        GPIO.output(luz2, GPIO.HIGH)
        print("Luz 02 ligada")
        light2 = 1

    if light2 == 1:
        GPIO.output(luz2, GPIO.LOW)
        print("Luz 02 ligada")
        light2 = 0 

##########################################################################################

def ligAr():
    GPIO.output(air, GPIO.HIGH)
    print("Ar condicionado ligado")

def desligAR():
    GPIO.output(air, GPIO.LOW)
    print("Ar condicionado desligado")

def ligaPR():
    GPIO.output(projetor, GPIO.HIGH)
    print("Projetor ligado")

def desligaPR():
    GPIO.output(projetor, GPIO.LOW)
    print("Projetor desligado")
        
def LigaCargas():
    GPIO.output(luz1, GPIO.HIGH)
    GPIO.output(luz2, GPIO.HIGH)
    GPIO.output(air, GPIO.HIGH)
    GPIO.output(projetor, GPIO.HIGH)

def Descargas():
    GPIO.output(luz1, GPIO.LOW)
    GPIO.output(luz2, GPIO.LOW)
    GPIO.output(air, GPIO.LOw)
    GPIO.output(projetor, GPIO.LOW)

def LigaLuz():
    GPIO.output(luz1, GPIO.HIGH)
    GPIO.output(luz2, GPIO.HIGH)

def Desliga():
    GPIO.output(luz1, GPIO.LOW)
    GPIO.output(luz2, GPIO.LOW)

##########################################################################################

# Sistema de alarme
def ligarAlarme():
    global alarme
    if GPIO.input(SJan)==1 or GPIO.input(SPor)==1 or GPIO.input(pir)==1 or GPIO.input(SFum)==1 or GPIO.input(SC_in)==1 or GPIO.input(SC_out)==1:
        print("Não é possível ligar o sistema de alarme")
        print("Verifique os sensores!")
        data = datetime.datetime.now()
        with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([data, 'Não foi possivel ligar o sistema de alarme, verifique os sensores'])
        alarme = 0
    else:
        print("Sistema de alarme ligado")
        data = datetime.datetime.now()
        with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([data, 'alarme ligado'])	
        alarme = 1

def desligarAlarme():
    print("Sistema de larme desligado")
    global alarme
    alarme = 0
    if leituraSensor() == 11 or leituraSensor() == 12 or leituraSensor() == 13:
        LigaLuz()
        time.sleep(15)
        Desliga()

##########################################################################################

def AlertaGeral():
    GPIO.output(alarme, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(alarme, GPIO.LOW)

def Fumacento():
    if GPIO.event_detected(SFum):
        print("Fumaça Detectada!!")
        print("Fujam para as colinas!!")
        AlertaGeral()
        print("Sirene ligada")

##########################################################################################

def ContaPeople():
    global pessoas
    if GPIO.event_detected(SC_in):
        pessoas += 1
    elif GPIO.event_detected(SC_out):
        pessoas += -1
    if sala == 1:
        server1.send(bytes(pessoas,"utf8")) 
    elif sala == 2:
        server2.send(bytes(pessoas,"utf8")) 

##########################################################################################

def main():
    global alarme
    global sala
    sala = int(input("Esta sala usa configuração 1 ou 2?"))
    IniciaPinos()
    desligarAlarme()
    GPIO.output(alarme, GPIO.LOW)
    while True:

        if sala == 1: 
            msg = porta1.recv(1024)
            if not msg:
                break
            print("recebido:", msg.decode())
            porta1.send(msg)

            if msg.decode() == "L01":
                Luz01()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luz 01 ligada'])
            elif msg.decode() == "DL01":
                Luz01()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luz 01 desligada'])
            elif msg.decode() == "L02":
                Luz02()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luz 02 ligada'])
            elif msg.decode() == "DL02":
                Luz02()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luz 02 desligada'])
            elif msg.decode() == "AC":
                ligAr()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'AC ligado'])
            elif msg.decode() == "DAC":
                desligAR()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'AC desligado'])
            elif msg.decode() == "PR":
                ligaPR()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Projetor ligado'])
            elif msg.decode() == "DPR":
                desligaPR()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Projetor desligado'])
            elif msg.decode() == "AL":
                ligarAlarme()
            elif msg.decode() == "DAL":
                desligarAlarme()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Alarme desligado'])
            elif msg.decode() == "L12":
                LigaLuz()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luzes ligadas'])
            elif msg.decode() == "D12":
                Desliga()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luzes desligadas'])
            elif msg.decode() == "LG":
                LigaCargas()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Cargas ligadas'])
            elif msg.decode() == "DG":
                Descargas()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Cargas desligadas'])
            elif msg.decode() == "x":
                server1.close()
                break
        
        
        elif sala == 2:
            msg = porta2.recv(1024)
            if not msg:
                break
            print("recebido:", msg.decode())
            porta2.send(msg)

            if msg.decode() == "L01":
                Luz01()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luz 01 ligada'])
            elif msg.decode() == "DL01":
                Luz01()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luz 01 desligada'])
            elif msg.decode() == "L02":
                Luz02()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luz 02 ligada'])
            elif msg.decode() == "DL02":
                Luz02()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luz 02 desligada'])
            elif msg.decode() == "AC":
                ligAr()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'AC ligado'])
            elif msg.decode() == "DAC":
                desligAR()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'AC desligado'])
            elif msg.decode() == "PR":
                ligaPR()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Projetor ligado'])
            elif msg.decode() == "DPR":
                desligaPR()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Projetor desligado'])
            elif msg.decode() == "AL":
                ligarAlarme()
            elif msg.decode() == "DAL":
                desligarAlarme()
                data = datetime.datetime.now()
                with open('./logs/log_sala1.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Alarme desligado'])
            elif msg.decode() == "L12":
                LigaLuz()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luzes ligadas'])
            elif msg.decode() == "D12":
                Desliga()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Luzes desligadas'])
            elif msg.decode() == "LG":
                LigaCargas()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Cargas ligadas'])
            elif msg.decode() == "DG":
                Desliga()
                data = datetime.datetime.now()
                with open('./logs/log_sala2.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=':' , quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([data, 'Cargas desligadas'])
            elif msg.decode() == "x":
                server2.close()
                break
        if alarme == 1:
            if GPIO.input(pir)==1  or GPIO.input(SPor) ==1 or GPIO.input(SJan)==1 :
                GPIO.output(alarme, GPIO.HIGH)
                print("Sirene ligada!")

if __name__ == "__main__":
    main()