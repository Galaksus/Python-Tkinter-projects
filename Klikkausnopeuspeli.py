"""Yhden pelaajan klikkailupeli. Tehtävänäsi on klikata mustia painikkeita niin nopeasti kuin pystyt aikaa sinulla on
15 sekuntia. Jokaisesta onnistuneesta klikkauksesta lasketaan sinulle piste. Peli loppuu kun aika loppuu tai,
jos klikkaat vaaleaa painiketta mustan sijaan. Kenttä koostuu 16 buttonista joista yksi on aina mustan värinen.
Mustaa buttonia klikattaessa arpoo se uuden sijainnin mustan väriselle buttonille (se voi olla myös sama kuin
edellisellä klikkauksella). Kentän voi aloittaa alusta Restart-painikkeella. Ensimmäisellä
käynnistyskerralla painike on 'Start' niminen. Oikeassa yläreunassa on myös info-painike, joka suurentaa kentän
y-suuntaista geometriaa tuoden infotekstin näkyviin.
Tekijä: Konsta Lallo 25.09.2022 """
from tkinter import *
from functools import partial
import random
import time
import threading


class GUI:
    def __init__(self):
        # korkein pistemäärä
        self.__highestscore = 0

        # tkitnerin alkuasetukset
        self.__mainwindow = Tk()
        self.__mainwindow.title("Klikkailupeli")
        self.__geometry = "908x763"
        self.__mainwindow.geometry(self.__geometry)

        # Buttoni josta peli käynnistetään uudestaan, se tarkoittaa myös sitä että kenttä täytyy sekoittaa
        time.sleep(2)
        self.__startButton = Button(self.__mainwindow, text="Start game", relief="solid", borderwidth=3, height=3,
                                    width=30,
                                    command=self.startGame)
        self.__startButton.configure(bg="#5C8DB5")
        self.__startButton.place(x=350, y=10)

        # Buttoni ohjeille
        self.__info_button = Button(self.__mainwindow, text="Info", relief="solid", borderwidth=3, height=3,
                                    width=15, command=self.info)
        self.__info_button.configure(bg="#9FE2BF")
        self.__info_button.place(x=750, y=10)
        # Infoteksti label
        self.__info_text = Label(self.__mainwindow, background="grey",
                                 text="Kyseessä on yhdenpelaajan klikkailupeli, tehtävänäsi on klikata mustia "
                                      "painikkeita mahdollisimman nopeasti, aikaa sinulla on 15 s",
                                 relief=RAISED)
        # Labelit väärille arvauksille, ajalle ja maksimipisteille
        self.__stringVar_correct_clicks = StringVar()
        self.__stringVar_correct_clicks.set('Oikeita klikkauksia: ')
        self.__result_text = Label(self.__mainwindow, textvariable=self.__stringVar_correct_clicks, relief=RAISED)
        self.__result_text.place(x=10, y=30)
        #
        self.__stringVar_time_left = StringVar()
        self.__stringVar_time_left.set('Aikaa jäljellä: ')
        self.__result_text_2 = Label(self.__mainwindow, textvariable=self.__stringVar_time_left, relief=RAISED)
        self.__result_text_2.place(x=10, y=5)
        #
        self.__intVar_best = IntVar()
        self.__stringVar_best = StringVar()
        self.__stringVar_best.set('Paras suorituksesi: ')
        self.__result_text_3 = Label(self.__mainwindow, textvariable=self.__stringVar_best, relief=RAISED)
        self.__result_text_3.place(x=10, y=55)

    def checkButtonColor(self, buttonIndex):
        """
        Tarkistaa onko painike väriltään musta, jos pelaaja saa pisteen, jos ei ole pelaaja häviää pelin
        :param buttonIndex: # painikkeen indeksinumero
        :return:
        """
        if self.__button_list[buttonIndex].cget('bg') == 'black':
            self.__button_list[buttonIndex].configure(bg='#D3D3D3')
            self.__correct_clicks_counter += 1
            self.__stringVar_correct_clicks.set('Oikeita klikkauksia: ' + str(self.__correct_clicks_counter))
            self.randomNumberGenerator()
        else:
            for x in range(len(self.__button_list)):
                self.__button_list[x]["state"] = "disabled"
            self.__button_list[buttonIndex].configure(bg='RED', fg='black', text="Game over!")
            self.terminateThread()
            # print("Hävisit pelin")
        pass

    def highestScore(self, currentscore):
        """
     Määritetään paras pelaajan paras tulos
     :param currentscore: Viimeisen kierroksen tulos
     :return:
     """
        if currentscore > self.__highestscore:
            self.__highestscore = currentscore
            self.__stringVar_best.set('Paras suorituksesi: ' + str(currentscore))
        else:
            return

    def randomNumberGenerator(self):
        """
        Asettaa randomilla yhden buttonin mustan väriseksi
        :return:
        """
        self.__button_list[random.randrange(12)].configure(bg='black')

    def info(self):
        """
        Tämä funktio muuttaa kentän geometriaa, jolloin infoteksti saadaan näkyviin.
        :return:
        """
        self.__info_text.place(x=100, y=768)
        if self.__geometry == "908x763":
            self.__geometry = "908x790"
            self.__mainwindow.geometry(self.__geometry)
        else:
            self.__geometry = "908x763"
            self.__mainwindow.geometry(self.__geometry)

    def startGame(self):
        """
        Käynnistää pelin, luomalla buttonit kentälle
        :return:
        """
        # Threadin tila
        self.__thread_running = False

        self.__correct_clicks_counter = 0
        self.__button_locations = [[8, 80], [308, 80], [608, 80],
                                   [8, 250], [308, 250], [608, 250],
                                   [8, 420], [308, 420], [608, 420],
                                   [8, 590], [308, 590], [608, 590]]

        self.__button_list = []
        self.__button_click_counter_list = [False] * len(self.__button_locations)

        random.shuffle(self.__button_locations)
        self.__startButton["text"] = "Restart game"

        # Tehdään buttonit
        for i, xy in enumerate(self.__button_locations):
            buttons = Button(self.__mainwindow, text="??", borderwidth=3, relief="ridge", height=10, width=40,
                             command=partial(self.checkButtonColor, i))
            buttons.configure(bg='#D3D3D3')
            buttons.place(x=xy[0], y=xy[1])

            self.__button_list.append(buttons)
        self.randomNumberGenerator()

        self.__thread_running = True
        t = threading.Thread(target=self.gameTimer, args=(15,), daemon=True)
        t.start()

    def terminateThread(self):
        """
        Pysäyttää threadin kirjoittamalla muuttujan Falseksi
        :return:
        """
        self.__thread_running = False

    def gameTimer(self, seconds):
        """
        Palauttaa kaksi buttonia takaisin default väriinsä tietyn sekuntimäärän jälkeen
        :param seconds: sekuntimäärä
        :return:
        """

        # Peli alkaa viedään yläpalkin buttonit poist tieltä
        self.__startButton.place(x=2000, y=10)
        self.__info_button.place(x=2000, y=10)
        while self.__thread_running and seconds > 0:
            self.__stringVar_time_left.set('Aikaa jäljellä: ' + str(seconds) + ' s')
            seconds = seconds - 1
            # print("Elapsed: ", seconds)
            time.sleep(1)
        # Kertaalleen määritetään tässä, niin timeri ei jämähdä yhteen sekuntiin (1)
        self.__stringVar_time_left.set('Aikaa jäljellä: ' + str(seconds) + ' s')

        # Peli loppuu tuodaan yläpalkin buttonit taas näkyviin
        self.__startButton.place(x=350, y=10)
        self.__info_button.place(x=750, y=10)

        self.highestScore(self.__correct_clicks_counter)
        # print("Game over")
        for x in range(len(self.__button_locations)):
            self.__button_list[x]["state"] = "disabled"

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
