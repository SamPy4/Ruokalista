import PyPDF2, sivu_class
from tkinter import *
from datetime import datetime

# TODO: Ikkuna levittää itsentä niin että teksti pomppaa pois näkyvistä
# TODO: Sisältää tyhmän "maanantai" = 0 = maanantai käännöksen
# TODO: Päivät joiden mukaan viikot on märätty ovat kovakoodattu, voisi tehdä sen pdf:n käsittelyssä

class main():
    def __init__(self):
        self.version = "5.5.7"

        self.ikkuna = Tk()
        self.ikkuna.title("Kouluruoka - Syksy")

        self.text = Label(self.ikkuna, text="")

        self.ruokaListaORG = open("ruokalista_2017_syksy.pdf", "rb")
        self.reader  = PyPDF2.PdfFileReader(self.ruokaListaORG)
        self.pituus  = self.reader.numPages

        self.paivatStr = ["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "maanantai", "maanantai"]

        self.currDay    = datetime.now().day
        self.currMonth  = datetime.now().month
        self.currWeek   = 0
        self.currDaySTR = self.paivatStr[datetime.now().weekday()]

        self.etsittava = StringVar()

        if self.currDay in range(7, 12) and self.currMonth == 8:
            self.currWeek = 1
        elif self.currDay in range(12, 19) and self.currMonth == 8:
            self.currWeek = 2
        elif self.currDay in range(19, 26) and self.currMonth == 8:
            self.currWeek = 3
        elif self.currDay == 26 and self.currMonth == 8:
            self.currWeek = 5
        elif self.currDay in range(27, 32) and self.currMonth == 8 or self.currDay == 1 and self.currMonth == 9:
            self.currWeek = 5
        elif self.currDay in range(2,9) and self.currMonth == 9:
            self.currWeek = 6
        elif self.currDay in range(9,16) and self.currMonth == 9:
            self.currWeek = 7
        #print(self.currWeek)
        #print(self.currDay, self.currMonth)

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
        TopText.grid(column=0, row=0)

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

        etsinta = Entry(self.ikkuna, textvariable=self.etsittava)
        etsinta.grid(column=0, row=5)

        for i in range(7):
            # Töytetään lista "syksy" sivu-objekteilla vain kerran ohjelman
            # ajon aikana
            syksy.append(sivu_class.sivu(i))

        paivatList = syksy[int(valittuViikko.get())].getPaivatList()

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

        def kirjoitaTanaan():
            valittuPaiva.set(self.currDaySTR)
            valittuViikko.set(self.currWeek)

            kirjoita(self.text)

        def kirjoitaHuomenna():
            paivanro = datetime.now().weekday()

            if paivanro == 4:
                valittuPaiva.set(self.paivatStr[0])
                valittuViikko.set(self.currWeek+1)
            elif paivanro > 4:
                valittuPaiva.set(self.paivatStr[1])
                valittuViikko.set(self.currWeek)
            elif paivanro < 4:
                valittuPaiva.set(self.paivatStr[paivanro+1])
                valittuViikko.set(self.currWeek)

            kirjoita(self.text)

        def kirjoitaEilen():
            paivanro = datetime.now().weekday()

            if paivanro == 0 or paivanro > 4:
                valittuPaiva.set(self.paivatStr[4])
                valittuViikko.set(self.currWeek-1)
            elif paivanro < 5:
                valittuPaiva.set(self.paivatStr[paivanro-1])
                valittuViikko.set(self.currWeek)

            kirjoita(self.text)

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

            tuloksetStr = Label(popup, text=string)
            tuloksetStr.pack()

            yhteensa = Label(popup, text=yht)
            yhteensa.pack()
            return

        kirjoita(self.text) #Tulostaa ohjeman avautuessa päivän ruoan

        # Tulostaa tämän päivän tuoan välittämättä siitä, missä käyttäjä on
        tanaanNappi = Button(self.ikkuna, text="Tänään", command=kirjoitaTanaan)
        tanaanNappi.grid(column=2,row=3)

        eilenNappi = Button(self.ikkuna, text="Eilen", command=kirjoitaEilen)
        eilenNappi.grid(column=3,row=3)

        huomennaNappi = Button(self.ikkuna, text="Huomenna", command=kirjoitaHuomenna)
        huomennaNappi.grid(column=4, row=3)

        paivita = Button(text="Päivitä", command=lambda: kirjoita(self.text))
        paivita.grid(column=1, row=3)

        etsiNappi = Button(self.ikkuna, text="Etsi", command=etsi)
        etsiNappi.grid(column=1,row=5)

        mainloop()

if __name__ == "__main__":
    main = main()
    main.run()
