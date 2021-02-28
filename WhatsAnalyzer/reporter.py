from rich.console import Console
from rich.table import Table

from plotter import Plotter
from analyzer import Analyzer


class Reporter:
    def __init__(self, chatname):
        self._analyzer = Analyzer(chatname)
        self._plotter = Plotter(self._analyzer.manager.messages)
        self._chatname = chatname

    def create_report(self):
        self.export_graphs()
        self.create_html_report()
        self.cmd_out()

    def export_graphs(self) -> None:
        '''Erstellt und exportiert Graphen aus den Ergebnissen'''

        # Nachrichten gruppiert nach Stunde
        self._plotter.plot_group_messeges_by(
            "hour", export_path="plots/msg_by_hour.png")

        # Nachrichten gruppiert nach Wochentag
        self._plotter.plot_group_messeges_by(
            "weekday", export_path="plots/msg_by_weekday.png")

        # Nachrichtenverlauf (pro Woche)
        self._plotter.plot_total_messages_over_time(
            export_path="plots/msg_per_week.png")

        # Nachrichten pro Nutzer
        self._plotter.plot_user_vs_number_dict(self._analyzer.user_msg_count(),
                                               title="Nachrichten pro Nutzer",
                                               mode="pie",
                                               export_path="plots/msg_per_user.png")

        # Erste Nachricht des Tages Counter
        self._plotter.plot_user_vs_number_dict(self._analyzer.user_start_conversation(),
                                               title="Wie oft hat der Nutzer die Unterhaltung gestartet?",
                                               mode="pie",
                                               label_func=lambda s: f"{s}%",
                                               export_path="plots/conv_start.png")

        # Medien Anzahl pro Nutzer
        self._plotter.plot_user_vs_number_dict(self._analyzer.user_count_media(sum_only=True),
                                               title="Medienanzahl pro Nutzer\n(Bilder, Sticker, Sprachnachrichten...)",
                                               mode="pie",
                                               export_path="plots/media_per_user.png")

        # Durchschnittliche Wortanzahl pro Nachricht pro Nutzer
        self._plotter.plot_user_vs_number_dict(self._analyzer.user_avg_word_count(),
                                               title="Durchschnittliche Anzahl an Worten pro Nachricht",
                                               mode="bar",
                                               export_path="plots/msg_len_per_user.png")

    def cmd_out(self):
        '''Zeigt Ergebnisse in der Konsole an'''
        con = Console()

        def most_common_table(d):
            usernames = [obj.username for obj in d.keys()]
            tab = Table(show_header=True)

            tab.add_column("Platz", justify="center")
            for name in usernames:
                tab.add_column(name, justify="center")

            anzahl_plaetze = len(list(d.values())[0])  # Länge der Einträge

            for platz_nr in range(anzahl_plaetze):
                row = [str(platz_nr + 1)]  # erste beiden Spalten
                for user in d.keys():
                    data = d[user]
                    haeufigkeit = data[platz_nr][1]  # wie oft kommt es vor
                    element = data[platz_nr][0]  # z.B. Wort / Emoji
                    eintrag = f"\"{element}\"\n({str(haeufigkeit)} mal)"

                    if platz_nr != anzahl_plaetze - 1:  # alle außer letzter Durchgang
                        eintrag += "\n"

                    row.append(eintrag)
                tab.add_row(*row)
            con.print(tab)

        con.print(
            f"[bold magenta]Ergebnisse des Chats \"{self._chatname}\" mit den Nutzern {', '.join(self._analyzer.manager.usernames)}[bold magenta]")

        con.print("[green]Fakten zum Chat[/green]")
        chat_stats = Table(show_header=False)

        tot_msg_count = self._analyzer.total_msg_count()
        chat_stats.add_row("[red]Gesamtanzahl der Nachrichten[/red]",
                           str(tot_msg_count))

        chat_avg_msg_per_day = self._analyzer.chat_avg_msg_per_day()
        chat_stats.add_row("[red]Durchschnittliche Nachrichten pro Tag[/red]",
                           str(round(chat_avg_msg_per_day, 1)))

        con.print(chat_stats)
        print()  # newline

        con.print(
            "[green]Häufigste Wörter (Standardworte werden ausgeschlossen)[/green]")
        most_common_words = self._analyzer.user_most_common_words()
        most_common_table(most_common_words)
        print()

        con.print(
            "[green]Häufigste Emojis (als Text, da das Terminal keine Emojis anzeigen kann)[/green]")
        most_common_emojis = self._analyzer.user_most_common_emojis(
            as_text=True)
        most_common_table(most_common_emojis)
        print()

    def create_html_report(self):
        html_str = '''
<!DOCTYPE html>
<html>
  <head></head>

  <body>
    <h1 style="font-family: Trebuchet MS" id="title">WhatsApp Report</h1>
    <div>
      <img
        src="plots/msg_per_user.png"
        alt="msg_by_user"
        width="640"
        height="480"
      />

      <img
        src="plots/conv_start.png"
        alt="conv_start"
        width="640"
        height="480"
      />
    
      <img
        src="plots/media_per_user.png"
        alt="media_per_user"
        width="640"
        height="480"
      />
    </div>
    <div>
      <img
        src="plots/msg_by_hour.png"
        alt="msg_by_hour"
        width="640"
        height="480"
      />

      <img
        src="plots/msg_by_weekday.png"
        alt="msg_by_weekday"
        width="640"
        height="480"
      />
    </div>
    <div>
      <img
        src="plots/msg_per_week.png"
        alt="msg_per_week"
        width="640"
        height="480"
      />
    </div>
  </body>
</html>
'''
        with open("report.html", "w") as f:
            f.write(html_str)
