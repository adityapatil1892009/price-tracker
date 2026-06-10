import requests
import smtplib
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(os.environ["SENDER"],os.environ["PASSWORD"])


headers = {
    "User-Agent": "Mozilla/5.0"
}
link = "https://buyhatke.com/amazon-lost-generation-we-have-everything-still-empty-price-in-india-63-113208718"
response = requests.get(link,headers=headers)
response.encoding = "utf-8"

soup = BeautifulSoup(response.text,"html.parser")
price_tag = soup.find(
    "span",
    class_="text-2xl md:text-3xl font-bold"
)

if price_tag is None:
    print("Price element not found!")
    print(response.text[:2000])
    exit()

price = int(
    price_tag.get_text(strip=True)
    .replace("₹", "")
    .replace(",", "")
)
print("Price:", price)
print("SENDER:", os.environ.get("SENDER"))
print("RECEIVER:", os.environ.get("RECEIVER"))
print("About to send email...")
if price > 100:
    message = f"Subject:Price down alert!!\n\nThe price of the book named as 'Lost Generation' is dropped to {price}\nProduct link -- {link}"

    result = server.sendmail(
        from_addr=os.environ["SENDER"],
        to_addrs=os.environ["RECEIVER"],
        msg=message
    )
    result = server.sendmail(
    from_addr=os.environ["SENDER"],
    to_addrs=os.environ["RECEIVER"],
    msg=message
)

print("sendmail returned:", result)
print("Email sent!")
server.quit()


