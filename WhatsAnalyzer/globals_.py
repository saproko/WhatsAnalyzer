# -*- coding: utf-8 -*-

DATEPATTERN_IOS = r"^\[\d\d\.\d\d\.\d\d,\s\d\d:\d\d:\d\d\]"
DATEPATTERN_ANDROID = r"\d\d\.\d\d\.\d\d,\s\d\d:\d\d"

DATEPARSE_IOS = "[%d.%m.%y, %H:%M:%S]"
DATEPARSE_ANDROID = "%d.%m.%y, %H:%M"

MSG_PATTERN = (r"^(?P<prefix>(?P<dateandtime>(?:\[)?\d\d\.\d\d\.\d\d,\s\d\d:\d\d(?::\d\d\])?)"  # dateandtime
               r"\s(?:-\s)?(?P<username>.+?):\s?)"  # username und Ende des Prefix
               r"(?:(?:<?|[^\w\d])(?P<media>\w+)\s(?:ausgeschlossen|weggelassen)>?$)?"  # media
               r"(?P<body>.*)")  # body


# https://github.com/PetengDedet/WhatsApp-Analyzer/blob/master/stop-words/german.txt
# https://www.pc-erfahrung.de/nebenrubriken/sonstiges/webdesignwebentwicklung/stoppwortliste.html

STOPWORDS = ['hab', 'wollte', 'daß', 'dort', 'zwar', 'genau', 'gewesen', 'dafür', 'einiges', 'welchem', 'möchte', 'ihr', 'dieser', 'siehe', 'macht', 'hier', 'viel', 'bist', 'könnte', 'deinem', 'überhaupt', 'so', 'das', 'gerne', 'bleiben', 'wirklich', 'welche', 'jedem', 'durch', 'auch', 'vor', 'meine', 'finde', 'anderem', 'worden', 'ansonsten', 'sicherlich', 'einmal', 'sonst', 'd.h', 'wollen', 'einigen', 'mal', 'geht', 'bestimmte', 'dies', 'unter', 'möglichst', 'wo', 'ok',
             'bereits', 'am', 'können', 'weiteren', 'beide', 'entweder', 'beispielsweise', 'halt', 'sie', 'eure', 'hierbei', 'deren', 'anfangs', 'neue', 'gilt', 'bekommen', 'mehr', 'wenn', 'völlig', 'diesem', 'kommt', 'eigentlich', 'daraus', 'deine', 'wesentlich', 'bzw', 'diese', 'darüber', 'dem', 'momentan', 'andern', 'ein', 'nach', 'ihre', 'wird', 'hin', 'auf', 'nachdem', 'manche', 'einiger', 'ist', 'anderen', 'aller', 'jetzt', 'z.b', 'allen', 'indem', 'ganz', 'hierfür',
             'weil', 'andere', 'zum', 'solche', 'jenes', 'von', 'was', 'manches', 'ohne', 'letztere', 'deines', 'jede', 'deiner', 'diesen', 'hatte', 'statt', 'und', 'außerdem', 'wiederum', 'denselben', 'i', 'anders', 'einem', 'gibt', 'leider', 'usw', 'dich', 'folgender', 'nicht', 's', 'eines', 'welches', 'nämlich', 'erstmals', 'dieselbe', 'seine', 'ne', 'schon', 'den', 'besteht', 'weg', 'obwohl', 'vielen', 'nein', 'weiterer', 'sondern', 'dessen', 'andernfalls', 'sehr', 'ander',
             'musste', 'wie', 'habe', 'sollten', 'derselben', 'ich', 'wieder', 'welcher', 'folgendem', 'gegen', 'wichtige', 'gut', 'unseren', 'jenen', 'eures', 'war', 'hinzu', 'an', 'keinen', 'zur', 'anstatt', 'werde', 'darf', 'jeweils', 'ja', 'zuvor', 'soll', 'hat', 'einen', 'oder', 'allem', 'keine', 'gleichzeitig', 'ab', 'gleichen', 'keines', 'viele', 'immer', 'jeweilige', 'genannten', 'sobald', 'eine', 'müssen', 'heute', 'zwischen', 'jemand', 'folgenden', 'anderes',
             'folgende', 'für', 'konnte', 'ihres', 'solches', 'entscheidend', 'ihrem', 'der', 'aber', 'dabei', 'sind', 'wurden', 'unserem', 'einfach', 'dass', 'insgesamt', 'lediglich', 'einige', 'h', 'etwas', 'sein', 'will', 'einer', 'daran', 'weiter', 'c', 'jener', 'wobei', 'sowohl', 'bestimmter', 'weiterhin', 'zuerst', 'bringen', 'desselben', 'sprich', 'darauf', 'zusätzlich', 'ihnen', 'nächsten', 'einzelnen', 'unsere', 'also', 'jedoch', 'per', 'dieselben', 'besonders',
             'sich', 'sofern', 'jedes', 'mehrere', 'solcher', 'einig', 'muss', 'davon', 'dieses', 'nichts', 'mit', 'hinter', 'letzteres', 'weiteres', 'eurer', 'aus', 'richtig', 'ebenfalls', 'während', 'seiner', 'unseres', 'darstellt', 'wäre', 'ins', 'immerhin', 'hätte', 'zu', 'nahezu', 'waren', 'jenem', 'dar', 'danach', 'kann', 'hast', 'seinem', 'mache', 'bevor', 'neuen', 'damit', 'die', 'hatten', 'mancher', 'lässt', 'nur', 'andersherum', 'wirst', 'es', 'daher', 'alle',
             'keinem', 'sollen', 'würde', 'bietet', 'denen', 'werden', 'würden', 'aufgrund', 'mich', 'meines', 'desto', 'ihn', 'anhand', 'dasselbe', 'eurem', 'bei', 'sorgt', 'folgt', 'her', 'derer', 'hingegen', 'meinen', 'solchen', 'allerdings', 'anderm', 'bringt', 'gleich', 'doch', 'natürlich', 'man', 'ihrer', 'eher', 'lautet', 'möglich', 'da', 'beim', 'meiner', 'anderer', 'ziemlich', 'konnten', 'morgen', 'dann', 'manchen', 'irgendwie', 'deinen', 'hauptsächlich', 'vorher',
             'um', 'sagen', 'wichtigsten', 'wurde', 'mittels', 'genannte', 'über', 'hoch', 'als', 'je', 'scheint', 'meisten', 'befindet', 'anschließend', 'derselbe', 'gerade', 'euer', 'im', 'ihm', 'welchen', 'demselben', 'in', 'vom', 'denn', 'noch', 'oftmals', 'gar', 'gesagt', 'lassen', 'trotz', 'warum', 'sämtliche', 'du', 'wei', 'euren', 'somit', 'selbst', 'warst', 'kein', 'bsp', 'mein', 'jeder', 'bis', 'dazu', 'glaube', 'wir', 'haben', 'jene', 'weitere', 'heutigen', 'mir',
             'vorerst', 'unser', 'keiner', 'etc', 'jo', 'nun', 'meinem', 'demzufolge', 'gehen', 'gemacht', 'zwecks', 'uns', 'wer', 'alles', 'einigem', 'solchem', 'seinen', 'folgendes', 'ob', 'er', 'seines', 'dein', 'bin', 'jeweiligen', 'des', 'unserer', 'machen', 'hält', 'dir', 'letztendlich', 'sowie', 'manchem', 'sollte', 'bestimmten', 'kam', 'liegt', 'später', 'euch', 'ihren', 'habt', 'mithilfe', 'eigenen', 'jeden', 'kommen']
