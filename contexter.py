# Python 3.8.5
# By Gabriel Romão
# Control C -> Copies word context to clipboard
# Control V-> Changes copied context
# Control T -> Pastes word's translation and breaks (allowing control C to work again)
# Control E -> Also breaks (in case you dont want translation)


# test 2
import bs4
import requests

# from googletrans import Translator
# translator=Translator()
# while True:
# translated=translator.translate( 'palavra' ,src='de',dest='en')
# print(translated.text)
import pyperclip

# pyperclip.paste() /.copy
import pyautogui

# pyautogui.hotkey('ctrl', 'c')
import keyboard

# keyboard.is.pressed()
import time
import pprint
import re
from selenium import webdriver
import selenium
from selenium.webdriver.support.ui import (
    WebDriverWait,
)  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser

# substituicao google translate
# def traduzir(palavra_traduzir):
#     option = webdriver.ChromeOptions()
#     option.add_argument('headless')
#     url_traducao = 'https://translate.google.com/?sl=de&tl=en&text=' + str(palavra_traduzir) + '&op=translate'
#     driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe',options=option)
#     driver.get(url_traducao)
#     command = "document.getElementById('source').value = '" + palavra_traduzir + "'"
#     driver.execute_script(command)
#     time.sleep(3)
#     output1 = driver.find_element_by_xpath( '/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]').text
#     return output1

# substituição langenscheidt
def traduzir(palavra_traduzir):
    url2 = "https://dict.leo.org/german-english/" + palavra_traduzir + "side=right"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    res2 = requests.get(url2, headers=headers)
    res2.raise_for_status()

    soup2 = bs4.BeautifulSoup(res.text, "html.parser")
    en_element = soup2.find_all("div", class_="isRelinked")
    return en_element[0]


# detect control C
while True:
    lista_frases = []
    lista_frases_final = []
    f = 0
    g = 1
    while True:
        if keyboard.is_pressed("ctrl+c"):
            time.sleep(0.3)
            palavra_original = pyperclip.paste()
            break

    # open page and get phrase
    url = "https://context.reverso.net/translation/german-english/" + palavra_original
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    de_element = soup.find_all("span", attrs={"class": "text", "lang": "de"})
    # print('pre regex')

    # regex começar com letra
    tirar_n = re.compile(r"\w.*")

    for i in range(len(de_element)):
        temp_list = de_element[i]
        temp_list_2 = temp_list.get_text()
        lista_frases.append(str(temp_list_2))

    for i in range(len(lista_frases)):
        mo1 = tirar_n.search(lista_frases[i]).group()
        lista_frases_final.append(mo1)

    # sort lista frases final
    def lensort(a):
        n = len(a)
        for i in range(n):
            for j in range(i + 1, n):
                if len(a[i]) > len(a[j]):
                    temp = a[i]
                    a[i] = a[j]
                    a[j] = temp
        return a

    lensort(lista_frases_final)

    # copy phrase to clipboard
    pyperclip.copy(lista_frases_final[0])
    print("Frase copiada para o clipboard")

    # get more phrases after ctrl+v #get translation with ctrl+t
    while f == 0:
        if keyboard.is_pressed("ctrl+v"):
            time.sleep(0.2)
            try:
                pyperclip.copy(lista_frases_final[g])
            except IndexError:
                print("Fim das frases")
                g = 0
            g = g + 1
            print("Trocando a frase")
        elif keyboard.is_pressed("ctrl+t"):
            traducao = traduzir(palavra_original)
            time.sleep(0.1)
            pyperclip.copy(traducao)
            time.sleep(0.1)
            # print(traducao.text)
            pyautogui.write(" " + traducao)
            time.sleep(0.1)
            # keyboard.press_and_release('ctrl+v')
            time.sleep(1)
            print("Voltando ao loop principal")
            f = 1
        elif keyboard.is_pressed("ctrl+e"):
            time.sleep(1)
            print("Voltando ao loop principal")
            f = 1
