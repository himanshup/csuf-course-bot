# Coursebot

Simple Facebook Messenger bot that checks the status of classes at Cal State Fullerton.  

Option to subscribe to a class number and schedule emails/text for when they are available will be implemented soon.

## Usage

Send the subject and course number (e.g. `CPSC 120`) to the bot and it will reply with all the classes and the status/available seats for each class.

## Run locally

```
git clone https://github.com/himanshup/coursebot.git
cd coursebot
pip install -r requirements.txt
```

Create a Facebook acount If you don't already have one and then [create a Facebook app](https://developers.facebook.com/docs/messenger-platform/getting-started/quick-start/)


Create a .env file in the root of the project directory and add your access and verify token:
```
ACCESS_TOKEN=''
VERIFY_TOKEN=''
```

Set up a [ngrok](https://ngrok.com/) server as a proxy (localhost URL won't work for Facebook Messenger bots).  

Run `python app.py` in one terminal and `ngrok http 3000` in another (both in the directory of the project).  

Add the web interface URL as a callback URl for your Facebook app and your bot should work.

## Files

`scrape.py` contains a function that scrapes CSUF's course catalog and returns course info.  

You will need to add CHROMEDRIVER_PATH to your .env file (google CHROMEDRIVER_PATH to get your path):

  ```
  CHROMEDRIVER_PATH=''
  ```
  
