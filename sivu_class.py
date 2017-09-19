import PyPDF2
""" This module parses the vantti pdf file """
class sivu():
    def __init__(self, sivuIndex):
        self.ruokaListaORG = open("ruokalista_2017_syksy-loppu.pdf", "rb")
        self.reader  = PyPDF2.PdfFileReader(self.ruokaListaORG)
        self.sivu  =  self.reader.getPage(sivuIndex)

        self.sivuIndex = sivuIndex
        self.sivunSisalto = self.sivu.extractText()


        self.viikko = [
                       "MA",
                       "TI",
                       "KE",
                       "TO",
                       "PE" ]

        self.ruokaLista = self._makeRuokalista()
        self.paivatList = self._makePaivatList()

    def _makeRuokalista(self):
        lista = self.sivunSisalto[self.sivunSisalto.find("MA"):]

        for paiva in self.viikko:
            lista = lista[:lista.find(paiva)]     + "\n---" + lista[lista.find(paiva):]
            lista = lista[:lista.find(paiva) + 3] + "\n" + lista[lista.find(paiva) + 3:]

        return lista

    def getRuokaLista(self):
        return self.ruokaLista

    def getPaivatList(self):
        return self.paivatList

    def _makePaivatList(self):
        paivatSivullaString = self.ruokaLista

        maanantai   = paivatSivullaString[:paivatSivullaString.find("---TI")]
        tiistai     = paivatSivullaString[paivatSivullaString.find("---TI"):paivatSivullaString.find("---KE")]
        keskiviikko = paivatSivullaString[paivatSivullaString.find("---KE"):paivatSivullaString.find("---TO")]
        torstai     = paivatSivullaString[paivatSivullaString.find("---TO"):paivatSivullaString.find("---PE")]
        perjantai   = paivatSivullaString[paivatSivullaString.find("---PE"):]

        self.paivatList = [maanantai, tiistai, keskiviikko, torstai, perjantai]

        return self.paivatList

    def etsinta(self, etsittava):
        tulokset = []
        for paiva in self.paivatList:

            if etsittava in paiva:

                vko = self.sivuIndex
                pv = paiva[3:5]
                tulokset.append((vko, pv))

        return tulokset
