import requests, os
from lxml import html

def fetch():
    url = open("url.txt", "r+")
    urlcont = url.read()
    pdflink = []
    try:
        page = requests.get('http://www.vantti.fi/ruokalistat/101/0/koulut')
    except requests.exceptions.ConnectionError:
        print("Fetcher couldn't fetch: No internet connection")
        print("PDF might be out-of-date")
        return

    tree = html.fromstring(page.content)
    pdflink = tree.xpath("/html/body/form/div[3]/div/div[2]/div/div[1]/div/div[1]/p[2]/span//a/@href")
    if urlcont != pdflink[0]:
        fetchPDF()
        url.seek(0)
        url.truncate(0)
        url.write(pdflink[0])
        print("PDF fetched and updated")
    else:
        print("PDF is up-to-date")
        return

def fetchPDF():
    try:
        os.system("del ruokalista.pdf")

        page = requests.get('http://www.vantti.fi/ruokalistat/101/0/koulut')
        tree = html.fromstring(page.content)
        pdflink = tree.xpath("/html/body/form/div[3]/div/div[2]/div/div[1]/div/div[1]/p[2]/span//a/@href")

        pdflink = "http://www.vantti.fi/" + pdflink[0]
        links = [pdflink]
        for link in links:
            book_name = "ruokalista.pdf" #link.split('/')[-1]
            with open(book_name, 'wb') as book:
                a = requests.get(link, stream=True)

                for block in a.iter_content(512):
                    if not block:
                        break

                    book.write(block)
    except:
        raise
        print("Couldn't fetch pdf")
        return

if __name__ == "__main__":
    fetch()
