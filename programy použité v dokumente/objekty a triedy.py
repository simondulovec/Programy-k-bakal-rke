class Zviera:
    def __init__(self, meno, zvuk="vrrrr"):
        self.meno = meno
        self.zvuk = zvuk

    def vydaj_zvuk(self):
        print(self.zvuk)

class Macka(Zviera):
    def __init__(self, meno, zvuk):
        super().__init__(meno, zvuk)

class Pes(Zviera):
    def __init__(self, meno, zvuk):
        super().__init__(meno, zvuk)

zviera = Zviera("Fero")
macka = Macka("Aneta", "Mnau")
pes = Pes("Dunco","Hav") 

zviera.vydaj_zvuk()
macka.vydaj_zvuk()
pes.vydaj_zvuk()




