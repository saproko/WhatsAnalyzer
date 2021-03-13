# -*- coding: utf-8 -*-

from rich.console import Console
from rich.table import Table
import os
from os import path

from plotter import Plotter
from analyzer import Analyzer


class Reporter:
    def __init__(self, chatname):
        self._analyzer = Analyzer(chatname)
        self._plotter = Plotter(self._analyzer.manager.messages)
        self._chatname = chatname

        self._chatname_base = path.splitext(
            self._chatname)[0].lower()  # Dateiname ohne ".txt"
        self._project_basedir = path.dirname(os.getcwd())  # Projekt Root
        self._chat_plot_dir = path.join(
            self._project_basedir, "plots", self._chatname_base)  # Plotordner für den chat
        self._rel_chat_plot_dir = fr"\{path.relpath(self._chat_plot_dir, self._project_basedir)}"


    def folder_setup(self):
        '''Erstellt die benötigten Ordner'''
        if not path.exists(f"{self._project_basedir}/chats"):
            os.makedirs(f"{self._project_basedir}/chats")
            print("Chatordner erstellt")

        if not path.exists(f"{self._project_basedir}/plots"):
            os.makedirs(f"{self._project_basedir}/plots")
            print("Plotordner erstellt")

        if not path.exists(self._chat_plot_dir):
            os.makedirs(self._chat_plot_dir)
            print("Chatspeziefischer Plotordner erstellt")

        if not path.exists(f"{self._project_basedir}/reports"):
            os.makedirs(f"{self._project_basedir}/reports")
            print("Reportordner erstellt")

    def create_report(self):
        self.folder_setup()
        self.export_graphs()
        self.create_html_report()
        self.cmd_out()

    def export_graphs(self) -> None:
        '''Erstellt und exportiert Graphen aus den Ergebnissen'''

        # Nachrichtenverlauf pro Nutzer
        self._plotter.plot_user_messages_over_time(
            title=None,
            export_path=f"{self._chat_plot_dir}/msg_per_person_per_week.png")

        # Nachrichten gruppiert nach Stunde
        self._plotter.plot_group_messeges_by(
            "hour", export_path=f"{self._chat_plot_dir}/msg_by_hour.png")

        # Nachrichten gruppiert nach Wochentag
        self._plotter.plot_group_messeges_by(
            "weekday", export_path=f"{self._chat_plot_dir}/msg_by_weekday.png")

        # Nachrichtenverlauf (pro Woche)
        self._plotter.plot_total_messages_over_time(
            title=None,
            export_path=f"{self._chat_plot_dir}/msg_per_week.png")

        # Nachrichten pro Nutzer
        self._plotter.plot_user_vs_number_dict(self._analyzer.user_msg_count(),
                                               title=None,
                                               mode="pie",
                                               export_path=f"{self._chat_plot_dir}/msg_per_user.png")

        # Erste Nachricht des Tages Counter
        self._plotter.plot_user_vs_number_dict(self._analyzer.user_start_conversation(),
                                               title=None,
                                               mode="pie",
                                               label_func=lambda s: f"{s}%",
                                               export_path=f"{self._chat_plot_dir}/conv_start.png")

        # Medien Anzahl pro Nutzer
        self._plotter.plot_user_vs_number_dict(self._analyzer.user_count_media(sum_only=True),
                                               title=None,
                                               mode="pie",
                                               export_path=f"{self._chat_plot_dir}/media_per_user.png")

        # Durchschnittliche Wortanzahl pro Nachricht pro Nutzer
        self._plotter.plot_user_vs_number_dict(self._analyzer.user_avg_word_count(),
                                               title=None,
                                               mode="bar",
                                               export_path=f"{self._chat_plot_dir}/msg_len_per_user.png")

    def cmd_out(self):
        '''Zeigt Ergebnisse in der Konsole an'''
        con = Console()

        def user_most_common_table(d):
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
        user_most_common_table(most_common_words)
        print()

        con.print(
            "[green]Häufigste Emojis (als Text, da das Terminal keine Emojis anzeigen kann)[/green]")
        most_common_emojis = self._analyzer.user_most_common_emojis(
            as_text=True)
        user_most_common_table(most_common_emojis)
        print()

    def create_html_report(self):
        html_str = fr'''
<!DOCTYPE html>
<html>
  <head>
    <!-- Meta tags -->
    <meta charset="utf-8" />
    <meta
      name="viewport"
      content="width=device-width, initioal-scale=1, shrink-to-fi=no"
    />

    <!-- Bootstrap CSS -->
    <link
      rel="stylesheet"
      href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
      integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
      crossorigin="anonymous"
    />
    
    <style>
      .jumbotron {{
        border-radius: 0px 0px 15px 15px;
        padding: 2vh;
      }}

      .card {{
        background: rgb(236, 239, 244);
        border-color: rgb(236, 239, 244);
        border-radius: 30px;
        box-shadow: -15px -15px 20px white,
          15px 15px 20px rgb(151, 167, 195, 0.5);
      }}

      .card-title {{
        font-family: "Roboto", sans-serif;
        font-weight: 600;
        padding: 5px;
      }}

      h1 {{
        font-family: Trebuchet MS;
        justify-content: center;
      }}

      body {{
        background-color: rgb(236, 239, 244);
      }}
    </style>

    <script
      src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"
      defer
    ></script>
    <script
      src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"
      defer
    ></script>
    <script
      src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"
      defer
    ></script>
  </head>

  <body>
    <div class="jumbotron bg-info text-white text-center">
      <div class="container">
        <h1 class="display-4">WhatsApp Report von "{self._chatname_base}"</h1>
      </div>
    </div>

    <div class="container text-center text-muted" style="min-width: 90vw">
      <!-- cards -->
      <div class="row">
        <div class="col-lg-12 col-xl-6 mb-4">
          <div class="card h-100">
            <img
              class="card-img-top img-fluid"
              src="{path.join(self._rel_chat_plot_dir, "msg_per_user.png")}"
              alt="msg_by_user"
            />
            <div class="card-block">
              <h2 class="card-title">Nachrichten pro Nutzer</h2>
            </div>
          </div>
        </div>

        <div class="col-lg-12 col-xl-6 mb-4">
          <div class="card h-100">
            <img
              class="card-img-top img-fluid"
              src="{path.join(self._rel_chat_plot_dir, "media_per_user.png")}"
              alt="media_per_user"
            />
            <div class="card-block">
              <h2 class="card-title">Medienanzahl pro Nutzer</h2>
            </div>
          </div>
        </div>

        <div class="col-lg-12 col-xl-6 mb-4">
          <div class="card h-100">
            <img
              class="card-img-top img-fluid"
              src="{path.join(self._rel_chat_plot_dir, "conv_start.png")}"
              alt="conv_start"
            />
            <div class="card-block">
              <h2 class="card-title">
                Wie oft hat der Nutzer die Unterhaltung gestartet?
              </h2>
            </div>
          </div>
        </div>

        <div class="col-lg-12 col-xl-6 mb-4">
          <div class="card h-100">
            <img
              class="card-img-top img-fluid"
              src="{path.join(self._rel_chat_plot_dir, "msg_len_per_user.png")}"
              alt="msg_len_per_user"
            />
            <div class="card-block">
              <h2 class="card-title">Durchschnittliche Anzahl an Worten pro Nachricht</h2>
            </div>
          </div>
        </div>

        <div class="col-lg-12 col-xl-6 mb-4">
          <div class="card h-100">
            <img
              class="card-img-top img-fluid"
              src="{path.join(self._rel_chat_plot_dir, "msg_by_weekday.png")}"
              alt="msg_by_weekday"
            />
            <div class="card-block">
              <h2 class="card-title">Nachrichten pro Wochentag</h2>
            </div>
          </div>
        </div>

        <div class="col-lg-12 col-xl-6 mb-4">
          <div class="card h-100">
            <img
              class="card-img-top img-fluid"
              src="{path.join(self._rel_chat_plot_dir, "msg_by_hour.png")}"
              alt="msg_by_hour"
            />
            <div class="card-block">
              <h2 class="card-title">Nachrichten pro Uhrzeit</h2>
            </div>
          </div>
        </div>

        <div class="col-lg-12 col-xl-6 mb-4">
          <div class="card h-100">
            <img
              class="card-img-top img-fluid"
              src="{path.join(self._rel_chat_plot_dir, "msg_per_week.png")}"
              alt="msg_by_hour"
            />
            <div class="card-block">
              <h2 class="card-title">Nachrichten pro Woche</h2>
            </div>
          </div>
        </div>

        <div class="col-lg-12 col-xl-6 mb-4">
          <div class="card h-100">
            <img
              class="card-img-top img-fluid"
              src="{path.join(self._rel_chat_plot_dir, "msg_per_person_per_week.png")}"
              alt="msg_per_person_per_week"
            />
            <div class="card-block">
              <h2 class="card-title">Nachrichten pro Woche pro Nutzer</h2>
            </div>
          </div>
        </div>

      </div>
    </div>
  </body>
</html>

'''
        # Report im Reportordner speichern
        report_path = path.join(
            self._project_basedir, "reports", f"{self._chatname_base}_report.html")
        with open(report_path, "w") as f:
            f.write(html_str)

        # aktuellen Report im Rootverzeichnis speichern
        recent_report_path = path.join(
            self._project_basedir, f"recent_report.html")
        with open(recent_report_path, "w") as f:
            f.write(html_str)
