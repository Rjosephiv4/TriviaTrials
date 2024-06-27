from bs4 import BeautifulSoup
import requests
import datetime

def scrapper():
    
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    day = datetime.datetime.now().day
    month = months[(datetime.datetime.now().month - 1)]

    url = f"https://www.britannica.com/on-this-day/{month}-{day}"

    result = requests.get(url)

    doc = BeautifulSoup(result.text, "html.parser")

    classes_to_find = ["card-body", "card-footer", ]
    elements = doc.find_all("div", class_=lambda class_: class_ in classes_to_find)


    with open("output.txt", "w") as file: 
        
        for element in elements:
            file.write(str(element.text))
