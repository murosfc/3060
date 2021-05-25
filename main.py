'''
RTX Scrapping 1.0
Por Felipe Muros
Bot para fazer busca de estoque de placas RTX na Amazon e fazer a compra
Versão 1.0 é a versão funcional utilizando Threads para otimizar a busca.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import threading
import winsound
import colorama
from colorama import Fore
from colorama import Style
import pyautogui
import os

#found = 0 #variável global de controle para encerrar outras threads quando alguma placa for encontrada em estoque

def login(navegador):
    navegador.find_element_by_xpath('//*[@id="nav-link-accountList-nav-line-1"]').click()  # clica fazer login
    navegador.find_element_by_xpath('//*[@id="ap_email"]').send_keys("muros@yahoo.com.br")  # digita endereço
    navegador.find_element_by_xpath('//*[@id="continue"]').click()  # clica em continuar
    navegador.find_element_by_xpath('//*[@id="ap_password"]').send_keys("Nafe1301")  # digita a senha
    navegador.find_element_by_xpath('//*[@id="signInSubmit"]').click()  # confirma login

def iniciar_navegador(link):
    driver = webdriver.Chrome()
    driver.get(link)
    login(driver)
    print('Navegador pronto para uso')
    return driver

def tocar_alarme():
    for i in range(0, 10):
        winsound.Beep(300, 200)
        winsound.Beep(300, 200)
        winsound.Beep(300, 700)

def comprar_item(navegador):
    threading.Thread(target=tocar_alarme).start()
    pyautogui.hotkey('ctrl', 'win', 'right')
    pyautogui.hotkey('win', 'd')
    navegador.maximize_window()
    navegador.find_element_by_xpath('//*[@id="add-to-cart-button"]').click()
    time.sleep(1)
    try:
        navegador.find_element_by_xpath('//*[@id="attachSiNoCoverage"]/span/input').click()
    except Exception:
        pass
    time.sleep(0.5)
    try:
        navegador.find_element_by_xpath('//*[@id="attach-sidesheet-checkout-button"]/span/input').click()
    except Exception:
        pass
    time.sleep(0.5)
    try:
        navegador.find_element_by_xpath('//*[@id="hlb-ptc-btn-native"]').click()
    except Exception:
        pass
    time.sleep(0.5)
    try:
        navegador.find_element_by_id("spc-orders").click()
    except Exception:
        pass
    time.sleep(0.5)
    try:
        navegador.find_element_by_id("placeYourOrder").click()
    except Exception:
        pass
    os.system('pause')

def bot_de_busca(driver, modelo, preco_limite):
    i = 1
    print (Fore.GREEN + "\nBusca do modelo " + modelo + " iniciada" + Style.RESET_ALL)
    while (i > 0):
        driver.refresh()
        for i in range(1, 25):
            try:
                driver.find_element_by_xpath(f'//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div[{i}]/div/span/div/div/div[2]/div[2]/div/div[3]/div[1]/div/div[1]/div[2]/a/span/span[2]/span[2]')
                preco = int(driver.find_element_by_xpath(f'//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div[{i}]/div/span/div/div/div[2]/div[2]/div/div[3]/div[1]/div/div[1]/div[2]/a/span/span[2]/span[2]').text)
                nome_do_item = driver.find_element_by_xpath(f'//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div[{i}]/div/span/div/div/div[2]/div[2]/div/div[1]/h2/a/span').text
                if nome_do_item.find(modelo) > 0:
                    print ('modelo desejado')
                if (preco < preco_limite and nome_do_item.find(modelo) > 0):
                    print(Fore.RED + "Modelo " + modelo + " disponível em estoque.\nProsseguindo com a compra..." + Style.RESET_ALL)
                    driver.find_element_by_xpath(
                        f'//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div[{i}]/div/span/div/div/div[2]/div[2]/div/div[1]/h2/a/span').click()
                    comprar_item(driver)
                    break
            except Exception:
                pass

def comprar_3060():
    modelo = '3060'
    preco_limite = 600
    link = r"https://www.amazon.com/s?k=RTX+3060&i=computers&bbn=284822&rh=n%3A284822&dc&qid=1621638530&rnid=2661599011&ref=sr_nr_p_n_availability_2"
    driver = iniciar_navegador(link)
    driver.minimize_window()
    bot_de_busca(driver, modelo, preco_limite)

print('\n')
comprar_3060()

