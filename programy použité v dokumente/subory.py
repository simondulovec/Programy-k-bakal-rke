subor = open('subor.txt', 'r')
riadok = subor.readline()
subor.close()
print(riadok)

with open('subor.txt', 'r') as subor2:
    riadok2 = subor2.readline()
print(riadok2)

from PIL import Image
img = Image.open("obrazok.jpg")
img.show()






