import requests
from bs4 import BeautifulSoup
import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = 'weather'
)

curs = mydb.cursor()


while True:
    try:
        city = input("\n" "Enter City(use Georgian font): " "\n")  
        days_ = int(input("\n" "Enter how many days forecast you want(5,10,15,25): " "\n")) 
        URL = (f"https://amindi.ge/ka/city/{city}/?d={days_}")
        req = requests.get(URL)
        soup = BeautifulSoup(req.content, 'html5lib')
        cities = soup.find('div', class_='dropdown-menu').findAll('ul')[0].findAll('li') + \
                    soup.find('div', class_='dropdown-menu').findAll('ul')[1].findAll('li')               
        day = soup.findAll('p', class_='day')

        weather = soup.findAll('div', class_='degrees')
        weekdays = soup.findAll('div', class_='weekDay')

        citieslist = []      

        for i in cities:
            varcities = i.find("a").text.rstrip(i.find("a").find("span").text)
            citieslist.append(varcities)

  
        if city not in citieslist:
            print("Wrong City Name!")
            break

        curs.execute(f"DROP TABLE IF EXISTS {city}")
        curs.execute(f"CREATE TABLE {city}(WEATHER VARCHAR(255),WEEKDAY VARCHAR(255),DATE VARCHAR(255))")

        daycount = []
        daytemperature = []
        nighttemperature = []

        if days_ == "":
            break

        for i in day:
            daycount.append(i.text)

        for i in weather:
            daytemperature.append(i.span.text)

        daytemperature.pop(0)
 
        for div in weather:
            span = div.find_next('span').find_next('span')
            nighttemperature.append(span.text)
            
        nighttemperature.pop(0)
        weekdaycount = []
        for div in weekdays:
            weekdaycount.append(div.text)    
     
        #checking if entered days are correct
        if days_ == 5 or days_ == 10 or days_ == 15 or days_ == 25:
            print("\n" f"({city}) - ტემპერატურა შემდეგი {days_} დღის განმავლობაში" "\n")
            for a,b,c,d in zip(daytemperature,nighttemperature,weekdaycount,daycount):
                print(f"{d} - {c} - {a}° - {b}°")
                insert = f"INSERT INTO {city}(WEATHER,WEEKDAY,DATE) values(%s,%s,%s)"
                val = ((f"{a}°-{b}°"),c,d)
                curs.execute(insert,val)

        else:
            break


        mydb.commit()

    except Exception as i:
        print(i)
        retry = str(input("try again?(Yes/No): "))
        if retry != "Yes" and retry != "yes":
            break   
