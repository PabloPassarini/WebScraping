from bs4 import BeautifulSoup
import requests, os, re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def get_price(link):
    if 'kabum' in link:
        site = 'Kabum'
        tag_valor = 'h4'
        class_valor = 'sc-5492faee-2 ipHrwP finalPrice'

        tag_nome = 'h1'
        class_nome = 'sc-58b2114e-6 brTtKt'

    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    tag = soup.find_all(tag_valor, class_=re.compile(class_valor))
    for item in tag:
        valor = item.text
        if "R$" in valor:
            break

    tag = soup.find_all(tag_nome, class_=re.compile(class_nome))
    for item in tag:
        nome = item.text
       
    
    print(valor, nome)

get_price('https://www.kabum.com.br/produto/643102/console-ps5-pro-sony-ssd-2tb-com-controle-sem-fio-dualsense-branco')