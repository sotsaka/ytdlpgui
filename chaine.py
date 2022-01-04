from noeud import Noeud

class Chaine(Noeud):
    def __init__(self,url):
        super().__init__(url)
if __name__ == "__main__":
    print(Chaine("a"))