import os 
import smtplib
import requests
from email.message import EmailMessage
from generate_report import create_analytics_report
from datetime import datetime, timedelta

dog_info = requests.get('https://api.thedogapi.com/v1/images/search').json()[0]
dog_url = dog_info['url']

EMAIL_ADDRESS = os.environ.get('EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
print(EMAIL_ADDRESS)
print(EMAIL_PASSWORD)
msg = EmailMessage()
msg['Subject'] = "Covid analytucs report (with a cute doggie)"
msg['From'] = EMAIL_ADDRESS
msg['To'] = ['juangrajales618@gmail.com']

msg.set_content('Attached is the analytics report from yesterday')
msg.add_alternative(f'Guau!\n<img src="{dog_url}" width="300px">', subtype='html')
#yesterday = (datetime.today() - timedelta(days=1)).strftime("%m/%d/%y").replace("/0","/").lstrip("0")
yesterday = "10/10/20" # Uncomment line for testing
create_analytics_report(yesterday, filename="tmp/report.pdf")

with open("tmp/report.pdf", "rb") as f:
    data = f.read()
    
msg.add_attachment(data, filename="report.pdf", maintype="application/pdf", subtype="pdf")
 
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
    