import PyPDF2, sivu_class
from tkinter import *
from datetime import datetime

# TODO: Ikkuna levittää itsensä niin että teksti pomppaa pois näkyvistä
# TODO: Sisältää tyhmän "maanantai" = 0 = maanantai käännöksen
# TODO: Päivät joiden mukaan viikot on märätty ovat kovakoodattu, voisi tehdä sen pdf:n käsittelyssä

class main():
    def __init__(self):
        self.version = "5.8.9"

        self.ikkuna = Tk()
        self.ikkuna.title("Kouluruoka - Syksy")

        self.text = Label(self.ikkuna, text="")

        self.ruokaListaORG = open("ruokalista_2017_syksy_2.pdf", "rb")
        self.reader  = PyPDF2.PdfFileReader(self.ruokaListaORG)
        self.pituus  = self.reader.numPages

        self.paivatStr = ["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "maanantai", "maanantai"]

        self.currDay    = datetime.now().day
        self.currMonth  = datetime.now().month
        self.currWeek   = 0
        self.currDaySTR = self.paivatStr[datetime.now().weekday()]
        self.currDayINT = datetime.now().weekday()
        self.showedDay  = self.currDayINT
        self.showedWeek = 0

        self.etsittava = StringVar()





        given_day = 23
        given_mon = 10

        acc_days  = []
        start     = given_day
        end       = given_day+7

        for i in range(self.pituus):
            if start >= 30:
                print(start)
                given_mon += 1
                start = 1
                end   = 8

            acc_days.append([range(start, end), given_mon, i+1])
            start = start + 1
            end   = end   + 1

        for i in acc_days:
            print(i[0], i[1])

        for i in acc_days:
            if self.currDay in i[0] and self.currMonth == i[1]:
                self.currWeek = i[2]

        print(self.currWeek)




        if self.currDay in range(11, 16) and self.currMonth == 9:
            self.currWeek = 1
        elif self.currDay in range(16, 23) and self.currMonth == 9:
            self.currWeek = 2
        elif self.currDay in range(23, 30) and self.currMonth == 9:
            self.currWeek = 3
        elif self.currDay in range(2, 7) and self.currMonth == 10:
            self.currWeek = 4
        elif self.currDay in range(7, 14) and self.currMonth == 10:
            self.currWeek = 5
        elif self.currDay in range(14, 21) and self.currMonth == 10:
            self.currWeek = 6
        #print(self.currWeek)
        #print(self.currDay, self.currMonth)

        self.paivaStr = ["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai"]

    def run(self):
        paiva = {"maanantai"   : 0,
                 "tiistai"     : 1,
                 "keskiviikko" : 2,
                 "torstai"     : 3,
                 "perjantai"   : 4 }

        viikko = range(1,self.pituus+1)

        sivu = 2

        syksy = []


        valittuViikko = StringVar(self.ikkuna)
        valittuViikko.set(self.currWeek)

        valittuPaiva = StringVar(self.ikkuna)
        valittuPaiva.set(self.currDaySTR)

        """ INITIALIZING LABELS """

        TopText = Label(self.ikkuna, text="v. %s" % self.version)
        TopText.grid(column=1, row=0)

        currViikkoText = Label(self.ikkuna, text="Nyt on viikko %i" % self.currWeek)
        currViikkoText.grid(column=2, row=1)

        currPaivaText = Label(self.ikkuna, text="Tänään on %s" % self.currDaySTR)
        currPaivaText.grid(column=2, row=2)

        viikkoText = Label(self.ikkuna, text="Viikko:")
        viikkoText.grid(column=0, row=1)

        paivaText = Label(self.ikkuna, text="Päivä:")
        paivaText.grid(column=0, row=2)

        """INITIALIZING OPTION MENUS"""
        viikkoValikko = OptionMenu(self.ikkuna, valittuViikko, *viikko)
        viikkoValikko.grid(column=1, row=1)

        paivaValikko = OptionMenu(self.ikkuna, valittuPaiva, *paiva)
        paivaValikko.grid(column=1, row=2)

        """INITIALIZING SEARCH ENTRY"""

        etsinta = Entry(self.ikkuna, textvariable=self.etsittava, takefocus=True)
        etsinta.bind("<Enter>")
        etsinta.grid(column=0, row=5)

        for i in range(7):
            # Töytetään lista "syksy" sivu-objekteilla vain kerran ohjelman
            # ajon aikana
            syksy.append(sivu_class.sivu(i))

        #paivatList = syksy[int(valittuViikko.get())-1].getPaivatList() TURHA?

        #paivanRuokaStr = paivatList[paiva[valittuPaiva.get()]]

        # paivanRuoka = Label(self.ikkuna, text=paivanRuokaStr)
        # text = paivanRuoka
        # paivanRuoka.pack()

        def kirjoita(label):
            """ Overwrites the existing text and replaces it"""
            label.destroy()

            # 0-4 maanantai = 0 perjantai = 4
            paivatList = syksy[int(valittuViikko.get())-1].getPaivatList()

            paivanRuokaStr = paivatList[paiva[valittuPaiva.get()]]
            paivanRuoka = Label(self.ikkuna, text=paivanRuokaStr)
            paivanRuoka.grid(column=2, row=4)

            self.text = paivanRuoka

            #print("Kirjoitettu päivä", self.showedDay)
            #print("Kiroitettu viikko", self.showedWeek)
            #print()

        def kirjoitaTanaan():
            valittuPaiva.set(self.currDaySTR)
            valittuViikko.set(self.currWeek)

            self.showedDay  = datetime.now().weekday()
            self.showedWeek = self.currWeek
            if datetime.now().weekday() > 4:
                    self.showedDay  = 0

            kirjoita(self.text)

        def kirjoitaHuomenna():
            paivanro = datetime.now().weekday()

            if paivanro == 4:
                valittuPaiva.set(self.paivatStr[0])
                valittuViikko.set(self.currWeek+1)

                self.showedWeek = self.currWeek+1
                self.showedDay  = 0

            elif paivanro > 4:
                valittuPaiva.set(self.paivatStr[1])
                valittuViikko.set(self.currWeek)

                self.showedWeek = self.currWeek
                self.showedDay = 1

            elif paivanro < 4:
                valittuPaiva.set(self.paivatStr[paivanro+1])
                valittuViikko.set(self.currWeek)

                self.showedWeek = self.currWeek
                self.showedDay  = paivanro+1


            kirjoita(self.text)

        def kirjoitaEilen():
            paivanro = datetime.now().weekday()

            if paivanro == 0 or paivanro > 4:
                valittuPaiva.set(self.paivatStr[4])
                valittuViikko.set(self.currWeek-1)

                self.showedWeek = self.currWeek-1
                self.showedDay = 4

            elif paivanro < 5:
                valittuPaiva.set(self.paivatStr[paivanro-1])
                valittuViikko.set(self.currWeek)

                self.showedWeek = self.currWeek
                self.showedDay = paivanro - 1

            kirjoita(self.text)

        def kirjoitaSeur():
            paivanro  = self.showedDay
            viikkonro = self.showedWeek

            #print("paivanro", paivanro)
            #print("viikkonro", viikkonro)

            if paivanro is not 4:
                valittuPaiva.set(self.paivaStr[paivanro+1])
                valittuViikko.set(viikkonro)

                self.showedWeek = viikkonro
                self.showedDay  = paivanro + 1

            if paivanro == 4:
                valittuPaiva.set(self.paivaStr[0])
                valittuViikko.set(viikkonro + 1)

                self.showedDay  = 0
                #print("Lisätään viikko", viikkonro)
                self.showedWeek += 1

            #print("Enne kirjoitusta päivä on: %i" % self.showedDay)
            #print("Enne kirjoitusta viikko on: %i" % self.showedWeek)

            kirjoita(self.text)
            return

        def kirjoitaEdel():
            paivanro  = self.showedDay
            viikkonro = self.showedWeek

            #print("paivanro", paivanro)
            #print("viikkonro", viikkonro)

            if paivanro > 0 and paivanro <= 4:
                #print(len(self.paivaStr))
                #print("problem?", paivanro)
                valittuPaiva.set(self.paivaStr[paivanro-1])
                valittuViikko.set(viikkonro)

                self.showedWeek = viikkonro
                self.showedDay  = paivanro - 1

            if paivanro == 0 or paivanro > 4:
                valittuPaiva.set(self.paivaStr[4])
                valittuViikko.set(viikkonro - 1)

                self.showedDay  = 4
                self.showedWeek -= 1

            #print("Enne kirjoitusta päivä on: %i" % self.showedDay)
            #print("Enne kirjoitusta viikko on: %i" % self.showedWeek)

            kirjoita(self.text)
            return
        def ohje():
            string = """Sami Porio 2017 VANTTI-ruokalista \n v. {} \n
Pikanäppäimet:\n
välilyönti : tämä päivä\n
ylä nuoli : huominen\n
ala nuoli : eilinen\n
oikea nuoli : seuraava päivä\n
vasen nuoli : edellinen päivä\n
enter : etsi\n
esc : sulje
             """.format(self.version)

            ohjePopup = Toplevel()
            ohjePopup.title("Ohje")

            def poistu(event):
                ohjePopup.destroy()

            ohjePopup.bind("<Escape>", poistu)

            ohjeteksti = Label(ohjePopup, text=string)
            ohjeteksti.grid(column=0, row=0)
        def etsi():
            """ Etsitään kaikista mahdollisista päivistä, sisältääkö merkkijono etsittävän"""
            tulokset = []
            string = ""
            for paiva in syksy:
                tulokset.append(paiva.etsinta(self.etsittava.get()))

            yht = 0
            for tulos in tulokset:
                for paiva in tulos:
                    viikkonro = paiva[0] + 1
                    if paiva[1] == "-M":
                        string += "viikko %i päivä: MA\n" % viikkonro

                    else:
                        string += "viikko %i" % viikkonro + " päivä: %s\n" % paiva[1]

                    yht += 1

            yht = "Tuloksia: %i" % yht

            # Luodaan popup, jossa näkyy hakutulokset annetulle haulle
            popup = Toplevel()
            popup.title("Hakutulokset")

            def poistu(event):
                popup.destroy()

            popup.bind("<Escape>", poistu)

            tuloksetStr = Label(popup, text=string)
            tuloksetStr.pack()

            yhteensa = Label(popup, text=yht)
            yhteensa.pack()
            return

        kirjoita(self.text) #Tulostaa ohjeman avautuessa päivän ruoan

        def painettu(event):
            """ Ottaa painetun napin ja tekee sillä jotain """
            nappi = event.keysym
            #print(nappi)

            if nappi == "Left":
                kirjoitaEdel()
            if nappi == "Right":
                kirjoitaSeur()
            if nappi == "space":
                kirjoitaTanaan()
            if nappi == "Up":
                kirjoitaHuomenna()
            if nappi == "Down":
                kirjoitaEilen()
            if nappi == "Return":
                etsi()
            #if nappi == "h" or nappi == "o":
                #ohje()
            if nappi == "Escape":
                exit()
            return

        self.ikkuna.bind("<Key>", painettu)

        # Tulostaa tämän päivän ruoan välittämättä siitä, missä käyttäjä on
        kirjoitaTanaan() # Kirjoittaa päivän ruoan ohjelman alkaessa ja päivittää samalla self.showed- arvot
        tanaanNappi = Button(self.ikkuna, text="Tänään", command=ohje)
        tanaanNappi.grid(column=2,row=3)

        eilenNappi = Button(self.ikkuna, text="Eilen", command=kirjoitaEilen)
        eilenNappi.grid(column=3,row=3)

        huomennaNappi = Button(self.ikkuna, text="Huomenna", command=kirjoitaHuomenna)
        huomennaNappi.grid(column=4, row=3)

        paivita = Button(text="Päivitä", command=lambda: kirjoita(self.text))
        paivita.grid(column=1, row=3)

        etsiNappi = Button(self.ikkuna, text="Etsi", command=etsi)
        etsiNappi.grid(column=1,row=5)

        seurNappi = Button(self.ikkuna, text="Seuraava", command=kirjoitaSeur)
        seurNappi.grid(column=4, row=5)

        edelNappi = Button(self.ikkuna, text="Edellinen", command=kirjoitaEdel)
        edelNappi.grid(column=3, row=5)

        ohjeNappi = Button(self.ikkuna, text="Ohje", command=ohje)
        ohjeNappi.grid(column=0, row=0)

        mainloop()

if __name__ == "__main__":
    main = main()
    main.run()
