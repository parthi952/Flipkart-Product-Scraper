import requests
import bs4
import sys
import os
from excelfileconvertion import ConvertExcel
from emailsend import SendMail
from dotenv import load_dotenv
load_dotenv()


search=input('Enter a product name to search :')
while search!='quit':
    mail=input("enter mail id : ")
    min=int(input('enter min price range to filter:'))
    max=int(input('enter max price range to filter:'))

    url = f"https://www.flipkart.com/search?q={search}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off"
    filtered_product_dict={'price':[],'product name':[]}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.64",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1"
    }

    #headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "https://www.flipkart.com/", "DNT": "1","Connection": "keep-alive" }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup=bs4.BeautifulSoup(response.content,'html.parser')
            product=soup.find_all('div',class_='KzDlHZ')
            for i,j in enumerate(soup.find_all('div',class_='Nx9bqj _4b5DiR')):
                price=int(j.get_text().encode('utf-8').decode(sys.stdout.encoding).replace('₹'.encode('utf-8').decode(sys.stdout.encoding),'').replace(',',''))
                if price>=min and price<=max:
                    filtered_product_dict['price'].append(j.get_text().encode('utf-8').decode(sys.stdout.encoding))
                    filtered_product_dict['product name'].append(product[i].get_text())
        else:
            print(f"Failed to access {url}. Status code: {response.status_code}")
    except Exception as e:
        print(e)

    print(filtered_product_dict)
    if filtered_product_dict['price'] and filtered_product_dict['product name']:
        xlsx_file_name=search+'_filtered_products.xlsx'
        if ConvertExcel(filtered_product_dict,xlsx_file_name):
            print('waiting to send email...')
            response=SendMail(os.getenv('SENDER_EMAIL'),mail,os.getenv('SENDER_EMAIL_PASSWORD'),f"{search} Filtered Products In Excel Format",xlsx_file_name)
            print(response)
        else:
            print('Convert To Excel Was Failed')
    

    search=input('Enter a product name to search :')

