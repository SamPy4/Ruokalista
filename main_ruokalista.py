import PyPDF2, sivu_class
from tkinter import *
from datetime import datetime

# TODO: Ikkuna levittää itsentä niin että teksti pomppaa pois näkyvistä
# TODO: Lista täyttyy loputtomiin line 101
# TODO: Sisältää tyhmän "maanantai" = 0 = maanantai käännöksen
# TODO: Päivät joiden mukaan viikot on märätty ovat kovakoodattu, voidi tehdä sen pdf:n käsittelyssä

class main():
    def __init__(self):
        self.version = "3.5.6"

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

        if self.currDay in range(7, 12) and self.currMonth == 8:
            self.currWeek = 1
        elif self.currDay in range(12, 19) and self.currMonth == 8:
            self.currWeek = 2
        elif self.currDay in range(19, 26) and self.currMonth == 8:
            self.currWeek = 3
        elif self.currDay == 26 and self.currMonth == 8:
            self.currWeek = 4
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

        currPaivaText = Label(self.ikkuna, text="Nyt on %s" % self.currDaySTR)
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

        for i in range(7):
            syksy.append(sivu_class.sivu(i))

        paivatList = syksy[int(valittuViikko.get())].getPaivatList()

        #paivanRuokaStr = paivatList[paiva[valittuPaiva.get()]]

        # paivanRuoka = Label(self.ikkuna, text=paivanRuokaStr)
        # text = paivanRuoka
        # paivanRuoka.pack()


        def kirjoita(label):
            """ Overwrites the existing text and replaces it"""
            label.destroy()


            for i in range(6):
                syksy.append(sivu_class.sivu(i+1)) # Ei koskaan tyhjennetä

            # 0-4 maanantai = 0 perjantai = 4
            paivatList = syksy[int(valittuViikko.get())-1].getPaivatList()

            paivanRuokaStr = paivatList[paiva[valittuPaiva.get()]]
            paivanRuoka = Label(self.ikkuna, text=paivanRuokaStr)
            paivanRuoka.grid(column=1, row=4)

            self.text = paivanRuoka

        kirjoita(self.text) #Tulostaa suoraan avatessa päivän ruoan

        paivita = Button(text="Päivitä", command=lambda: kirjoita(self.text))
        paivita.grid(column=1, row=3)

        mainloop()

main = main()
main.run()
