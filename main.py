import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }
)

url = "https://www.terabyteshop.com.br/busca?str=mem%C3%B3ria+ram+8gb+3200MHz"


def limpar_preco(texto_preco):
    if not texto_preco:
        return 0.0
    # Transforma "R$ 2.500,00" em 2500.00
    texto = texto_preco.replace('R$', '').replace(
        '.', '').replace(',', '.').strip()
    try:
        return float(texto)
    except:
        return 0.0


try:
    response = scraper.get(url)
    print(f"Status: {response.status_code}")

    dados_pagina = BeautifulSoup(response.text, 'html.parser')
    todas_frases = dados_pagina.find_all('div', class_="product-item")

    for div in todas_frases:

        # Define padrão caso não encontre
        nome = "Sem Nome"
        preco = "0"
        link = "Sem Link"

        nome = div.find('h2').text

        div_preco = div.find('div', class_="product-item__new-price")
        if div_preco:
            preco = div_preco.find('span').text

        link_tag = div.find('a', class_="product-item__name")
        if link_tag and link_tag.has_attr('href'):
            link = link_tag['href']

        print(f"Nome: {nome}")
        print(f"Preço: {limpar_preco(preco)}")
        print(f"Link: {link}")
        print("-" * 100)

except Exception as e:
    print(f"Erro: {e}")