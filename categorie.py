from noeud import Noeud

class Categorie(Noeud):
    def __init__(self,url,path=None):
        super().__init__(url,path)
if __name__ == "__main__":
    print(Categorie("a"))