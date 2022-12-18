import json
 
#def Gravador(b):
    #sensores = {
    #    "brabo":{
    #        "Janelas": b
    #    }
    #}   

    # Serializing json
    #json_object = json.dumps(sensores, indent=4)

    #with open("Testeiro.json", "w") as outfile:
    #    outfile.write(json_object)

    #print("Valores Gravados com sucesso!")

def LeData():
    with open('configuracao_sala_01.json', 'r') as f:
        data = json.load(f)
    
    print(data["nome"])

    # Closing file
    f.close()

    
LeData()