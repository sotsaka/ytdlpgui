# -*- coding: utf-8-*-
#from requests_html import Element
import utils
from utils import *
import time


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Francetv(Chaine):
    def __init__(self):
        super().__init__("https://www.france.tv/")
        self.tousLesNoeuds = {}
        
        mytuple = ("guide", Categorie(str("https://www.france.tv/chaines/")))
        self.ajouterElt(mytuple)
        self.ajouterDansTousLesNoeuds(mytuple,"https://www.france.tv/chaines/")
        #alaune
        #recherche

    def ajouterDansTousLesNoeuds(self,elt,url):
        
        if hash(str(url)) in self.tousLesNoeuds.keys():
            print("deja instancié")
        else:
            self.tousLesNoeuds[hash(str(url))] = elt
       
    def explorerVideosByDate(self,datee):#encours
        def cliquer_sur_le_jour(date):#les dates de francetv sont de la forme AAAA-MM-JJ
            pass
        driver = self.startDriver()
        start_url = getCategorie(self.listeEnfant,"guide").url
        print(start_url)
        driver.get(start_url)
        try:
            self.__accepterCookies(driver)
        except:
            pass
        from datetime import date
        today = date.today()
        d = today.strftime("%Y%m%d")
        print(d)
        print(type(d))
        if str(datee) == "today" or str(datee) == d:
            pass
        else:            
            elements = driver.find_elements_by_xpath("//main/div[contains(@class,'c-days-slider')]//div[contains(@class,'c-days-slider__content')]/a")
            #print(len(elements))
            for i in elements:
                #print((datee[0:4] + "-" + datee[4:6] + "-" + datee[6:8]))
                #print(str(i.get_attribute('data-date')))
                if str(i.get_attribute('data-date')) == (datee[0:4] + "-" + datee[4:6] + "-" + datee[6:8]):
                    i.click()
        time.sleep(1)
        #endirect #id=live_slider
        #js-section-stream-content

        #je veux recupérer les noms des chaines dans l'ordre
        ordredeschaines = driver.find_elements_by_xpath("//main//div[contains(@class,'c-stream-menu__item')]")
        listeDesChaines = []
        for elt in ordredeschaines:
            noms = elt.get_attribute('data-streams')
            for i in noms.split(','):
                listeDesChaines.append(i)

        lapremierpage = driver.find_element_by_xpath("//main//div[contains(@class,'c-section-stream-cards ')]")#l'espace à la fin du xpath est important (essai de l'enlever pour voir)
        #il faut clicker sur la fleche de droite pour load le reste des chaines
        flechedroite = driver.find_element_by_xpath("//main/div//span[contains(@class,'c-stream-menu__next')]")
        flechedroite.click()
        ladeuxiemepage = driver.find_element_by_xpath("//main//div[contains(@class,'c-section-stream-cards ')]")#l'espace à la fin du xpath est important (essai de l'enlever pour voir)
        print(lapremierpage)
        #print(lapremierpage.get_attribute('id'))
        #à travailler
        #matinApremFinDeETCTITRE = driver.find_elements_by_xpath("//main//div[contains(@class,'c-section-stream-cards ')]/h3")
        matinApremFinDeETC = driver.find_elements_by_xpath("//main//div[contains(@class,'c-section-stream-cards ')]/div")

        for colonne in matinApremFinDeETC:
            print(i.get_attribute('innerHTML'))
        self.quitDriver(driver)

    def main(self):
        self.trouverLesCategories()
    def trouverLesCategories(self):
        for i in self.__trouverCategories():
            if (i[:len(self.url)]==self.url):
                self.creerItem(self,i,titre=findNom(i))
            elif (i[0] == "/"):
                self.creerItem(self,self.url + str(i[1:]),titre=findNom(self.url + str(i[1:])))
            else:pass

    def __trouverCategories(self):
        listearetourner = []

        driver = self.startDriver()
        start_url = self.url
        driver.get(start_url)
        self.__accepterCookies(driver)
        navbar = driver.find_elements_by_xpath("//nav[@role='navigation']/ul/li")
        chaines_navbar = navbar[1].find_elements_by_xpath("./div/ul/li")
        for elt in chaines_navbar:
            elt = elt.find_element_by_xpath("./a").get_attribute('href')
            listearetourner.append(elt)

        categories_navbar = driver.find_elements_by_xpath("//nav[@role='navigation']/ul//li[contains(@class,'categories-item')]")
        for elt in categories_navbar:
            elt = elt.find_element_by_xpath("./a").get_attribute('href')
            listearetourner.append(elt)

        self.quitDriver(driver)
        return list(set(listearetourner))


    def crawlCategorie(self,uneCategorie):
        
        if isinstance(uneCategorie,Categorie):
            if uneCategorie.xpath == None:
                self.__crawlCategorie(uneCategorie)
            else:#xpath != None                
                driver = self.startDriver()
                start_url = uneCategorie.url
                driver.get(start_url)
                try:
                    self.__accepterCookies(driver)
                except:
                    pass
                elements = driver.find_elements_by_xpath(uneCategorie.xpath)
                for elt in elements:
                    self.creerItem(uneCategorie,elt.get_attribute('href'))

                self.quitDriver(driver)

    def __crawlCategorie(self,uneCategorie):
        driver = self.startDriver()
        start_url = uneCategorie.url
        driver.get(start_url)
        try:
            self.__accepterCookies(driver)
        except:
            pass
        tousLesDivDeLaPage = driver.find_elements_by_xpath("//body/main/*")
        k=0
        i = tousLesDivDeLaPage[k]
        while ("c-more-content-button" not in i.get_attribute("class").split(' ')) and (k<len(tousLesDivDeLaPage)):
            #print(i.get_attribute("class"))
            atts = i.get_attribute("class").split(' ')

            if ("c-slider" in atts):
                title = i.find_element_by_xpath("./ul[contains(@class,'c-slider__content')]").get_attribute("id")
                #slider_content = i.find_elements_by_xpath("./ul[contains(@class,'c-slider__content')]/li//a")
                if i is tousLesDivDeLaPage[0]:
                    title = "slider à la une"
                self.creerItem(uneCategorie,uneCategorie.url,traiterTitle(title),xpath="//body/main/*["+str(k+1)+"]/ul[contains(@class,'c-slider__content')]/li//a")


            if ("c-now-on-channel" in atts):
                title = i.find_element_by_xpath(".//*[contains(@class,'c-section-header__title')]").get_attribute("innerHTML")
                #slider_content = i.find_elements_by_xpath(".//*[contains(@class,'c-now-on-channel__content')]//a")
                """
                for elt in slider_content:
                    print(elt.get_attribute("title"))
                    print(elt.get_attribute("href"))
                """
                self.creerItem(uneCategorie,uneCategorie.url,traiterTitle(title),xpath="//body/main/*["+str(k+1)+"]//*[contains(@class,'c-now-on-channel__content')]//a")


            if ("c-playlist" in atts):
                tmp = i.find_elements_by_xpath("./div[contains(@class,'c-section-slider')]")
                for index in range(len(tmp)):
                    elt = tmp[index]
                    title = elt.find_element_by_xpath(".//h2").get_attribute('innerHTML')
                    #print(title)
                    #slider_content = elt.find_elements_by_xpath("./div[2]//*[contains(@class,'c-slider__content')]/li//a")
                    """
                    print(len(slider_content))
                    for j in slider_content:
                        print(j.get_attribute('href'))
                    """
                    self.creerItem(uneCategorie,uneCategorie.url,traiterTitle(title),xpath="//body/main/*["+str(k+1)+"]/div[contains(@class,'c-section-slider')]["+str(index+1)+"]/div[2]//*[contains(@class,'c-slider__content')]/li//a")
                    

            if ("c-solo-mea" in atts):
                title = url_ = i.find_element_by_xpath(".//a").get_attribute('href')
                #print(title)
                self.creerItem(uneCategorie,url_,traiterTitle(title))

            if ("c-section-slider" in atts):
                title = i.find_element_by_xpath("./div/h2").get_attribute('innerHTML')
                #print(title)
                """
                slider_content = i.find_elements_by_xpath("./div[2]//*[contains(@class,'c-slider__content')]/li//a")
                for j in slider_content:
                        print(j.get_attribute('href'))
                """
                self.creerItem(uneCategorie,uneCategorie.url,traiterTitle(title),xpath="//body/main/*["+str(k+1)+"]/div[2]//*[contains(@class,'c-slider__content')]/li//a")

                
                
            if ("c-section-salto-mesh" in atts):
                elt = i.find_element_by_xpath("./a")
                title = elt.get_attribute('title')
                content = elt.get_attribute('href')
                self.creerItem(uneCategorie,content,title)

            if ("c-section-pagination" in atts):
                #https://www.france.tv/collection/1207791-osez-rever-d-aventure/
                title = uneCategorie.url
                """
                print(title)
                content = i.find_elements_by_xpath("./div[contains(@class,'c-wall')]/a")
                for elt in content:
                    print(elt.get_attribute('href'))
                """
                self.creerItem(uneCategorie,uneCategorie.url,titre=findNom(title),xpath="//body/main/*["+str(k+1)+"]/div[contains(@class,'c-wall')]/a | //body/main/*["+str(k+1)+"]//*[contains(@class,'c-wall__item')]/a")

            if ("c-section-mea" in atts):
                try:
                    title = i.find_element_by_xpath("./div/a").get_attribute('href')
                except:
                    try:
                        title = i.find_element_by_xpath("./a").get_attribute('href')
                    except:
                        pass

                #print(title)
            if ("c-section-sub-categories" in atts):               
                
                for elt in i.find_elements_by_xpath("./div[2]/a"):
                    url_ = elt.get_attribute('href')
                    self.creerItem(uneCategorie,url_,titre=self.__findNom_subcategorie(url_))
                #self.creerItem(uneCategorie,self.url,xpath="//body/main/*["+str(k)+"]/div[2]/a")
            if ("c-section-video-wall-block" in atts):
                title = i.find_element_by_xpath("./div/h2").get_attribute('innerHTML')
                print(title)
                content = i.find_elements_by_xpath("./ul/li/a")
                self.creerItem(uneCategorie,uneCategorie.url,traiterTitle(title),xpath="//body/main/*["+str(k+1)+"]/ul/li/a")


            k +=1
            try:
                i = tousLesDivDeLaPage[k]
            except Exception as e:
                pass


        print("stopped")
        try:
            i = tousLesDivDeLaPage[k]
            if "c-more-content-button" in i.get_attribute("class").split(' '):
                content = i.find_element_by_xpath("./a").get_attribute('href')#toutes les videos et tous les programmes
                #print(content)
                self.creerItem(uneCategorie,content)

        except Exception as e:
            pass
        if len(self.listeEnfant) == 0:
            #print("err " + uneCategorie.url +  str(i))
            if i != 1:
                with open("err.file.txt",'a') as f:
                    f.write(uneCategorie.url + ":"+ str(i)+"\r")
            self.creerItem(uneCategorie,uneCategorie.url,xpath="//main/*["+str(i)+"]//a")
        self.quitDriver(driver)

    def __accepterCookies(self,driver):
        driver.find_element_by_xpath("//button[@id='didomi-notice-disagree-button']").click()
    
    def creerItem(self,node,url,titre=None,xpath=None):
        if self.__is_Video(url):
            item = Video(str(url))
        else:
            item = Categorie(url,path=xpath)
        if titre==None:
            titre = findNom(item.url)
        titre = titre.lower()

        mytuple = ( titre , item )
        node.ajouterElt(mytuple)
        if self.__is_Video(url):
            self.ajouterDansTousLesNoeuds(mytuple, item.url)
        else:
            if item.xpath == None:
                self.ajouterDansTousLesNoeuds(mytuple, item.url)
            else:
                self.ajouterDansTousLesNoeuds(mytuple, item.url +"@"+ item.xpath)

    def __is_Video(self,url):
        if url[-5:] == ".html":
            return True
        else: return False
    def __findNom_subcategorie(self,msg):
        if len(msg)>0:
            tmp = []
            for j in range(len(msg)):
                if msg[j] =="/":
                    tmp.append(j)
            if len(tmp)>1:
                if msg[-1] == "/":
                    return msg[tmp[-3]+1:tmp[-1]]
                else:
                    return msg[tmp[-2]+1:]
        return msg
if __name__ == "__main__":
    f = Francetv()
    print(f)

    if False:
        f.trouverLesCategories()
        print(f.listeEnfant)
    if False:
        c = Categorie("https://www.france.tv/france-2/")
        f.crawlCategorie(c)
        print(c.listeEnfant)
    if False:#pas encore fait c'est le truc de explorer par date
        c = Categorie("https://www.france.tv/chaines/")
    if False:
        cr = Categorie("https://www.france.tv/recherche/")
    if True:
        c1 = Categorie("https://www.france.tv/")
        c2 = Categorie("https://www.france.tv/france-2/")
        c3 = Categorie("https://www.france.tv/france-3/")
        c4 = Categorie("https://www.france.tv/france-4/")
        c5 = Categorie("https://www.france.tv/france-5/")
        c6 = Categorie("https://www.france.tv/la1ere/")#euh pas pour l'instant +voir "https://www.france.tv/la1ere/toutes-les-videos/"
        c7 = Categorie("https://www.france.tv/franceinfo/")
        c8 = Categorie("https://www.france.tv/spectacles-et-culture/")
        c9 = Categorie("https://www.france.tv/slash/")
        c10 = Categorie("https://www.france.tv/enfants/")
        c11 = Categorie("https://www.france.tv/series-et-fictions/")
        c12 = Categorie("https://www.france.tv/documentaires/")
        c13 = Categorie("https://www.france.tv/films/")
        c14 = Categorie("https://www.france.tv/actualites-et-societe/")
        c15 = Categorie("https://www.france.tv/spectacles-et-culture/")
        c16 = Categorie("https://www.france.tv/sport/")
        c17 = Categorie("https://www.france.tv/jeux-et-divertissements/")
        c18 = Categorie("https://www.france.tv/vie-quotidienne/")
        c19 = Categorie("https://www.france.tv/toutes-les-videos/")
        c20 = Categorie("https://www.france.tv/tous-les-programmes/")
        for i in range(1,21):
            c = locals()["c" + str(i)]
            print("->" + str(c.url))
            f.crawlCategorie(c)
            print("listeEnfant : ")
            print(c.listeEnfant)
    if False:
        cx1 = Categorie("https://www.france.tv/france-2/",path="//body/main/*[1]/ul[contains(@class,'c-slider__content')]/li//a")
        cx2 = Categorie("https://www.france.tv/france-3/",path="//body/main/*[2]//*[contains(@class,'c-now-on-channel__content')]//a")
        cx3 = Categorie("https://www.france.tv/france-3/",path="//body/main/*[7]/div[contains(@class,'c-section-slider')][2]/div[2]//*[contains(@class,'c-slider__content')]/li//a")
        cx4 = Categorie("https://www.france.tv/france-3/",path="//body/main/*[7]/div[contains(@class,'c-section-slider')][2]/div[4]//*[contains(@class,'c-slider__content')]/li//a")
        cx5 = Categorie("https://www.france.tv/france-3/",path="//body/main/*[5]/div[2]//*[contains(@class,'c-slider__content')]/li//a")
        cx6 = Categorie("https://www.france.tv/la1ere/toutes-les-videos/",path="//body/main/*[3]/div[contains(@class,'c-wall')]/a")
        #cx8 = Categorie("https://www.france.tv/la1ere/toutes-les-videos/",path="//body/main/*[3]/div[contains(@class,'c-wall')]/a")
        for i in range(1,7):
            c = locals()["cx" + str(i)]
            print("->" + str(c.url))
            f.crawlCategorie(c)
            print("listeEnfant : ")
            print(c.listeEnfant)
    if False:
        cx1 = Categorie("https://www.france.tv/france-2/")
        f.crawlCategorie(cx1)
        for i in cx1.listeEnfant:
            print(i[1].url + " : " + str(i[1].xpath))
            f.crawlCategorie(i[1])
            print(i[1].listeEnfant)
    if False:
        cc1 = Categorie("https://www.france.tv/france-2/infrarouge/")
        cc2 = Categorie("https://www.france.tv/france-2/j-ai-menti/")
        cc3 = Categorie("https://www.france.tv/collection/1207791-osez-rever-d-aventure/")

        for i in range(1,4):
            c = locals()["cc" + str(i)]
            print("->" + str(c.url))
            f.crawlCategorie(c)
            print("listeEnfant : ")
            print(c.listeEnfant)
            for j in c.listeEnfant:
                print("")
                print(j)
                f.crawlCategorie(j[1])
                print("--> "+str(j[1]))
                print(j[1].listeEnfant)
        
    if False:
        f.explorerVideosByDate("20211226")
        print(f.listeEnfant)
        c = getCategorie(f.listeEnfant,"guide")
        c.listeEnfant


