import Scraper

x = Scraper.GetStats('Dilka30003', '0000', 'unrated')
print(x[0])
print(x[1])
if (x[0] == 0):
    Scraper.GenerateWeaponGraphic(x[1]).show()
elif (x[0] == 1):
    print("User not authenicated. Please authenticate " + x[1])
elif (x[0] == 404):
    print("User does not exist")