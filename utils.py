import sys
try:
    from noeud import Noeud

    from chaine import Chaine
    from categorie import Categorie
    from video import Video
except ImportError:
    pass
import requests

def getCategorie(tab,nomCategorie):
    for i in tab:
        if i[0] == nomCategorie and isinstance(i[1],Categorie):
            return i[1]
"""
def getSerie(tab,nomSerie):
    for i in tab:
        if i[0] == nomSerie and isinstance(i[1],Serie):
            return i[1]
"""
def getVideo(tab,nomVideo):
    for i in tab:
        if i[0] == nomVideo and isinstance(i[1],Video):
            return i[1]
def getNoeudByUrl(tab,url):
    for i in tab:
        if i[0] == url:
            return i[1]


def getAllHref(text):
        tmp = []
        for i in range(len(text)):
            if (text[i]=="h" and text[i+1]=="r" and text[i+2]=="e" and text[i+3]=="f" and text[i+4]=="=" ):
                mystr=""
                j = i+6 #href="link"
                        #123456
                if text[i+5]=="\'":
                    while(text[j]!="\'"):#caractere: '
                        mystr += text[j]
                        j+=1
                if text[i+5]=="\"":
                    while(text[j]!="\""):#caractère: "
                        mystr += text[j]
                        j+=1
                tmp.append(mystr)
        return tmp
def findNom(msg):
            if len(msg)>0:
                tmp = []
                for j in range(len(msg)):
                    if msg[j] =="/":
                        tmp.append(j)
                if len(tmp)>1:
                    if msg[-1] == "/":
                        return msg[tmp[-2]+1:tmp[-1]]
                    else:
                        return msg[tmp[-1]+1:]
            return msg
def traiterTitle(titre):
    while( titre[0] == " "):
        titre = titre[1:]
    while( titre[len(titre)-1] == " "):
        titre = titre[:len(titre)-1]
    tmp =""
    for i in titre:
        if i == " ":
            tmp += "-"
        else:
            tmp+=i
    return tmp  
def filepath_from_downloaded_image(url,path_pour_sauvegarder_image="./data/images/imageInfoTab.image"):
    try:
        tmp = requests.get("https://i.ytimg.com/vi_webp/UyavZeKsYTA/maxresdefault.webp")
        print(tmp.__dict__)
        with open(path_pour_sauvegarder_image, 'wb') as f:
            f.write(tmp.content)
        return path_pour_sauvegarder_image
    except:
        print("impossible de telecharger l'image")
if __name__ == "__main__":
    pass
