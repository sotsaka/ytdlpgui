from datetime import date
import sys

from PySide6.QtGui import QImage, QPicture, QPixmap
from artetv import Artetv
from francetv import Francetv
from video import Video
from utils import *
from yt_dlp.utils import DownloadError

#sudo apt install libopengl0 -yD:\TOOLS\python\Lib\site-packages\yt_dlp

#from PySide6 import QtCore, QtWidgets
#from PySide6.QtQuick import QQuickView
#import PySide6.QtQuickWidgets
#from PySide6.QtQuickWidgets import QQuickWidget

import PySide6
import PySide6.QtCore
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import   (QApplication,
                                 QCalendarWidget,
                                 QComboBox,
                                 QHBoxLayout,
                                 QLabel,
                                 QMainWindow,
                                 QMessageBox,
                                 QPushButton,
                                 QTabWidget,
                                 QTextEdit,
                                 QTreeWidget,
                                 QTreeWidgetItem,
                                 QVBoxLayout,
                                 QWidget
                                )
from PySide6.QtGui import QIcon, QPixmap
#from PySide6.QtGui import QPalette,QColor,QAction,QPixmap

class MyGui():
    def __init__(self):
        self.CHAINES = {"artetv" : Artetv(), "francetv" : Francetv()}

        self.DICTITEMS = {}
        for i in self.CHAINES.keys():
            self.DICTITEMS[self.CHAINES[i].url] = self.CHAINES[i]
        print(self.DICTITEMS)
        v = Video("https://www.arte.tv/en/videos/078750-020-A/open-worlds/")
        self.CHAINES["artetv"].listeEnfant.append(("openworld", v))
        v = Video("https://www.youtube.com/watch?v=UyavZeKsYTA")
        self.CHAINES["artetv"].listeEnfant.append(("utube", v))

        self.app = QApplication([])

        window = QMainWindow()
        window.setWindowTitle("My App")
        window.setMinimumSize(QSize(900, 600))


        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Item", "Url"])
        self.tree.setColumnWidth(0, 300)

        self.init_tree_widget(self.tree)
        self.tree.currentItemChanged.connect(self.onItemChanged)
        self.tree.itemDoubleClicked.connect(self.crawlItem)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)
        self.tabs.setMaximumHeight(200)


        self.information_tab = QTextEdit()
        self.information_tab.setText("<center><h1>Bienvenue</h1></center>")
        self.information_tabImage = QLabel()
        self.information_tabImage.setText("")


        information_tab_container = QWidget()
        layoutInfotab = QHBoxLayout()
        layoutInfotab.setContentsMargins(0,0,0,0)
        layoutInfotab.addWidget(self.information_tab)
        layoutInfotab.addWidget(self.information_tabImage)
        information_tab_container.setLayout(layoutInfotab)
        self.information_tab.resize(information_tab_container.size())
        self.information_tab.setMaximumHeight(information_tab_container.size().height())


        self.dictitemstab = QTextEdit()
        self.__refreshDictitemstab()

        self.dateBox = QCalendarWidget()

        self.tabs.addTab(information_tab_container, "informations")
        self.tabs.addTab(self.dictitemstab, "liste")
        self.tabs.addTab(self.dateBox, "date")

        self.infoButton = QComboBox()
        self.infoButton.setPlaceholderText("meilleur qualité")
        #self.infoButton.clicked.connect(self.infoVideo)

        self.crawlButton = QPushButton()
        self.crawlButton.setText("crawl")

        self.crawlButton.clicked.connect(self.crawlItem)

        layoutButton = QHBoxLayout()
        layoutButton.addWidget(self.infoButton)
        layoutButton.addWidget(self.crawlButton)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(self.tabs)
        layout.addLayout(layoutButton)

        container = QWidget()
        container.setLayout(layout)
        # Set the central widget of the Window.
        window.setCentralWidget(container)

        window.show()
        print("done")

        self.app.exec()

    def addChildToItem(self, parent, enfant):
        qtwi = QTreeWidgetItem()
        qtwi.setText(0, str(enfant[0]))
        qtwi.setText(1, str(enfant[1].url))
        self.DICTITEMS[enfant[1].url] = enfant[1]            
        parent.addChild(qtwi)

    def init_tree_widget(self, tree):
        for i in self.CHAINES.keys():
            a = QTreeWidgetItem()
            a.setText(0, i)
            a.setText(1, self.CHAINES[i].url)
            tree.addTopLevelItem(a)

    def getCurrentItemEvent(self, event):
        print(self.tree.currentItem().text(0))
        print(self.CHAINES[self.tree.currentItem().text(0)])
        #return event,self.CHAINES[event.text(0)]

    def getCurrentItem(self):
        ci = self.tree.currentItem()
        try:
            return ci, self.DICTITEMS[ci.text(1)]
        except KeyError:
            return None, None

    def infoVideo(self, event):
        item, objet = self.getCurrentItem()
        objet.extract_infos()
        text = ""
        try: 
            text += "<h1>{}</h1>".format(objet.infos['titre'])
        except:pass
        try:
            text += "<p>{}</p>".format(objet.infos['durée'])
        except:pass
        try:
            text += "<p>{}</p>".format(objet.infos['description'])
        except:pass
        try:
            text += "<p>{}</p>".format(objet.infos['categories'])
        except:pass
        try:
            text += "<p>{}</p>".format(objet.infos['tags'])
        except:pass

        self.information_tab.setText(text)
        """
        image = QPixmap(filepath_from_downloaded_image(""))
        #image.loadFromData(download_image(""))
        self.information_tabImage.setPixmap(image)
        """

    def crawlItem(self, event):
        item, objet = self.getCurrentItem()
        
        print(item, objet)
        """
        print(item.parent())
        for child_index in range(item.childCount()):
            print(item.child(child_index).text(1))
        """
        if isinstance(objet, Video):
            try:
                if self.infoButton.currentText() == "" or self.infoButton.currentText() == "meilleur qualité":
                    objet.download()
                else:
                    objet.download(self.infoButton.currentText().split(":")[0])#download(ID)
            except DownloadError as e:
                self.information_tab.setText(self.information_tab.toPlainText() +"\n" + str(e))
                mb = QMessageBox()
                mb.setIcon(mb.Icon.Warning)
                mb.setText("{0}".format(e))
                mb.setWindowTitle("Erreur de format")
                mb.exec()
 
                
        else:
            if item.parent() == None:
                objet.main()
                item.takeChildren()
                #ca ne les retire pas du modele, 
                #ca veut dire que des elt 'faux' peuvent toujours etre présents 
                #mais peuvent ne pas etre fonctionnel
                for j in self.__trierEnfants(objet.listeEnfant):
                    self.addChildToItem(item, j)
            else:
                chaineItem = self.__trouverChaineDeLItem(item)
                if item.text(0) == "guide":#bug c'est possible d'ajouter 2 fois le meme jour

                    selectedDate = self.dateBox.selectedDate()
                    if int(selectedDate.year()) < 10:
                        year = "0" + str(selectedDate.year())
                    else:
                        year = str(selectedDate.year())
                    if int(selectedDate.month()) < 10:
                        month = "0" + str(selectedDate.month())
                    else:
                        month = str(selectedDate.month())
                    if int(selectedDate.day()) < 10:
                        day = "0" + str(selectedDate.day())
                    else:
                        day = str(selectedDate.day())
                    datestring = year + month + day
                    #for child_index in range(item.childCount()):
                    #    pass

                    newitemDateDansGuide = QTreeWidgetItem()
                    newitemDateDansGuide.setText(0, datestring)
                    urlNewItemDateDansGuide = item.text(1) + datestring
                    newitemDateDansGuide.setText(1, urlNewItemDateDansGuide)
                    item.addChild(newitemDateDansGuide)
                    item.setSelected(True)
                    item.setExpanded(True)
                    print(chaineItem.text(0))
                    print(self.CHAINES[chaineItem.text(0)])
                    print(datestring)
                    self.CHAINES[chaineItem.text(0)].explorerVideosByDate(datestring)

                    trouve = False
                    for i in self.CHAINES[chaineItem.text(0)].listeEnfant: #je cherche ma categorie "guide",et ses enfants dans mon model
                        if i[0] == "guide":
                            for j in i[1].listeEnfant:
                                if j[0] == datestring:
                                    tmp = j[1].listeEnfant
                                    trouve = True
                                    break
                        if trouve == True:#categorie trouvée
                            break
                    for i in tmp:#je prend les enfants et je les mets dans la categorie=lejour 
                        print(i)
                        self.addChildToItem(newitemDateDansGuide, i)
                else:
                    if chaineItem.text(0) in self.CHAINES.keys():
                        self.CHAINES[chaineItem.text(0)].crawlCategorie(objet)
                    item.takeChildren()#ca ne les retire pas du modele, ca veut dire que des elt 'faux' peuvent toujours etre présents mais peuvent ne pas etre fonctionnel
                    for j in self.__trierEnfants(objet.listeEnfant):
                        self.addChildToItem(item, j)
                    item.setExpanded(True)
            self.crawlButton.setText("refresh")

            self.__refreshDictitemstab()

    def onItemChanged(self, event):
        item, objet = self.getCurrentItem()
        print(objet)
        
        if isinstance(objet, Video):
            while self.infoButton.count() != 0:
                self.infoButton.removeItem(0)
            self.infoVideo(event)
            formatOption = "petitformats"
            self.infoButton.addItem("meilleur qualité")
            for ligneformat in objet.infos[formatOption].values():
                textligne = "" + ligneformat['ID'] + ":"
                
                for i in list(ligneformat.values())[1:]:
                    if i != "":
                        textligne += i + ","
                self.infoButton.addItem(textligne[:-1])
            self.crawlButton.setText("download")
        else:
            if item.isExpanded():
                self.crawlButton.setText("refresh")
            else:
                self.crawlButton.setText("crawl")

        if item.text(0) == "guide":
            print("guide")

    def __trierEnfants(self, listDeNoeud):
        dico = dict(listDeNoeud)
        names = dico.keys()
        names = sorted(names)
        res = []
        for name in names:
            res.append((name, dico[name]))
        return res
    def __trouverChaineDeLItem(self, item):
        if item.parent() != None:
            return self.__trouverChaineDeLItem(item.parent())
        else:
            return item
    def __refreshDictitemstab(self):
        res = "items disponibles\n"
        for i in sorted(self.DICTITEMS.keys()):
            res += str(i) + "\n"
        self.dictitemstab.setText(res)




if __name__ == "__main__":
    MyGui()
