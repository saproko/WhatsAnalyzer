# -*- coding: utf-8 -*-

class User():
    def __init__(self, username: str, userrows: list) -> None:
        self._username = username  # Chatname des Nutzers
        self._userrows = userrows  # nur die Zeilen, in denen der Nutzer etwas schreibt

    @property
    def userrows(self) -> list:
        return self._userrows

    @property
    def username(self) -> str:
        return self._username

    def __lt__(self, other):
        return self.username < other.username
