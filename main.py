import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json
import smtplib
from email.mime.text import MIMEText

# load .env (for development only)
load_dotenv()

# all env
SITE_URL = os.getenv("SITE_URL")
SENDER_EMAIL = os.getenv("SENDER_GMAIL_ADDRESS")
RECEIVER_EMAIL = os.getenv("RECEIVER_GMAIL_ADDRESS")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def sendMail(type="msg"):
    
    if type == "err":
        message = """Required env variables are missing for the web scrapper bot, please add the required variables in the Github Actions secret."""
    else:
        message = f"""📢 New Hostel Notice\n\nDate: {date}\n\nTitle: {notice}\n\nLink: {link}\n\n\n\nBy- web scrapper bot"""
    msg = MIMEText(message)
    
    msg["Subject"] = "Action required - web scrapper bot" if type == "err" else "Notice Updated - web scrapper bot"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL or SENDER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, PASSWORD)
        smtp.send_message(msg)

# check if env data is provided
if not all([SITE_URL, SENDER_EMAIL, PASSWORD]):
    # send error alert
    sendMail("err")
    raise ValueError("env variables are missing")
    
# getting res from website
res = requests.get(SITE_URL)
soup = BeautifulSoup(res.content, "html.parser")

# get desired data by selecting element
table_row = soup.find_all("tr")
content = table_row[1].find_all("td") 
# data formatting   
date = content[0].text.strip()
notice= content[1].text.strip()
link = content[2].find("a").get("href").strip()

# check for changes and update json file  
with open("notice.json", "r") as f:
    stored_data = json.load(f)

# update notice.json
if (date != stored_data["date"] or notice != stored_data["notice"]):
    stored_data["date"] = date
    stored_data["notice"] = notice
    stored_data["link"] = link

    with open("notice.json", "w") as f:
        json.dump(stored_data, f, indent=4)

    # automated message alert 
    sendMail()