import PyPDF2, fetch_pdf

""" This module parses the vantti pdf file """
# NOTE: ROW 78

class sivu():
    def __init__(self, sivuIndex):
        self.ruokaListaORG = open("ruokalista.pdf", "rb")
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


    def getSivunPaivat(self):
        ind = 0
        string = ""
        text = self.sivunSisalto

        for i in range(53):
            finding = "VK {}".format(str(i))
            try:
                ind = text.index(finding)
                vko = str(i)
            except:
                pass

        """ 3 saattaa aiheuttaa parsimisongelmia """
        startInd = ind + len(vko) + 3
        lastInd = text.index("LOUNAS")

        for i in range(startInd, lastInd):
            if not text[i] == "\n" or text[i] == " ":
                string += text[i]

        string = string.strip()

        if string[-1] != "." and string[-1] != " ":
            string += "."

        exist = True
        try:
            negsubind = string.index("-") - 1
            possubind = string.index("-") + 1
        except ValueError:
            exist = False

        if exist:
            if string[negsubind] == ".":
                string = string.replace("-","")
            if string[possubind] == ".":
                string = string.replace("-","")
            else:
                string = string.replace("-",".")

        string = string.split(".")
        string.append(self.sivuIndex+1)

        try:
            string[5]
            string.append(True)
        except IndexError:
            string.append(False)

        if not exist:
            del(string[-1])
            string.append(None)
            for i in range(2):
                string[i] = int(string[i])

        if not string[-1] == None:
            if string[-1]:
                for i in range(4):
                    string[i] = int(string[i])
            else:
                for i in range(3):
                    string[i] = int(string[i])

        return string

class PDFFetcher():
    def fetch():
        fetch_pdf.fetch()
        return

if __name__ == "__main__":
    for i in range(7):
        test = sivu(i)
        text = test.getSivunPaivat()
        print("Main:", text)
