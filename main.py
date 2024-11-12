import requests
import bs4
import sys
import pandas
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
load_dotenv()

# URL you want to access
search=input('Enter a product name to search :')
mail=input("enter mail id : ")
min=int(input('enter min price range to filter:'))
max=int(input('enter max price range to filter:'))

url = f"https://www.flipkart.com/search?q={search}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off"
ab={'price':[],'product name':[]}
# Custom headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.64",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1"
}

#headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "https://www.flipkart.com/", "DNT": "1","Connection": "keep-alive" }


# Set a timeout (e.g., 10 seconds)
try:
    response = requests.get(url, headers=headers, timeout=10)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request was successful!")
        print("Response Text:")
        #print(response.content)
        soup=bs4.BeautifulSoup(response.content,'html.parser')
        price=soup.find_all('div',class_='KzDlHZ')
        for i,j in enumerate(soup.find_all('div',class_='Nx9bqj _4b5DiR')):
            print(j.get_text().encode('utf-8').decode(sys.stdout.encoding))
            t=int(j.get_text().encode('utf-8').decode(sys.stdout.encoding).replace('₹'.encode('utf-8').decode(sys.stdout.encoding),'').replace(',',''))
            if t>=min and t<=max:
                ab['price'].append(j.get_text().encode('utf-8').decode(sys.stdout.encoding))
                ab['product name'].append(price[i].get_text())
    else:
        print(f"Failed to access {url}. Status code: {response.status_code}")
except requests.exceptions.Timeout:
    print("The request timed out.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
print(ab)
df=pandas.DataFrame(ab)
df.to_excel('filter.xlsx')


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Sender and receiver email addresses
sender_email = os.getenv('SENDER_EMAIL')
receiver_email = mail
password = os.getenv('SENDER_EMAIL_PASSWORD')  # Use app password if 2FA is enabled

# SMTP server details for Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587  # Use 465 for SSL, 587 for TLS

# Create the message
message = MIMEMultipart()
message['From'] =os.getenv('SENDER_EMAIL')
message['To'] = mail
message['Subject'] = "Search product filter result in excel"
try:
    with open('filter.xlsx', "rb") as attachment:
        # Create a MIMEBase object to handle the attachment
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())  # Read the content of the file
        encoders.encode_base64(part)  # Encode the file in base64
        
        # Add the file as an attachment to the email
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename('filter.xlsx')}'
        )
        
        # Attach the file to the email message
        message.attach(part)

except Exception as e:
    print(f"Failed to attach file: {e}")
# Email body
body = "Hello, this is a test email sent from Python using smtplib!"

# Send the email using SMTP
try:
    # Establish a secure connection with the Gmail SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Start TLS encryption

    # Login to the SMTP server
    server.login(sender_email, password)

    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")

except Exception as e:
    print(f"Failed to send email: {e}")

finally:
    # Close the server connection
    server.quit()