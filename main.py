from Ui import Ui
from Data import Data
from Parse import Parse
import PySimpleGUI as gui
from Analysis import Analysis

import numpy as np

CANCEL = "Cancel"
EXIT = "Exit"

TIMEOUT_VALUE = 30
VALUE_START = 0
VALUE_END = 1000


if __name__ == "__main__":

    ui = Ui()
    window = ui.get_ui()
    progress_bar = ui.get_progress_bar()

    while True:

        event, values = window.Read(close=False)

        if event in (gui.WIN_CLOSED, EXIT):
            break

        company = values[0]

        data = Data()

        parse = Parse(company=company)
        articles_of_interest = parse.get_articles_of_interest()
        number_of_articles = parse.get_len_articles_of_interest()
        step = VALUE_END / number_of_articles
        index = VALUE_START

        analysis = Analysis(company=company, data=articles_of_interest, size=number_of_articles)

        for article in np.arange(VALUE_START, VALUE_END, step):
            analysis.analyse(index)
            index += 1
            progress_bar.UpdateBar(article)

        progress_bar.UpdateBar(VALUE_END)

        analysis.show_analysis()

        print("\nYou can key in another company's name to get started with a new analysis.")