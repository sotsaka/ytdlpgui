import yt_dlp
from yt_dlp import YoutubeDL
#https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L154-L452

def getFfmegLocation():
    import platform
    osname = platform.system()
    if osname == "Windows":
        ffmeglocation = ".\\ffmpeg\\ffmpeg.exe"
        outFolder = ".\\data\\%(title)s.%(ext)s"
    elif osname == "Linux":
        ffmeglocation = "./ffmpeg/ffmpeg"
        outFolder = "./data/%(title)s.%(ext)s"
    elif osname == "Darwin":
        pass
    else:
        raise OSError("os non supporte")
    return ffmeglocation,outFolder

class Video():
    def __init__(self,url):
        self.url = url
        self.infos = {}
        self.ffmeglocation,self.outFolder = getFfmegLocation()

    def outputStreamToDict(self,tmp):
        tmp = tmp.replace("0;32m","")
        tmp = tmp.replace("0;33m","")
        tmp = tmp.replace("0;34m","")
        tmp = tmp.replace("0m","")
        tmp = tmp.replace("\x1b","")
        tmp = tmp.replace("[","")
        tmp = tmp.replace("|","")
        tmp = tmp.replace("-","")
        tmp = tmp.split("\n")
        tailledescolonnes = [0]
        for i in range(len(tmp[0])-1):
            if tmp[0][i] == " " and tmp[0][i+1] != " ":
                tailledescolonnes.append(i)

        lescles = tmp[0].split(' ')
        lescles = [i for i in lescles if i != '']
        a = lescles.pop(-1)
        lescles[-1] = lescles[-1] + " " + a

        max = 0
        for i in tmp[1:]:
            if len(i) > max:
                max = len(i)
        tailledescolonnes[-1] = max
        lignes = []
        for ligne in tmp[1:]:
            tmp = []
            for indice in range(len(tailledescolonnes)-1):
                tmpligne = ligne[tailledescolonnes[indice]:tailledescolonnes[indice+1]]
                try:
                    while( tmpligne[0] == " "):
                        tmpligne = tmpligne[1:]
                except:pass
                try:
                    while( tmpligne[len(tmpligne)-1] == " "):
                        tmpligne = tmpligne[:len(tmpligne)-1]
                except:pass
                tmp.append(tmpligne)
            lignes.append(tmp)

        for ligne in lignes:
            for i in range(len(ligne)-1):
                l = ligne[i].split(' ')
                if len(l) > 1 :
                    ligne[i] = l[0]
                    ligne[i+1] = l[1] + ligne[i+1]

        tmpdictPetitFormat = {}
        tmpdictGrandFormat = {}
        for ligne in lignes:
            if ligne[0] == "": 
                pass
            else:
                tmp = {}
                tmppourinfos = {}
                for key in range(len(lescles)):
                    tmp[lescles[key]] = ligne[key]#grandformat
                    #petitformat
                    if str(lescles[key]) == "EXT" or str(lescles[key]) == "RESOLUTION" or str(lescles[key]) == "FPS" or str(lescles[key]) == "VCODEC" or str(lescles[key]) == "MORE INFO":
                        tmppourinfos[lescles[key]] = ligne[key]
                tmpdictPetitFormat[len(tmpdictPetitFormat)+1] = tmp
                tmpdictGrandFormat[tmp['ID']] = tmppourinfos
        return tmpdictPetitFormat, tmpdictGrandFormat


    def extract_infos(self):
        ydl_opts = {"simulate" : True,
                    "quiet" : True,
                    "writedescription" : True,
                    "outtmpl": self.outFolder,
                    "listformats" : True}
        infos = None
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl._screen_file = open('formats.infos', 'w')#redirige stdout vers "formats.info"
            infos = ydl.sanitize_info(ydl.extract_info(self.url))
        tmp = ""
        with open('formats.infos','r') as f:
            tmp = f.read()
        self.infos["petitformats"], self.infos["grandformats"] = self.outputStreamToDict(tmp)
        ydl_opts = {"simulate" : True,
                    "quiet" : True,
                    "check_formats" : True}
        with YoutubeDL(ydl_opts) as ydl:
            for i in self.infos["petitformats"].values():
                print(i['ID'])
                print(ydl._check_formats(i['ID']))
        
        if infos:#infos
            try:
                self.infos['titre'] = infos['title']
            except:pass
            try:
                heure = str(int(infos['duration']) // 3600)
                if heure == "0":
                    heure = ""
                else:
                    heure +="h"
                min = str((int(infos['duration']) % 3600) // 60)
                if min == "0":
                    min = ""
                else:
                    min +="m"
                sec = str(int(infos['duration']) % 60)
                if sec == "0":
                    sec = ""
                else:
                    sec += ""

                self.infos['durée'] =  heure + min + sec
            except:pass
            try:
                self.infos['thumbnail'] = infos['thumbnail']
            except:pass
            """
            try:
                self.infos['thumbnails'] =infos['thumbnails']
            except:pass
            """
            """
            for i in infos['formats']:
                try:
                    self.infos['ext'] = str(i['ext'])
                except:pass
                try:
                    self.infos['format_note'] = str(i['format_note'])
                except:pass
                try:
                    self.infos['langue'] = str(i['language'])
                except:pass
            """
            try:
                self.infos['description'] = infos['description']
            except:pass
            try:
                self.infos['categories'] = infos['categories']
            except:pass
            try:
                self.infos['tags'] = infos['tags']
            except:pass
            try:
                self.infos['is_live'] = infos['is_live']
            except:pass


            
            
        
    def download(self,format="best"):
        """
        Pour les formats ydl on peut directement préciser l'ID du format. La vidéo sera téléchargée avec le format correspondant à l'ID.
        voir aussi : https://github.com/yt-dlp/yt-dlp#format-selection, https://github.com/ytdl-org/youtube-dl/blob/master/README.md#format-selection
        """
        ydl_opts = {'simulate':True,#True pour les debugage
                    'outtmpl': self.outFolder,
                    'ffmpeg_location' : self.ffmeglocation,
                    'format' : str(format)}
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

if __name__ == "__main__":
    v = Video("https://www.youtube.com/watch?v=9qpBAAfTdtY")
    v.extract_infos()
    print(v.infos['titre'])
    v.download("worst")