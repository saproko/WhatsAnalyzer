# -*- coding: utf-8 -*-

from collections import Counter
from collections.abc import Iterable
import emoji

from chatmanager import ChatManager


class Analyzer():
    def __init__(self, chatname: str) -> None:
        self._manager = ChatManager(chatname)

    @property
    def manager(self):
        return self._manager

    def _flatten(self, lst: list) -> list:
        '''Return die die Ursprungsliste nur mit einer Dimension
           (Unterlisten werden entfernt)'''
        for el in lst:
            if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
                yield from self._flatten(el)
            else:
                yield el

    def _get_percent(self, total: float, part: float):
        '''Return wie viel Prozent part von total ist'''
        return 100 / (total / part)

    def _get_most_common(self, lst: list, n: int) -> list:
        '''Return n häufigste Elemente in der Liste
           Returntype: [(element1, count1), (element2, count2)...]'''
        c = Counter(lst)
        return c.most_common(n)

    def user_msg_count(self) -> dict:
        '''Return Anzahl der Nachrichten für jeden Nutzer'''
        return {user: len(user.userrows) for user in self.manager.users}

    def total_msg_count(self) -> int:
        '''Return die Gesamtanzahl der Nachrichten im Chat'''
        return len(self.manager.messages)

    def user_all_words(self, include_stopwords=True) -> list:
        '''Return eine Liste mit allen Wörtern in jeder Nachricht für jeden Nutzer'''
        d = {}
        for user in self.manager.users:
            all_words = []
            # Nachrichten rausfiltern, die keine Wörter enthalten (z.B. Medien)
            word_rows = [msg for msg in user.userrows if msg.words is not None]
            # Entferne Datum / Name von jeder Nachricht
            for msg in word_rows:
                # Füge alle Worte aus allen Nachrichten zu all_words hinzu
                if include_stopwords:
                    all_words.extend(msg.words)
                else:
                    all_words.extend(msg.words_without_stopwords)
            d[user] = all_words
        return d

    def user_avg_word_count(self) -> dict:
        '''Return die durschnittliche Anzahl an Wörtern pro Nachricht für jeden Nutzer'''
        all_words = self.user_all_words()
        return {user: len(all_words[user]) / len(user.userrows)
                for user in self.manager.users}


    def chat_avg_msg_per_day(self) -> float:
        '''Return die durchschnittliche Anzahl an Nachrichten pro Tag in einem Chat'''
        content = self.manager.messages
        first_day = content[0].dateandtime
        last_day = content[-1].dateandtime
        deltadays = (last_day - first_day).days
        return self.total_msg_count() / deltadays

    def most_common_links(self, n: int = 5) -> dict:
        '''Return die n am häufigsten vorkommenden Websites'''
        all_sites = [url.netloc for msg in self._manager.messages for url in msg.links]
        # remove "www." prefix
        no_prefix = []
        for site in all_sites:
            prefix = "www."
            if site.startswith(prefix):
                no_prefix.append(site[len(prefix):])
            else:
                no_prefix.append(site)

        return self._get_most_common(no_prefix, n)

    def user_most_common_words(self, n: int = 5) -> dict:
        '''Return die n am häufigsten verwendeten Worte jedes Nutzers
           (Worte aus stopwords.py werden ignoriert)'''
        user_words = self.user_all_words(include_stopwords=False)
        return {user: self._get_most_common(user_words[user], n)
                for user in self.manager.users}

    def user_start_conversation(self) -> dict:
        '''Return den Anteil der Tage an denen der Nutzer
           die Unterhaltung gestartet hat (in Prozent) für jeden Nutzer'''
        d = {}
        for user in self.manager.users:
            start_counter = 0  # zählen, wie oft der Nutzer die Unterhaltung anfängt
            last_date = None
            for msg in self.manager.messages:
                # immer nur die erste Nachricht des Tages überprüfen
                date = msg.dateandtime.date()
                if date != last_date:
                    last_date = date
                    if msg.username == user.username:
                        start_counter += 1
            d[user] = start_counter  # absolute Zahlen, kein Prozent

        # Gesamtanzahl der Tage, an denen geschrieben wurde
        day_total = sum(d.values())
        for user in d:
            d[user] = self._get_percent(day_total, d[user])
        return d

    def user_most_common_emojis(self, n: int = 5, as_text: bool = False) -> dict:
        '''Return die n am häufigsten verwendeten Emojis jedes Nutzers'''
        d = {}

        for user in self.manager.users:
            user_emojis = [
                msg.emojitexts for msg in user.userrows if msg.emojitexts is not None]
            # Dimensionen auflösen
            if as_text:
                user_emojis = [emj.replace(":", "") for emj in self._flatten(user_emojis)]
            else:
                user_emojis = [emoji.emojize(emj)
                               for emj in self._flatten(user_emojis)]

            d[user] = self._get_most_common(user_emojis, n)

        return d

    def user_count_media(self, n: int = 5, sum_only = False):
        '''Return wie oft ein jeweiliges Medium verschickt wurde'''
        d = {}
        for user in self.manager.users:
            # Liste mit allen medien, die ein Nutzer versendet hat
            all_media = [msg.mediatype for msg in user.userrows
                         if msg.mediatype is not None]
            d[user] = self._get_most_common(all_media, n)
            if sum_only:
                media_sum = sum([tup[1] for tup in d[user]])
                d[user] = media_sum

        return d
