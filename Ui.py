import PySimpleGUI as gui


class Ui:

    OUTPUT_WIDTH = 80
    OUTPUT_HEIGHT = 20
    PROGRESS_BAR_WIDTH = 44.75
    PROGRESS_BAR_HEIGHT = 20
    PROGRESS_BAR_SIZE = 1000

    BAR = "bar"
    TITLE_PROGRESS_BAR = "Progress Bar"
    TITLE_WINDOW = "News Sentiment Analysis"
    PROMPT = "Please enter the company you would like to analyse: "
    PROMPT_BUTTON = 'Analyse'

    def __init__(self):
        self.set_ui()
        self.set_progress_bar()

    def get_ui(self):
        return self.ui

    def get_progress_bar(self):
        return self.progress_bar

    def get_window_layout(self):
        layout = [
                [gui.Text(self.PROMPT)],
                [gui.InputText()],
                [gui.Text(self.TITLE_PROGRESS_BAR)],
                [gui.ProgressBar(self.PROGRESS_BAR_SIZE, orientation='h',
                                 size=(self.PROGRESS_BAR_WIDTH, self.PROGRESS_BAR_HEIGHT), key=self.BAR)],
                [gui.Output(size=(self.OUTPUT_WIDTH, self.OUTPUT_HEIGHT))],
                [gui.Button(self.PROMPT_BUTTON), gui.Exit()]
            ]
        return layout

    def set_ui(self):
        layout = self.get_window_layout()
        window = gui.Window(self.TITLE_WINDOW, layout)
        self.ui = window

    def set_progress_bar(self):
        self.progress_bar = self.ui[self.BAR]