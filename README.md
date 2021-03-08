# WhatsAnalyzer

**Analyze and visualize your WhatsApp Chats!**

With this program you can get insight into all your WhatsApp chats, including group chats!

## Features

* Average messages per day
* User message count + total message count
* Conversation start count per user (how often did someone write the first message of the day)
* Average words per message per user
* Messages per weekday / hour
* Most common words per user (excluding common german words, see globals_.py)
* Most common Emojis per user
* Media count
* Link count
* HTML report with plots + display in Terminal

## Usage

1. Install Python 3.6+ if you haven't already
2. Install the required libraries
   `pip install -r requirements.txt`
3. Export the WhatsApp chat and put it into a folder named "chats". If you do not create this folder the program will do it for you.
4. Run main.py in command prompt
   `cd WhatsAnalyzer`  
   `python whatsanalyzer.py<chatfilename>`

## Limitations

I have initially written the program for my personal use. Therefore, most texts are in german at the moment. Furthermore, the date format at the beginning of each line (which is necessery for message detection) will probably vary from region to region. If you have problems, please contact me, as I intend to improve compatibility in the future.

Since this is my first repository on GitHub, please excuse if not anything is perfect. If you have feedback, please contact me.

E-Mail: saproko17@gmail.com
