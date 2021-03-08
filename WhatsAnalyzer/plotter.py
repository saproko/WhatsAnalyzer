# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from scipy.ndimage.filters import gaussian_filter1d


class Plotter:
    def __init__(self, messages) -> None:
        sns.despine(left=True, bottom=True)
        self._messages = messages
        self._df = self._init_dataframe()
        self._nicecolors = ["#577590", "#43aa8b", "#90be6d",
                            "#f9c74f", "#f8961e", "#f3722c", "#f94144"]
        self.prettify()

    def _init_dataframe(self, datetime_index=True) -> pd.DataFrame:
        messages = self._messages
        message_dicts = [msg.dictionary for msg in messages]
        df = pd.DataFrame(message_dicts)
        return df

    @property
    def df(self) -> pd.DataFrame:
        '''Return das Haupt DataFrame mit allen Nachrichten'''
        return self._df

    def prettify(self) -> None:
        '''Verschönert die Matplotlib Darstellung'''
        sns.set(font="Franklin Gothic Book",
                rc={"axes.axisbelow": False,
                    "axes.edgecolor": "lightgrey",
                    "axes.facecolor": "None",
                    "axes.grid": False,
                    "axes.labelcolor": "dimgrey",
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.facecolor": "white",
                    "lines.solid_capstyle": "round",
                    "patch.edgecolor": "w",
                    "patch.force_edgecolor": True,
                    "text.color": "dimgrey",
                    "xtick.bottom": False,
                    "xtick.color": "dimgrey",
                    "xtick.direction": "out",
                    "xtick.top": False,
                    "ytick.color": "dimgrey",
                    "ytick.direction": "out",
                    "ytick.left": False,
                    "ytick.right": False})

    def gaussian_filter(self, lst: list, sigma: float = 1.5):
        return gaussian_filter1d(lst, sigma=sigma)

    def plot_total_messages_over_time(self, export_path: str = None, show: bool = False):
        '''Plots Nachrichten über Zeit (resample mode bestimmt Periode)
           export_path: falls nicht None -> speichert den plot unter <export_path>
           show: falls True: zeigt das Diagramma an'''

        # Gruppieren (resamplen) auf die festgelegte Periode
        data = self.df.groupby(self.df._dateandtime.dt.date).size()
        data.index = pd.to_datetime(data.index)
        data = data.resample("W").sum()
        ax = data.plot(kind="bar", title="Nachrichten pro Woche")

        # tick Formatierung
        ticklabels = [""]*len(data.index)
        ticklabels[::4] = [item.strftime('%b %d') for item in data.index[::4]]
        ticklabels[::12] = [item.strftime('%b %d\n%Y')
                            for item in data.index[::12]]
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
        ax.set_xlabel("Zeit")
        plt.gcf().autofmt_xdate()

        self.plot(show=show, export_path=export_path)

    def plot_user_messages_over_time(self, export_path=None, show=False):
        '''Plot Entwicklung der Nachrichtenanzahl pro Nutzer über die Zeit'''
        groups = self.df.groupby([pd.Grouper(key="_dateandtime", freq="W"), "_username"])[
            "_username"].size()

        datadict = {}
        # Daten von jedem Nutzer bestimmen
        for username in self.df["_username"].unique():
            user_df = groups.xs(username, level=1, drop_level=False)
            x_data = list(user_df.index.get_level_values(0))
            y_data = self.gaussian_filter(list(user_df.values))
            datadict[username] = (x_data, y_data)

        # Nachrichten summieren und sortieren
        user_sums = {username: sum(data[1])
                     for username, data in datadict.items()}
        sorted_user_sums = dict(
            sorted(user_sums.items(), key=lambda item: item[1], reverse=True))

        # Daten entpacken und plotten
        for username in sorted_user_sums.keys():
            user_data = datadict[username]
            x_data = user_data[0]
            y_data = user_data[1]
            total_msg_count = user_sums[username]

            plt.plot(x_data, y_data,
                     label=f"{username} - ({total_msg_count} Total)")

        plt.legend()
        plt.gca().set_title("Nachrichten pro Woche pro Nutzer")
        self.plot(show=show, export_path=export_path)

    def plot_group_messeges_by(self, by: str, export_path=None, show=False):
        '''Plots Nachrichten Gruppiert nach "by"
           by: Möglichkeiten ("hour", "weekday")
           export_path: falls nicht None -> speichert den plot unter <export_path>
           show: falls True: zeigt das Diagramma an'''

        if by == "hour":
            data = self.df.groupby(self.df._dateandtime.dt.hour).size()
            ax = data.plot.bar(title="Nachrichten pro Stunde")
            ax.set_xlabel("Stunde")

        elif by == "weekday":
            data = self.df.groupby(self.df._dateandtime.dt.weekday).size()

            weekday_names = {0: "Montag", 1: "Dienstag", 2: "Mittwoch",
                             3: "Donnerstag", 4: "Freitag", 5: "Samstag", 6: "Sonntag"}
            data.index = [weekday_names.get(item, item) for item in data.index]

            ax = data.plot.bar(title="Nachrichten pro Wochentag")
            ax.set_xlabel("Wochentag")

        else:
            raise ValueError(
                f"Den Modus '{by}' gibt es nicht. Versuch es mal mit 'hour' oder 'weekday'")

        # x-Label rotieren
        ax = plt.gca()
        plt.setp(ax.get_xticklabels(), rotation=30,
                 horizontalalignment='right')

        self.plot(show=show, export_path=export_path)

    def plot_user_vs_number_dict(self, d: dict, mode: str = "bar",
                                 title: str = "", label_func=None,
                                 export_path=None, show=False):
        '''Plots Dictionary nach dem Muster {<User Objekt>: Wert (int)}
           data: Dictionary zum plotten
           mode: Diagrammtyp ("bar" oder "pie")
           title: Titel des Plots
           label_func: Funktion, die auf die Werte angewendet wird, bevor sie zu Labels werden
           export_path: falls nicht None -> speichert den plot unter <export_path>
           show: falls True: zeigt das Diagramma an'''

        def sorted_dict(to_sort: dict, reverse=False, round_numbers=True):
            # nach Wert sortieren
            sorted_dict = {k: v for k, v in sorted(
                to_sort.items(), key=lambda item: item[1], reverse=reverse)}

            # Werte runden
            if round_numbers:
                sorted_dict = {user: round(value, 1)
                               for user, value in sorted_dict.items()}

            # Nutzername als y-Wert
            return {user.username: value for user, value in sorted_dict.items()}

        def apply_label_func(l):
            return list(map(label_func, l))

        if mode == "bar":
            data = sorted_dict(d, reverse=True)
            plt.bar(data.keys(), data.values())

            # x-Ticks rotieren
            ax = plt.gca()
            plt.setp(ax.get_xticklabels(), rotation=30,
                     horizontalalignment='right')

            plt.gca().set_title(title)

        elif mode == "pie":
            data = sorted_dict(d, reverse=True)
            # Nutzernamen für die Legende
            legend_labels = data.keys()
            values = data.values()

            # Werte als Labels eventuell anpassen
            if label_func is not None:
                pie_labels = apply_label_func(values)
            else:
                pie_labels = values

            # plot erstellen
            patches, texts = plt.pie(values, startangle=-90,
                                     labels=pie_labels, labeldistance=.8,
                                     colors=self._nicecolors)
            # Labels anpassen
            for t in texts:
                t.set_horizontalalignment("center")
                t.set_color("white")

            # Titel einfügen
            plt.gca().set_title(title)
            # Legende rechts einfügen
            plt.legend(patches, legend_labels, loc="center left",
                       bbox_to_anchor=(0.9, 0.5), frameon=False)

        else:
            raise ValueError(f"Den Modus '{mode}' gibt es nicht.")

        self.plot(show=show, export_path=export_path)

    def plot(self, show=False, export_path=None):
        plt.tight_layout()
        plt.gcf().set_size_inches(8, 6)

        if export_path is not None:
            # Exportieren
            plt.savefig(export_path)

        if show:
            # Plot anzeigen
            plt.show()
        else:
            plt.clf()
