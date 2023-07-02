from pyrogram import Client, filters
from bs4 import BeautifulSoup
import requests

# Set up the Pyrogram client
api_id = 17737898  # Replace with your own API ID
api_hash = "ad762fe0516f367115ba651d929cf429"  # Replace with your own API hash
bot_token = "5771926112:AAEBetnNf9hkNyUVCnHVMlgqMAsCItmYwdM"  # Replace with your own bot token

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define the handler function to process incoming messages
@app.on_message(filters.private)
def handle_message(client, message):
    # Extract the URL from the message
    url = message.text

    # Send an HTTP GET request to fetch the webpage content
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the download link in the HTML
        download_link = soup.find("a", href=True)["href"]

        # Send the download link as a reply
        client.send_message(message.chat.id, download_link)
    else:
        client.send_message(message.chat.id, "Failed to fetch the webpage.")

# Start the bot
if __name__ == "__main__":
    app.run()
