p_list1 = list()
p_list2 = []

list1 = [1, 2, "kvet", 3.14, "strom", p_list1]
list2 = list(list1)

r_list = list1[0:4]

meno = "Anicka"
n_list = list(meno)

print(r_list)
print(n_list)
print(list1[0])
print(list1[-1])
print(list1[-2])

if (list1 == list2):
    print("Listy sú rovnaké!")
else:
    print("Listy nie sú rovnaké!")




    
