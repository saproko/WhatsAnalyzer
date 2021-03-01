# IDEAS
'''
IMPLEMENT
- Link count + häufigste Seiten
- Chat Startdatum

- cmd out in HTMl einbetten
- HTML verschönern
'''

from argparse import ArgumentParser
from reporter import Reporter
import os
from os import path


'''
Verfügbare Methoden in analyzer.py:
- user_msg_count
- total_msg_count
- user_avg_word_count
- chat_avg_msg_per_day
- user_most_common_words
- user_start_conversation
- user_most_common_emojis
- user_count_media

Verfügbare Methoden in plotter.py:
- plot_total_messages_over_time
- plot_group_messeges_by
- plot_user_vs_number_dict
'''


def pretty_print(result: dict) -> None:
    '''Gibt ein Dictionary wie {User Objekt: Wert} schöner aus'''
    try:
        for user, value in result.items():
            print(f"{user.username}: {value}")
    except Exception as e:
        print(
            f"Vermutlich falscher Datentyp für die pretty_print Funktion. ({str(e)})")
        print("Stattdessen wird das Ergebnis normal ausgegeben")
        print(result)


if __name__ == "__main__":
    parser = ArgumentParser("Tool zum Analysieren von WhatsApp Chats")
    parser.add_argument("chatname", help="Name der Chat Datei", type=str)
    args = parser.parse_args()

    chatname = args.chatname

    os.chdir(path.dirname(path.realpath(__file__)))

    reporter = Reporter(chatname)
    reporter.create_report()
