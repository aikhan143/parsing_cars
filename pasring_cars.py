# Код Аяны
import requests
from bs4 import BeautifulSoup
import csv

def write_csv(data):
    with open('cars.csv', 'a', newline='') as cars:
        writer = csv.writer(cars)
        writer.writerow((data['title'], data['price'], data['description'], data['photo']))

def get_html(url):
    response = requests.get(url)
    return response.text

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    cars = soup.find('div', class_='catalog-list').find_all('a', class_='catalog-list-item')
    
    for car in cars:
        try:
            title = car.find('span', class_='catalog-item-caption').text.strip()
        except:
            title = ''
        
        try:
            price = car.find('span', class_='catalog-item-price').text
        except:
            price = ''

        try:
            photo = car.find('img').get('src')
        except:
            photo = ''

        try:
            description = car.find('span', class_='catalog-item-descr').text.split()
            description = ' '.join(description)
        except:
            description = ''

        data = {'title': title, 'price': price, 'description': description, 'photo': photo}
        write_csv(data)


def get_page(html):
    soup = BeautifulSoup(html, 'lxml')
    page_list = soup.find('div', class_="pages fl").find_all('a')
    last_page = page_list[-2].text
    return int(last_page)
    
        
def main():
    url = 'https://cars.kg/offers'
    html = get_html(url)

    number = get_page(html)
    i = 1

    while i <= number:
        url = url + '/' + i
        html = get_html(url)
        get_data(html)

        if i == number:
            number = get_page(html)

        i += 1
        
        
main()