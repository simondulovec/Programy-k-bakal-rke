def ukaz_vlastnosti(**vyrobok):
    pom = ""
    for key in vyrobok:
        pom += "{}:{}, ".format(key, vyrobok[key])
    print(pom)

mikrovlnka = {"hmostnost": "5kg", "max_napatie": "240V"}
bazen = {"hmostnost": "20kg", "objem": "500L", "stav": "nove"}

ukaz_vlastnosti(**mikrovlnka)
ukaz_vlastnosti(**bazen)



