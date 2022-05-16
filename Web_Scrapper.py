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
        city = input("Enter City(use Georgian font): ""\n")
        days_ = input("Enter how many days forecast you want(5,10,15,25): ""\n")
        curs.execute(f"DROP TABLE IF EXISTS {city}")
        curs.execute(f"CREATE TABLE {city}(WEATHER VARCHAR(255),WEEKDAY VARCHAR(255),DAY VARCHAR(255))")
        URL = (f"https://amindi.ge/ka/city/{city}/?d={days_}")
        req = requests.get(URL)
        soup = BeautifulSoup(req.content, 'html5lib')
        weather = soup.findAll('div', class_='degrees')
        weekdays = soup.findAll('div', class_='weekDay')
        day = soup.findAll('p',class_='day')
        daycount = []

        if city == "":
            pass
        elif days_ == "":
            pass

        for i in day:
            daycount.append(i.text)

        daytemperature = []
        for i in weather:
            daytemperature.append(i.span.text)

        daytemperature.pop(0)

        nighttemperature = []
        for div in weather:
            span = div.find_next('span').find_next('span')
            nighttemperature.append(span.text)
        nighttemperature.pop(0)
        weekdaycount = []
        for div in weekdays:
            weekdaycount.append(div.text)


        if days_ == "5":    
            print("ტემპერატურა შემდეგი 5 დღის განმავლობაში")
            for a,b,c,d in zip(daytemperature,nighttemperature,weekdaycount,daycount):
                print(f"{d} - {c} - {a}° - {b}°")
                insert = f"INSERT INTO {city}(WEATHER,WEEKDAY,DAY) values(%s,%s,%s)"
                val = ((f"{a}°-{b}°"),c,d)
                curs.execute(insert,val)

        elif days_ == "10":
            print("ტემპერატურა შემდეგი 10 დღის განმავლობაში")
            for a,b,c,d in zip(daycount,weekdaycount,daytemperature,nighttemperature):
                print(f"{d} - {c} - {a}° - {b}°")
                insert = f"INSERT INTO {city}(WEATHER,WEEKDAY,DAY) values(%s,%s,%s)"
                val = ((f"{a}°-{b}°"),c,d)
                curs.execute(insert,val)

        elif days_ == "15":
            print("ტემპერატურა შემდეგი 15 დღის განმავლობაში")    
            for a,b,c,d in zip(daytemperature,nighttemperature,weekdaycount,daycount):
                print(f"{d} - {c} - {a}° - {b}°")
                insert = f"INSERT INTO {city}(WEATHER,WEEKDAY,DAY) values(%s,%s,%s)"
                val = ((f"{a}°-{b}°"),c,d)
                curs.execute(insert,val) 

        elif days_ == "25":
            print("ტემპერატურა შემდეგი 25 დღის განმავლობაში")    
            for a,b,c,d in zip(daytemperature,nighttemperature,weekdaycount,daycount):
                print(f"{d} - {c} - {a}° - {b}°")
                insert = f"INSERT INTO {city}(WEATHER,WEEKDAY,DAY) values(%s,%s,%s)"
                val = ((f"{a}°-{b}°"),c,d)
                curs.execute(insert,val) 

        mydb.commit()

    except Exception as i:
        print(i)
        retry = input("Error try again?(Yes/No): ")
        if (retry != "Yes"):
            break       

