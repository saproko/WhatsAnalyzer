import re
from datetime import datetime
import emoji
import globals_


class Message:
    def __init__(self, msg: list, os: str) -> None:
        self._msg = msg
        self._os = os
        self._stopwords = globals_.STOPWORDS
        self._username = self._init_username()
        self._dateandtime = self._init_dateandtime()
        self._body = self._init_body()
        self._mediatype = self._init_mediatype()
        self._words = self._init_words()
        self._words_without_stopwords = self._init_words(
            without_stopwords=True)
        self._emojitexts = self._init_emojitexts()

    def _init_username(self) -> str:
        # passende Variable für
        name_pattern = getattr(globals_, f"CAPTURE_NAME_PATTERN_{self.os}")
        match = re.match(name_pattern, self.msg)
        if match is not None:
            return match.group(1)
        else:
            return None

    def _init_dateandtime(self) -> datetime:
        date_pattern = getattr(globals_, f"DATEPATTERN_{self.os}")
        dateparse_pattern = getattr(globals_, f"DATEPARSE_{self.os}")

        datestring = re.match(date_pattern, self.msg)
        return datetime.strptime(datestring.group(0), dateparse_pattern)

    def _init_mediatype(self) -> str:
        media_pattern = getattr(globals_, f"CAPTURE_MEDIA_PATTERN_{self.os}")
        media_match = re.match(media_pattern, self.msg)
        if media_match is not None:
            return media_match.group(1)
        else:
            return None

    def _init_body(self) -> str:
        prefix_pattern = getattr(globals_, f"PREFIX_PATTERN_{self.os}")
        return re.sub(prefix_pattern, "", self.msg)

    def _init_words(self, without_stopwords=False) -> list:
        if self.mediatype is None and self.username is not None:
            blacklist_pattern = r"[^A-Za-zäöü\s]"
            charonly_msg = re.sub(blacklist_pattern, "", self.body)
            if without_stopwords:
                return [w.lower() for w in charonly_msg.split(" ")
                        if w != "" and w != " " and w.lower() not in self.stopwords]
            else:
                return [w.lower() for w in charonly_msg.split(" ")
                        if w != "" and w != " "]
        else:
            return None

    def _init_emojitexts(self):
        strange_pattern = r"[a-zA-Z0-9\.,:!?\s]"
        strange_signs_only = re.sub(strange_pattern, "", self.body)
        demojized = emoji.demojize(strange_signs_only)
        emoji_pattern = r":[a-z_]+:"
        emojitexts = re.findall(emoji_pattern, demojized)
        if len(emojitexts) > 0:
            return emojitexts
        else:
            return None

    @property
    def username(self) -> str:
        '''Return Nuternamen des Verfassers der Nachricht falls vorhanden,
           sonst None'''
        return self._username

    @property
    def dateandtime(self) -> datetime:
        '''Return datetime Objekt von der Zeit des Absendens'''
        return self._dateandtime

    @property
    def body(self) -> str:
        '''Return den Inhalt der Nachricht'''
        return self._body

    @property
    def words(self) -> list:
        '''Return Liste mit allen Wörtern der Nachricht falls vorhanden, sonst None'''
        return self._words

    @property
    def words_without_stopwords(self) -> list:
        '''Return Liste mit allen Wörtern der Nachricht (stopwords ausgenommen) falls vorhanden,
           sonst None'''
        return self._words_without_stopwords

    @property
    def mediatype(self) -> str:
        '''Return None wenn die Nachricht kein Medium darstellt,
           sonst Name des Mediums als String'''
        return self._mediatype

    @property
    def msg(self) -> str:
        '''Return die gesamte Nachrichtenzeile'''
        return self._msg

    @property
    def emojitexts(self):
        return self._emojitexts

    @property
    def os(self) -> str:
        '''Return Betriebssystem als String'''
        return self._os

    @property
    def stopwords(self) -> set:
        '''Return Liste mit Worten, die beim Wortzählen ignoriert werden'''
        return self._stopwords

    @property
    def dictionary(self):
        return self.__dict__
