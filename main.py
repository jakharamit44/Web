import pyrogram
from pyrogram import Client, filters
import os
import requests
from bs4 import BeautifulSoup

bot_token = os.environ.get("TOKEN", "5771926112:AAEBetnNf9hkNyUVCnHVMlgqMAsCItmYwdM")
api_hash = os.environ.get("HASH", "ad762fe0516f367115ba651d929cf429") 
api_id = os.environ.get("ID", "17737898")

app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  

def fetch(url):
    sess = requests.session()
    while 1:
        try:
            reqs = sess.get(url)
            print("Connected")
            break
        except: print("Retrying")

    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    for link in soup.find_all('a'): 
        tmp = link.get('href')
        if tmp is not None and "view_video" in tmp:
            if "https://" not in tmp:
                ttmp = "https://" + url.split("/")[2] + tmp
            else: ttmp = tmp
            if ttmp not in urls: urls.append(ttmp)
    return urls

@app.on_message(filters.text)
def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    msg = message.reply_text("Fetching...")
    res = fetch(message.text)
    # final = []
    # tmp = ""
    # for ele in res:
    #     tmp += ele + "\n\n"
    #     if len(tmp) > 3950:
    #         final.append(tmp)
    #         tmp = ""
    # final.append(tmp)
    print(len(res))
    msg.delete()
    for ele in res:
        message.reply_text(ele, disable_web_page_preview=True)
        # time.sleep(1)

app.run()
