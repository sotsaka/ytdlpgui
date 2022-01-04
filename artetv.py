# -*- coding: utf-8-*-
#from requests_html import Element
import utils
from utils import *
import time


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Artetv(Chaine):
    def __init__(self):
        super().__init__("https://www.arte.tv/fr/")
        self.tousLesNoeuds = {}
        
        mytuple = (findNom(str("https://www.arte.tv/fr/guide/")), Categorie(str("https://www.arte.tv/fr/guide/")))
        self.ajouterElt(mytuple)
        self.ajouterDansTousLesNoeuds(mytuple,"https://www.arte.tv/fr/guide/")
    def main(self):
        self.trouverLesCategories()
    def ajouterDansTousLesNoeuds(self,elt,url):
        
        if hash(str(url)) in self.tousLesNoeuds.keys():
            print("deja instancié")
        else:
            self.tousLesNoeuds[hash(str(url))] = elt
       
    def explorerVideosByDate(self,datee):
        """
            date doit etre au format AAAAMMJJ
        """
        categorieGuide = getCategorie(self.listeEnfant,"guide")
        
        from datetime import date
        today = date.today()
        d = today.strftime("%Y%m%d")
        """
        if datee == "today":     
            start_url =  "https://www.arte.tv/fr/guide/"+str(d) #(format année+mois+jour)
            driver = self.startDriver()
            driver.get(start_url)
            tmp = driver.find_element_by_xpath("//div[@class='previous-programs']/button[@class='previous-programs__button']").click()
            text = driver.find_element_by_xpath("/html/body/div[@id='__next']/div/*[5]").get_attribute("innerHTML")
        else:
            start_url = "https://www.arte.tv/fr/guide/"+str(date) #(format année+mois+jour)
            driver = self.startDriver()
            driver.get(start_url)
            text = driver.find_element_by_xpath("/html/body/div[@id='__next']/div/div[@id='dayslider']/following-sibling::div/div").get_attribute("innerHTML")
        """
        if datee == "today":     
            start_url =  "https://www.arte.tv/fr/guide/"+str(d) #(format année+mois+jour)
            print("d" + d)
        else:
            start_url = "https://www.arte.tv/fr/guide/"+str(datee) #(format année+mois+jour)
        print("start_url : " + start_url)
        driver = self.startDriver()
        driver.get(start_url)
        elements = driver.find_elements_by_xpath("//div[@class='program-timeline']/div/a")
        print("len " + str(len(elements)))
        newCategorie = Categorie(start_url)
        """
        for url in getAllHref(text):
            if url[:len("https://www.arte.tv/fr/videos/")] == "https://www.arte.tv/fr/videos/":
                mytuple = (findNom(str(url)), Video(str(url)))
                newCategorie.ajouterElt(mytuple)
                self.ajouterDansTousLesNoeuds(mytuple,url)
            else:
                pass
        """
        for element in elements:
            url_ = element.get_attribute('href')
            self.creerItem(newCategorie,url_)

        categorieGuide.ajouterElt((findNom(str(newCategorie.url)),newCategorie))
        self.quitDriver(driver)


    def trouverLesCategories(self):
        for i in self.__trouverCategories():
            if i[0]=="/":
                laCategorie = Categorie(str(self.url)+str(i[4:]))
                mytuple = ( findNom(laCategorie.url),laCategorie )
                self.ajouterElt(mytuple)
                self.ajouterDansTousLesNoeuds(mytuple,laCategorie.url)
            else:pass
    def __trouverCategories(self):
        driver = self.startDriver()
        start_url = self.url
        driver.get(start_url)
        menuButton = driver.find_elements_by_xpath("//span[contains(text(),'Menu')]/..")[0].click()
        menuButton = driver.find_elements_by_xpath("//span[contains(text(),'Menu')]/../../*[2]/*[2]/*[3]")
        text = (menuButton[0].get_attribute("innerHTML"))
        self.quitDriver(driver)
        return getAllHref(text)

    
    def crawlCategorie(self,uneCategorie):
        if isinstance(uneCategorie,Categorie):
            if uneCategorie.xpath == None:
                self.__crawlCategorie(uneCategorie)
            else:#xpath != None                
                driver = self.startDriver()            
                start_url = uneCategorie.url
                driver.get(start_url)
                def __getindex(text):
                    i=0
                    while text[i] != "[":
                        i+=1
                    index = i
                    while text[i] != "]":
                        i+=1
                    return int(text[index+1:i])
                for i in range(__getindex(uneCategorie.xpath)):
                    self.__scrollDown(driver)
                elts = driver.find_elements_by_xpath(uneCategorie.xpath)
                if False:
                    elts = driver.find_elements_by_xpath(uneCategorie.xpath)
                    print(len(elts))
                    self.__clickOnRightArrowbutton(driver,"//main/*["+str(__getindex(uneCategorie.xpath))+"]/div/div[@data-testid='teaserHover']//button[@data-testid='next-arrow']")
                    self.__clickOnRightArrowbutton(driver,"//main/*["+str(__getindex(uneCategorie.xpath))+"]/div/div[@data-testid='teaserHover']//button[@data-testid='next-arrow']")
                    self.__clickOnRightArrowbutton(driver,"//main/*["+str(__getindex(uneCategorie.xpath))+"]/div/div[@data-testid='teaserHover']//button[@data-testid='next-arrow']")

                for elt in elts:
                    self.creerItem(uneCategorie,elt.get_attribute('href'))
                if False:
                    elts = driver.find_elements_by_xpath(uneCategorie.xpath)
                    print(len(elts))

                self.quitDriver(driver)

        

    def __crawlCategorie(self,uneCategorie):
        driver = self.startDriver()            
        start_url = uneCategorie.url
        driver.get(start_url)
        
        row = "random"
        i=0
        #self.trouverPremierElement(driver,uneCategorie)
        while row:            
            i+=1
                                
            try: 
                row = driver.find_element_by_xpath("//main/*["+str(i)+"]")
                crawled = False
            except Exception as e:
                row = None
            if row != None:
                try:
                    title = row.find_element_by_xpath("./div/div[3]//h2").get_attribute('innerHTML')
                    #"https://www.arte.tv/fr/"
                except:
                    title = None
                if title != None:
                    url_ = getAllHref(row.find_element_by_xpath("./div/div[3]").get_attribute('innerHTML'))
                    self.creerItem(uneCategorie,url_[0],title)
                    crawled = True
                           
                try:
                    title = row.find_element_by_xpath("./h2").get_attribute('innerHTML')
                    #"https://www.arte.tv/fr/videos/RC-014123/arte-reportage/"
                except:
                    title = None
                if title != None:
                    #allitems = slider.find_elements_by_xpath("./div/div[@data-testid='teaserItem']")
                    self.creerItem(uneCategorie,uneCategorie.url,title,xpath="//main/*["+str(i)+"]//div[@data-testid='teaserItem']/a | //main/*["+str(i)+"]/a")
                    crawled = True

                title = None

                try:
                    slider = row.find_element_by_xpath("./div[@data-testid='slider']")
                    #"https://www.arte.tv/fr/videos/RC-014123/arte-reportage/"
                except:
                    slider = None
                if slider != None:
                    #allitems = slider.find_elements_by_xpath("./div/div[@data-testid='teaserItem']")
                    title = row.find_element_by_xpath("./*[1]")
                    while title.get_attribute('innerHTML')[:len("<")] == "<":
                       title = title.find_element_by_xpath("./*") 
                    title = title.get_attribute('innerHTML')
                    voirToutButton = row.find_elements_by_xpath("./div[1]/a")
                    if len(voirToutButton) == 1: #il ya un boutton voir tout
                        voirToutUrl = voirToutButton[0].get_attribute('href')
                        self.creerItem(uneCategorie,voirToutUrl,title)
                    else:
                        test = driver.find_elements_by_xpath("//main/*["+str(i)+"]//div[@data-testid='teaserItem']/a")
                        if len(test) != 0:
                            self.creerItem(uneCategorie,uneCategorie.url,title,xpath="//main/*["+str(i)+"]//div[@data-testid='teaserItem']/a")
                    crawled = True

                slider = None

                if crawled == False or len(self.listeEnfant) == 0:
                    #print("err " + uneCategorie.url +  str(i))
                    if i != 1:
                        with open("err.file.txt",'a') as f:
                            f.write(uneCategorie.url + ":"+ str(i)+"\r")
                    self.creerItem(uneCategorie,uneCategorie.url,xpath="//main/*["+str(i)+"]//a")


            self.__scrollDown(driver)
        print(i-1)
        self.quitDriver(driver)

    def creerItem(self,node,url,titre="",xpath=None,drive=None,rightarrowpath=None):
        if drive!=None and rightarrowpath!=None:
            #print("enter")
            self.__clickOnRightArrowbutton(drive,rightarrowpath)
        if self.__is_Video(url):
            item = Video(str(url))
        else:
            item = Categorie(url,path=xpath)
        if titre=="":
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
        if (("-A/" in url) or ("-K/" in url) or ("-F/" in url)):
            return True
        else:return False

    def __clickOnRightArrowbutton(self,driver,path):
        buttonpath = ".//button[@data-testid='next-arrow']"
        slider = driver.find_element_by_xpath(path[:len(path)-len(buttonpath)+1])
        #print(path[:len(path)-len(buttonpath)+1])
        hover = ActionChains(driver).move_to_element(slider)
        hover.perform()
        tmp = slider.find_elements_by_xpath(path)
        try:
            print(tmp[0].get_attribute('outerHTML'))
            tmp[0].click()
        except:
            pass
        time.sleep(0.5)
               
    def __scrollDown(self,driver):
        actions = ActionChains(driver)
        for j in range(5):
            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
            time.sleep(0.2)
if __name__ == "__main__":
    a = Artetv()
    print(a)
    if True: #test pour guide tv en fontion du jour
        a.explorerVideosByDate("today")
        print(a.listeEnfant)
        cg = getCategorie(a.listeEnfant,"guide")
        print(cg.listeEnfant)
        from datetime import date
        today = date.today()
        d = today.strftime("%Y%m%d")
        print(d)
        cd = getCategorie(cg.listeEnfant,d)
        print(cd.listeEnfant)
    if False:
        c1 = Categorie("https://www.arte.tv/fr/")
        a.crawlCategorie(c1)
        print(c1.listeEnfant)
        print(c1.listeEnfant[5][0])
        print(c1.listeEnfant[5][1])
        print(c1.listeEnfant[5][1].xpath)

        a.crawlCategorie(c1.listeEnfant[5][1])
    if False:
        c1 = Categorie("https://www.arte.tv/fr/",path="//main/*[29]//div[@data-testid='teaserItem']/a")
        a.crawlCategorie(c1)
        print(c1.listeEnfant)
    if False:
        c2 = Categorie("https://www.arte.tv/fr/videos/RC-014123/arte-reportage/")
        a.crawlCategorie(c2)
        print(c2.listeEnfant)
        #print(getCategorie(c1.listeEnfant,'').listeEnfant)

    if False:
        a.trouverLesCategories()
        print(a.listeEnfant)
        #c = getCategorie(a.listeEnfant,"info-et-societe")
        c = Categorie("https://www.arte.tv/fr/videos/RC-014123/arte-reportage/")
        a.crawlCategorie(c)
        print(c.listeEnfant)
        for i in c.listeEnfant:
            print(str(i[0])+" : " +str(i[1].url)+ " : "+ str(i[1].xpath))
        cc1 = c.listeEnfant[0][1]
        cc2 = c.listeEnfant[1][1]
        cc3 = c.listeEnfant[2][1]
        a.crawlCategorie(cc1)
        print(cc1.listeEnfant)
        a.crawlCategorie(cc2)
        print(cc2.listeEnfant)
        #print(cc2.listeEnfant[-1][1].listeEnfant)
        a.crawlCategorie(cc3)
        print(cc3.listeEnfant)

        ccc2 = Categorie(getCategorie(cc2.listeEnfant,"?page=2").url)
        a.crawlCategorie(ccc2)
        print(ccc2.listeEnfant)
    if False:
        c0 = Categorie("https://www.arte.tv/fr/videos/cinema/films/?page=2") #ex non RC avec sous categorie
        a.crawlCategorie(c0)
        print(c0.listeEnfant)
        print(c0.listeEnfant[0][1])
        cc0 = c0.listeEnfant[0][1]
        a.crawlCategorie(cc0)
        print(cc0.listeEnfant)
        ccc0 = getCategorie(cc0.listeEnfant,"?page=3")
        a.crawlCategorie(ccc0)
        print(ccc0.listeEnfant)

    
    if False:

        c1 = Categorie("https://www.arte.tv/fr/videos/RC-021397/le-cinema-de-bruno-dumont/")#ex RC avec une sous categorie
        a.crawlCategorie(c1)
        print(c1.listeEnfant)
        print(getCategorie(c1.listeEnfant,'Toutes les vidéos').listeEnfant)
        for i in c1.listeEnfant:
            if isinstance(i[1],Categorie):
                a.crawlCategorie(i[1])
                print("\t#########")
                print(i[1].listeEnfant)
    if False:
        c2 = Categorie("https://www.arte.tv/fr/videos/cinema/films/") #ex non RC avec sous categorie
        a.crawlCategorie(c2)
        print(c2.listeEnfant)
        for i in c2.listeEnfant:
            if isinstance(i[1],Categorie):
                a.crawlCategorie(i[1])
                print("\t#########")
                print(i[1].listeEnfant)
    if False:#problèmes generales
        c3 = Categorie("https://www.arte.tv/fr/videos/info-et-societe")#ex Categorie de base
        a.crawlCategorie(c3)
        print(c3.listeEnfant)
        for i in c3.listeEnfant:
            if isinstance(i[1],Categorie):
                print(":::" + i[1].url)
                a.crawlCategorie(i[1])
                for elt in i[1].listeEnfant:
                    if isinstance(elt[1],Categorie):
                        print(":::" + elt[1].url)
                        a.crawlCategorie(elt[1])
        #err https://www.arte.tv/fr/videos/RC-018674/l-afghanistan-sous-le-regne-des-talibans/1
        #err https://www.arte.tv/fr/videos/RC-014078/square/1
        #right arrow
        #coublons de nom afficher slash avant
    if False:
        c4 = Categorie("https://www.arte.tv/fr/videos/RC-017319/culture-hip-hop/")#ex RC equivalaent à categorie de base
        a.crawlCategorie(c4)
        print(c4.listeEnfant)
        
        for i in c4.listeEnfant: #prend une quinzaine de minutes
            if isinstance(i[1],Categorie):
                a.crawlCategorie(i[1])
                print("\t#########")
                print(i[1].listeEnfant)



    if False:#fleche droite
        c5 = Categorie("https://www.arte.tv/fr/videos/info-et-societe/",path="//main/*[3]//div[@data-testid='teaserItem']/a")
        a.crawlCategorie(c5)
        print(c5.listeEnfant)
        print(len(c5.listeEnfant))
        #a.crawlCategorie(c5)
    if False:#other elt
        c6 = Categorie("https://www.arte.tv/fr/arte-concert/plus-recentes/?genres=opera")
        a.crawlCategorie(c6)
        print(c6.listeEnfant)
