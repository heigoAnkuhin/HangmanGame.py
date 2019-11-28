import os
import subprocess
import sys, csv, random, codecs
import traceback
from urllib.request import urlopen as uopen
from typing import List
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

pakkumisArv = 0
maksimumPakkumisArv = 10

def joonistus() :
    global pakkumisArv
    if pakkumisArv == 1 :
        board.create_line(5, 250, 75, 250, width=4)
        board.create_line(30, 40, 30, 250, width=4)
    elif pakkumisArv == 2 :
        board.create_line(30, 40, 150, 40, width=4)
        board.create_line(30, 70, 60, 40, width=4)
    elif pakkumisArv == 3 :
        board.create_line(150, 40, 150, 70, width=4)
    elif pakkumisArv == 4 :
        board.create_oval(130,70,  170,110, width=3)
    elif pakkumisArv == 5:
        board.create_line(150, 110, 150, 180, width=3)
    elif pakkumisArv == 6:
        board.create_line(150, 120, 135, 165, width=3)
    elif pakkumisArv == 7:
        board.create_line(150, 120, 165, 165, width=3)
    elif pakkumisArv == 8:
        board.create_line(150, 180, 130, 220, width=3)
    elif pakkumisArv == 9:
        board.create_line(150, 180, 165, 215, width=3)
    elif pakkumisArv == 10:
        board.create_oval(139,82,  147,90, width=3, fill="red")
        board.create_oval(153,82,  161,90, width=3, fill="red")
        board.create_oval(140,95,  159,105, width=3, fill="red")
        messagebox.showinfo(message='Said surma :/ Õige sõna oli "' + str(sisendSona) + '".')
        root.update()
    return

def restart() :
    command = '"{}" "{}" "{}"'.format(
        sys.executable,
        __file__,
        os.path.basename(__file__),
    )
    try :
        subprocess.Popen(command)
    except Exception :
        traceback.print_exc()
        sys.exit('fatal error occurred rerunning script')
    else :
        quit()


def vordlus() :
    global pakkumisArv
    global maksimumPakkumisArv
    while pakkumisArv < maksimumPakkumisArv :
        while "_" in sisendSonaKuva :           
            pakkumine = tahePakkumine.get().lower()
            if (pakkumine not in taheKontroll) or (pakkumine == "") :
                messagebox.showinfo(message="Pakutud sümbol ei ole täht. Proovi uuesti..")
            elif pakkumine in kasutatudTahed :
                pakkumisArv += 1
                messagebox.showinfo(message="Sa oled seda tähte juba pakkunud..")
            else :
                kasutatudTahed.append(pakkumine)
                if pakkumine in sisendSona :
                    for i in range(0, sisendSonaPikkus) :
                        if sisendSona[i] == pakkumine :
                            sisendSonaKuva[i] = pakkumine
                            sisendSonaKuvaFunktsioon(sisendSonaKuva)
                    messagebox.showinfo(message="Tubli! Arvasid õigesti.")
                    if "_" not in sisendSonaKuva :
                        messagebox.showinfo(message="Sa oled võitnud! Valesti pakkusid " + str(pakkumisArv) + " korda.")
                else :
                    pakkumisArv += 1
                    messagebox.showinfo(message="Pakutud tähte sõnas ei eksisteeri. Proovi uuesti!")
            joonistus()
            root.update()
            return
        else :
            messagebox.showinfo(message="Sa oled võitnud! Valesti pakkusid " + str(pakkumisArv) + " korda.")
            joonistus()
            root.update()
            return
    else :
        messagebox.showinfo(message='Said surma :/ Õige sõna oli "' + str(sisendSona) + '".')
        root.update()
        return

def kontrolli(*args) :
    try :
        vordlus()
    except ValueError :
        pass

root = Tk()
root.title("Hangman")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E ,S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
tahePakkumine = StringVar()
kuvaSona = StringVar()

tahePakkumine_entry = ttk.Entry(mainframe, width=7, textvariable=tahePakkumine)
tahePakkumine_entry.grid(column=4, row=2, sticky=(W, E))
ttk.Label(mainframe, textvariable=kuvaSona).grid(column=4, row=1, sticky=(W, E))
ttk.Label(mainframe, text="Sõna: ").grid(column=3, row=1, sticky=W)
ttk.Button(mainframe, text="Kontrolli", command=kontrolli).grid(column=3, row=3, sticky=W)
ttk.Button(mainframe, text="Alusta uuesti", command=restart).grid(column=3, row=5, sticky=W)
ttk.Label(mainframe, text="Paku täht").grid(column=3, row=2, sticky=W)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
tahePakkumine_entry.focus()
root.bind('<Return>', kontrolli)

board = Canvas(root, width=600, height=600, background="White")
board.grid()

kasutatudTahed = []
sisendSonaKuva = []
taheKontroll = "abcdefghijklmnopqrstuvwxyzöäüõ"

# Funktsioon, et korrektselt kuvada tühjad lüngad
def sisendSonaKuvaFunktsioon(letters: List) -> None:
    kuvaSona.set("{0}".format(" ".join(letters)))

with uopen('https://ankuhin.ee/wp-content/wordlist.txt') as csvfail:
    csvLugeja = csv.reader(codecs.iterdecode(csvfail, 'utf-8'))
    sonaList = list(csvLugeja)
    suvalineSona = random.choice(sonaList)
    for sona in suvalineSona:
        sisendSona = sona.lower()
# Võtan sõna pikkuse
sisendSonaPikkus = len(sisendSona)
# kuvan sõna lünkadena
for character in sisendSona :
    sisendSonaKuva.append("_")
sisendSonaKuvaFunktsioon(sisendSonaKuva)
root.mainloop()         