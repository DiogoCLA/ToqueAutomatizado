import datetime
from dataclasses import dataclass
import operator
import sounddevice as sd
import soundfile as sf
import time

@dataclass
class Toque:
    sound_name: str
    time: str
    channel: str
    week_day: str
    is_active: bool
    school_level: str


"""
Incluir Toque na lista de Toques usando os arugmentos na lista que foram dados como uma 
class descrita acima
"""
def add_toque(args, toque_list):
    new_time = Toque(args[0], args[1], args[2], args[3], bool(args[4]), args[5])
    for time in toque_list:
        if time == new_time:
            return
    toque_list.append(new_time)



"""
Ler arquivo csv e separar itens em uma lista para permitir ser adicionado
"""
def read_data_csv(csvfile, lst):
    for line in open('toque.csv'):
        args = line.rstrip().split(';')
        add_toque(args, lst)



"""
Checar no sistema qual o dia da semana e setar todos os toques definidos no dia pra ativo e os
de outros dias para inativo
Dia da semana é representado por um int: Domingo=0, Segunda=1, Terça=2...
"""
def update_weekday(lst):
    for toque in lst:
        if toque.week_day.contains(str(datetime.datetime.now().isoweekday())):
            toque.is_active = True
        else:
            toque.is_active = False


def main():
    csvfile = 'toque.csv'
    while True: '''Pra sempre'''
        list_toques = []
        read_data_csv(csvfile, list_toques)

        update_weekday(list_toques)

        curr_hour = str(datetime.datetime.now().time())

        list_toques.sort(key=operator.attrgetter('time'))
        update_weekday(list_toques)

        for i in range(len(list_toques)): #Checar cada toque
            if list_toques[i].is_active and curr_hour < list_toques[i].time: #Se estiver ativo e ainda não deu a hora
                print("Próximo toque será às " + list_toques[i].time)
                while True:
                    curr_hour = str(datetime.datetime.now().time()) #Ficar atualizando horario
                    if curr_hour > list_toques[i].time: # Quando der a hora
                        data, fs = sf.read(list_toques[i].sound_name, dtype='float32') #Converter .WAV para NumPy Array
                        if list_toques[i].channel == '0':
                            sd.play(data, fs, device=3) #Tocar som no dispositivo 3 (Fone de Ouvido USB)
                            status = sd.wait()  # Esperar som terminar
                        elif list_toques[i].channel == '1':
                            sd.play(data, fs, device=4) #Tocar som no dispositivo 4 (Alto-falantes)
                            status = sd.wait()  # Esperar som terminar
                        list_toques[i].is_active = False
                        break # Sair do Loop
            else:
                list_toques[i].is_active = False

        while curr_hour < '01:00' and curr_hour > '03:00' : # Enquanto não estiver entre 1 e 3 da manhã
            time.sleep(1800) # Esperar 30 minutos
            curr_hour = str(datetime.datetime.now().time()) # Atualizar hora


if __name__ == '__main__':
    main()
