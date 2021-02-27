# WhatsAnalyzer

**Analyze and visualize your WhatsApp Chats!**

With this program you can get insight into all your WhatsApp chats, including group chats!

## Current features

* User message count + total message count
* Average words per message per user
* Average messages per day
* Most common words per user (excluding common german words, see globals_.py)
* Most common Emojis per user
* Conversation start count per user (how often did someone write the first message of the day)
* Media counter
* HTML report with plots + display in Terminal

## Usage

1. Export the WhatsApp chat and put it into a folder named "chats". If you do not create this folder the program will do it for you.
2. Install the required libraries
   `pip install -r requirements.txt`
3. Run main.py in command prompt
   `python main.py <chatfilename>`

## Limitations

I have written the program for my personal use. Therefore, most comments are in german at the moment. Furthermore, I suppose the date format at the beginning of each line (which is necessery for message detection) will vary from region to region. If you have problems, please contact me as I intend to improve compatibility in the future.

Since this is my first repository on GitHub, please excuse if not anything is perfect. If you have feedback, please contact me.
