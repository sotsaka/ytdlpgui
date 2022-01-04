from abc import ABC, abstractmethod
import os
import sys
import platform
if platform.system() == "Linux":
    sys.path.append('/home/simon/.local/lib/python3.8/site-packages') #problem sur linux

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import utils
from utils import *
import time
class Noeud(ABC):
    
    @abstractmethod
    def __init__(self,url,path=None):
        self.url = url
        self.xpath = path
        self.listeEnfant = []
        
        
    def ajouterElt(self,elt):
        if elt in self.listeEnfant:
            print("deja dans la liste des enfants")
        else:
            self.listeEnfant.append(elt)

    def startDriver(self):
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        #chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        #chrome_options.add_argument("--window-size=3000x1080")
        #chrome_options.add_argument("start-maximised")
        #chrome_options.headless = True # also works
        import platform
        osname = platform.system()
        if osname == "Windows":
            chromedriverpath = "chromedriverfolder\\chromedriver.exe"
        elif osname == "Linux":
            chromedriverpath = "./chromedriverfolder/chromedriver"       
        elif osname == "Darwin":
            chromedriverpath = "chromedriverfolder/chromedrivermac"
        else:
            raise OSError("os non supporte")
        print(chromedriverpath)
        driver = webdriver.Chrome(executable_path=chromedriverpath,options=chrome_options)

        return driver
    def quitDriver(self,drive):
        drive.quit()
    def __scrollDown(self,driver):
        actions = ActionChains(driver)
        for j in range(5):
            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
            time.sleep(0.5)
    def __str__(self):
        return self.url
if __name__ == "__main__":
    #Noeud("a")
    title ="   fce \trff        " 
    for i in traiterTitle(title):
        print(i)
    print(str(repr(traiterTitle(title))))
