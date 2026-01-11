from bs4 import BeautifulSoup

with open(r'.\Web_Scraping\asimov_exemplo.html', 'r') as file:
    conteudo = file.read()

ex = BeautifulSoup(conteudo, 'lxml')

tags = ex.find_all(class_='um')

for tag in tags:
    print(tag.text)

