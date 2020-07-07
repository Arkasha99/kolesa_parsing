import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json

#get data from url
url_path = 'https://kolesa.kz/a/show/91654374'
page = requests.get(url_path)

#json
data={}


payload =
resp = requests.get('https://kolesa.kz/a/ajaxPhones/?id=91654374',cookies=page.cookies)
#connect Selenium for dynamic parsing
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "/usr/bin/chromium"
#your path to chromedriver.exe
#https://chromedriver.storage.googleapis.com/index.html?path=83.0.4103.39/
driver_path = 'C:/Users/NewUser/Downloads/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(driver_path)
driver.get(url_path)
phone_button = driver.find_element_by_css_selector('div.offer__show-phone.action-link.showPhonesLink.js__show-phones').click()

#extract data with bs4
soup = BeautifulSoup(page.content,'html.parser')
soup_phone = BeautifulSoup(driver.page_source,'html.parser')

#Описание
if (soup.find('h3',class_='offer__sub').find_next('div',{'class','text'})):
    description = soup.find('h3',class_='offer__sub').find_next('div',{'class','text'})
    data['description']=[]
    data['description'].append({
        'description':description.text
    })

#Пробег
if (soup.find('dt',{'class':'value-title','title':'Пробег'}).find_next('dd')):
    mileage = soup.find('dt',{'class':'value-title','title':'Пробег'}).find_next('dd')
    data['mileage']=[]
    data['mileage'].append({
        'mileage':mileage.text.strip()
    })

#Марка и модель
if (soup.find('span',{'itemprop':'brand'}) and soup.find('span',{'itemprop':'name'})):
    brand = soup.find('span',{'itemprop':'brand'})
    name = soup.find('span',{'itemprop':'name'})
    data['name']=[]
    data['name'].append({
        'brand':brand.text,
        'name':name.text
    })

#Год выпуска
if (soup.find('span',{'class','year'})):
    year = soup.find('span',{'class','year'})
    data['year']=[]
    data['year'].append({
        'year':year.text.strip()
    })

#Телефонные номера
if (soup_phone.find_all('li',{'class','offer__phone'})):
    phone = soup_phone.find_all('li',{'class','offer__phone'})
    data['phone']=[]
    for ph in phone:
        data['phone'].append({
            'number':ph.text
        })

#Изображения
if (soup.find_all('button',{'class':'gallery__main js__gallery-main'})):
    img_main = soup.find_all('button',{'class':'gallery__main js__gallery-main'})
    data['img']=[]
    for i in img_main:
        data['img'].append({
            'image':i['data-href']
        })
if (soup.find_all('button', {'class': 'gallery__thumb-image js__gallery-thumb'})):
    imgs = soup.find_all('button', {'class': 'gallery__thumb-image js__gallery-thumb'})
    for i in imgs:
        data['img'].append({
            'image': i['data-href']
        })

#handling JSON
with open('data.json','w',encoding='utf-8') as output:
    json.dump(data,output,ensure_ascii=False)
