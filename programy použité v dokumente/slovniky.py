#prázdne slovníky
p_slovnik1 = dict()
p_slovnik2 = {}

#vytváranie neprázdnych slovníkov
slovnik1 = {"meno": "Fero", "vek":18, "stav":"slobodny"}
slovnik2 = dict(meno = "Anicka", vek = 19, stav = "slobodna")
slovnik3 = dict([("meno", "Anicka"), ("vek", 19), ("stav", "slobodna")])
slovnik4 = dict(zip(("meno", "vek", "stav"),("Jozef", 20, "slobodny")))


if  (slovnik1.contain("meno")):
    print("sdf")
