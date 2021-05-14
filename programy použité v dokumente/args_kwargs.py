def vypocitaj_obvod(*mnohouholnik):
    obvod = 0
    for strana in mnohouholnik:
        obvod += strana
    print(obvod)

desatuholnik = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
trojuholnik = [4, 4, 5]

vypocitaj_obvod(*desatuholnik)
vypocitaj_obvod(*trojuholnik)


