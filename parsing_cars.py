import requests
from bs4 import BeautifulSoup
import csv

def write_csv(data):
    with open('cars.csv', 'a') as cars:
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

with open('cars.csv', 'w', newline='') as cars:
    writer = csv.writer(cars)
    writer.writerow(['title', 'price', 'description', 'photo'])

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    next_button = soup.find('div', class_="pages fl").find_all('a')[-1].text[:5]
    current_page = 1
    if next_button == 'Далее':
        current_page += 1
        return current_page
    else:
        return 0
        
def main():
    url = 'https://cars.kg/offers'
    html = get_html(url)
    total_pages = get_total_pages(html)
    
    for page in range(1, total_pages + 1):
        page_url = f'{url}/{page}'
        print(page_url)
        page_html = get_html(page_url)
        get_data(page_html)

main()