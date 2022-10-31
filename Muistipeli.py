"""Yhden pelaajan muistipeli. Tehtävänäsi on selvittää kenttä läpi yhdistelemällä pareja samoista väreistä.
Kenttä koostuu 16 buttonista, jotka vaihtavat väriä painettaessa. Jos arvaat väärin pareja, laskee se jokaisen väärän
vastauksen laskuriin ylös.
Väärästä arvauksesta painikkeet vaihtavat värinsä takaisin defaulttiin ('#D3D3D3') 1.25 sekunnin kuluttua.
Kentän voi sekoittaa ja uudelleen käynnistää Restart-painikkeella.
Ensimmäisellä käynnistyskerralla painike on 'Start' niminen.
Oikeassa yläreunassa on myös info-painike, joka suurentaa kentän y-suuntaista geometriaa tuoden infotekstin näkyviin.
Tekijä: Konsta Lallo 25.09.2022 """
from tkinter import *
from functools import partial
import random
import time
import threading


class GUI:
    def __init__(self):
        self.__mainwindow = Tk()
        self.__mainwindow.title("Yhden pelaajan muistipeli")
        self.__geometry = "908x763"
        self.__mainwindow.geometry(self.__geometry)

        # Buttoni josta peli käynnistetään uudestaan, se tarkoittaa myös sitä että kenttä täytyy sekoittaa
        self.__shuffleButton = Button(self.__mainwindow, text="Start game", relief="solid", borderwidth=3, height=3,
                                      width=30,
                                      command=self.shuffleBoard)
        self.__shuffleButton.configure(bg="#5C8DB5")
        self.__shuffleButton.place(x=350, y=10)

        # Buttoni ohjeille
        self.__info_button = Button(self.__mainwindow, text="Info", relief="solid", borderwidth=3, height=3,
                                    width=15, command=self.info)
        self.__info_button.configure(bg="#9FE2BF")
        self.__info_button.place(x=750, y=10)
        # Infoteksti label
        self.__info_text = Label(self.__mainwindow, background="grey", text="Kyseessä on yhdenpelaajan muistipeli, selvitä kenttä läpi yhdistelemällä pareja samoista väreistä", relief=RAISED)
        # Labelit väärilel arvauksille
        self.__result_text = Label(self.__mainwindow, text="Vääriä arvauksia: ", relief=RAISED)
        self.__result_text.place(x=100, y=30)
        self.__intVar_counted_misses = IntVar()
        self.__result_text_2 = Label(self.__mainwindow, textvariable=self.__intVar_counted_misses, relief=RAISED)
        self.__result_text_2.place(x=200, y=30)

    def changeButtonColor(self, buttonIndex, color):
        """
        Muuttaa buttonin väriä sekä disabloi painetun buttonin että sitä ei voi rämpyttää
        :param buttonIndex: For loopilla ja listaan appendattujen buttonien indeksinumero
        :param color: kyseisen buttonin väri
        :return:
        """
        self.__button_click_counter_list[buttonIndex] = True

        # Väri ja disable napille
        self.__button_list[buttonIndex].configure(bg=color)
        if self.__button_list[buttonIndex]["state"] == "normal":
            self.__button_list[buttonIndex]["state"] = "disabled"

        for n, trues in enumerate(self.__button_click_counter_list):
            if n != buttonIndex:
                if trues:
                    if self.__button_list[n].cget('bg') == color:
                        self.destroyButton([n, buttonIndex])
                        self.__button_click_counter_list = [False] * len(self.__button_locations)
                        for x in range(len(self.__button_locations)):
                            self.__button_list[x].configure(bg='#D3D3D3')
                            self.__button_list[x]["state"] = "normal"
                    else:
                        self.__button_click_counter_list = [False] * len(self.__button_locations)
                        self.__miss_counter += 1
                        self.__intVar_counted_misses.set(self.__miss_counter)
                        for x in range(len(self.__button_locations)):
                            self.__button_list[x]["state"] = "disabled"
                        threading.Thread(target=self.TimerForButtonColorToReturnDefault, args=(1.25,)).start()

    def TimerForButtonColorToReturnDefault(self, seconds):
        """
        Palauttaa kaksi buttonia takaisin default väriinsä tietyn sekuntimäärän jälkeen
        :param seconds: sekuntimäärä
        :return:
        """
        time.sleep(seconds)
        for x in range(len(self.__button_locations)):
            self.__button_list[x].configure(bg='#D3D3D3')
            self.__button_list[x]["state"] = "normal"

    def destroyButton(self, index_for_buttons):
        """
        Hävittää GUI:sta kaksi buttonia
        :param index_for_buttons: Tässä kahden buttonin listan indeksinumero, jotta ne osataan .dertroy():ata oikeat
        :return:
        """

        for index in index_for_buttons:
            # self.__button_list[index].destroy()
            self.__button_list[index].place(x=2000, y=2000)

    def info(self):
        """
        Tämä funktio muuttaa kentän geometriaa, jolloin infoteksti saadaan näkyviin.
        :return:
        """
        self.__info_text.place(x=200, y=768)
        if self.__geometry == "908x763":
            self.__geometry = "908x790"
            self.__mainwindow.geometry(self.__geometry)
        else:
            self.__geometry = "908x763"
            self.__mainwindow.geometry(self.__geometry)




    def shuffleBoard(self):
        """
        Sekoittaa buttonien järjestyksen pelikentällä, tämä funktio myös tekee buttonit kentälle
        :return:
        """
        self.__miss_counter = 0
        self.__button_locations = [[8, 80], [308, 80], [608, 80],  # [908, 80],
                                   [8, 250], [308, 250], [608, 250],  # [908, 250],
                                   [8, 420], [308, 420], [608, 420],  # [908, 420],
                                   [8, 590], [308, 590], [608, 590]]  # [908, 590]]

        self.__button_colors = ['#cd853f', '#cd853f', 'blue', 'blue', 'green', 'green', 'yellow', 'yellow', 'red',
                                'red', 'purple', 'purple']


        self.__button_list = []
        self.__button_click_counter_list = [False] * len(self.__button_locations)

        random.shuffle(self.__button_locations)
        random.shuffle(self.__button_colors)

        self.__shuffleButton["text"] = "Restart game"

        # Tehdään buttonit
        for i, xy in enumerate(self.__button_locations):
            buttons = Button(self.__mainwindow, text="??", borderwidth=3, relief="ridge", height=10, width=40,
                             command=partial(self.changeButtonColor, i, self.__button_colors[i]))
            buttons.configure(bg='#D3D3D3')
            buttons.place(x=xy[0], y=xy[1])

            self.__button_list.append(buttons)

    def startGUI(self):
        """
        Starttaa mainloopin
        """
        self.__mainwindow.mainloop()


def main():
    """
    Tehdään classin objecti, sekä kutsuu mainlooppia
    """
    ui = GUI()
    ui.startGUI()


if __name__ == "__main__":
    main()
