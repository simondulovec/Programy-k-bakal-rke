class Zlomok:
    
    def __init__(self, citatel, menovatel):
        self.citatel = citatel
        self.menovatel = menovatel

    def __int__(self):
        return self.citatel//self.menovatel

    def __float__(self):
        return self.citatel/self.menovatel

    def __repr__(self):
        return "Ja som zlomok (z metódy __repr__())"

    def __str__(self):
        return "Ja som zlomok (z metódy __str__())"
    
z = Zlomok(3,2)
print(int(z))
print(float(z))
print(z)
