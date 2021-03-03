# -*- coding: utf-8 -*-

from message import Message
from user import User
import globals_
import re
from os import path
import os
import sys


class ChatManager():
    def __init__(self, chatname: str, ) -> None:
        self._chatname = chatname
        self._os = self._init_os()
        self._messages = self._init_messages()
        self._usernames = self._init_usernames()
        self._users = self._init_users()

    @property
    def os(self) -> str:
        return self._os

    @property
    def users(self) -> list:
        return self._users

    @property
    def messages(self) -> list:
        return self._messages

    @property
    def usernames(self) -> list:
        return self._usernames

    def _read_chat(self) -> list:
        '''Return alle Zeilen der Chatdatei als Liste
           remove_multiliners: wenn True werden Zeilen, die nicht mit Datumstempel starten entfernt'''

        # falls nur der Dateiname ohne ".txt" angegeben wurde, füge es hinzu
        if not self._chatname.endswith(".txt"):
            self._chatname += ".txt"

        try:
            project_basedir = path.dirname(os.getcwd())  # Projekt Root
            filepath = f"{project_basedir}/chats/{self._chatname}"
            with open(filepath, "r", encoding="utf-8") as f:
                # Inhalt der Chatdatei lesen, LTR Mark entfernen, erste Line (WA Info) entfernen
                content = f.read().replace(u"\u200e", "").splitlines()[1:]
            return content
        except FileNotFoundError:
            print(f"Die Datei {filepath} wurde nicht gefunden.\nSchau nach, ob sich die Datei wirklich im 'chats' Ordner befindet und ob du den Namen richtig geschrieben hast.")
            print("Aktuelles Verzeichnis:", os.getcwd())
            sys.exit()

    def _init_messages(self):
        content = self._read_chat()
        message_strings = []

        # Nachrichten zusammenfügen, die über mehrere Zeilen gehen
        date_pattern = getattr(globals_, f"DATEPATTERN_{self.os}")
        for line in content:
            if re.match(date_pattern, line) is not None:
                message_strings.append(line)
            else:
                message_strings[-1] += f" {line}"

        # Message Objekte erstellen und fehlgeschlagene Messages rausfiltern
        message_objects = [Message(msg, self.os)
                           for msg in message_strings]
        message_objects = [msg for msg in message_objects
                           if msg.username is not None]

        return message_objects

    def _init_usernames(self) -> list:
        '''Return Liste mit allen individuellen Nutzernamen im Chat'''
        allnames = set([msg.username for msg in self._messages])
        return list(allnames)

    def _init_users(self) -> list:
        '''Return Liste mit User Objekten aller Nutzer'''
        userlist = []
        for current_username in self._usernames:
            userrows = [msg for msg in self.messages
                        if msg.username == current_username]
            userlist.append(User(current_username, userrows))

        return sorted(userlist)

    def _init_os(self) -> str:
        '''Return Name des Betriebssystems ("ios" oder "android")'''
        first_line = self._read_chat()[0]

        if re.match(globals_.DATEPATTERN_IOS, first_line) is not None:
            return "IOS"

        elif re.match(globals_.DATEPATTERN_ANDROID, first_line) is not None:
            return "ANDROID"

        else:
            raise Exception(
                "Die Chatdatei kann keinem Muster zugeordnet werden")
