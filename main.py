import pyrogram
from pyrogram import Client, filters
import os
import requests
from bs4 import BeautifulSoup

def fetch(url):
    sess = requests.session()
    while 1:
        try:
            reqs = sess.get(url)
            break
        except: print("Retrying")

    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    for link in soup.find_all('a'): 
        tmp = link.get('href')
        if tmp is not None and "view_video" in tmp:
            urls.append("https://" + url.split("/")[2] +tmp)
    return urls

bot_token = os.environ.get("TOKEN", "")
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  

@app.on_message(filters.text)
def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    msg = message.reply_text("Fetching...")
    res = fetch(message.text)
    final = []
    tmp = ""
    for ele in res:
        tmp += ele + "\n"
        if len(tmp) > 3950:
            final.append(tmp)
            tmp = ""
    final.append(tmp)
    msg.delete()
    for msg in final:
        message.reply_text(msg, disable_web_page_preview=True)

app.run()