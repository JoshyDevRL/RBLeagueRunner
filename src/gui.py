
import sys, re
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QComboBox,
    QPushButton,
    QLabel,
    QTextEdit,
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

from threading import Thread

from rlbot.utils.maps import STANDARD_MAPS, GAME_MAP_TO_UPK
from rlbot.flat import MatchSettings, Launcher, GameMode, MatchLength, BoostOption, MutatorSettings

from runner import run_match

GAME_MODES = {
    "Soccer" : GameMode.Soccer, 
    "Hoops" : GameMode.Hoops,
    "Dropshot" : GameMode.Dropshot,
    "Snowday" : GameMode.Hockey,
    "Rumble" : GameMode.Rumble,
    "Heatseeker" : GameMode.Heatseeker,
    "Gridiron" : GameMode.Gridiron
}
TIME_CONTROLS = {
    "5 Minutes" : MatchLength.Five_Minutes,
    "10 Minutes" : MatchLength.Ten_Minutes,
    "20 Minutes" : MatchLength.Twenty_Minutes,
    "Unlimited" : MatchLength.Unlimited
}
BOOST_OPTIONS = {
    "Default" : BoostOption.Normal_Boost,
    "Unlimited" : BoostOption.Unlimited_Boost,
    "Slow Recharge" : BoostOption.Slow_Recharge,
    "Fast Recharge" : BoostOption.Rapid_Recharge,
    "No Boost" : BoostOption.No_Boost
}

class OutputRedirector:
    def __init__(self, append_function):
        self.append_function = append_function

    def write(self, message):
        if message.strip():
            self.append_function(message)

    def flush(self):
        pass

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Head
        self.setWindowTitle("RBLeagueRunner")
        self.setFixedSize(1280, 720)
        self.setWindowIcon(QIcon("assets/icon.ico"))
        with open("src/style.css", "r") as file:
            self.setStyleSheet(file.read())
        window_width = self.width()
        window_height = self.height()

        # Nav
        nav_bar = QWidget(self)
        nav_bar.setObjectName("nav_bar")
        nav_bar.setGeometry(0, 0, self.width(), 50)

        nav_bar2 = QWidget(self)
        nav_bar2.setObjectName("nav_bar2")
        nav_bar2.setGeometry(0, window_height-85, self.width(), 85)

        title_label = QLabel("RLBot League Runner", self)
        title_label.setObjectName("title_label")
        title_label.move(75, 10)
        title_label.adjustSize()

        icon_label = QLabel(self)
        pixmap = QPixmap("assets/icon.ico")
        scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
        icon_label.setPixmap(scaled_pixmap)
        icon_label.move(10, 10)

        # Main Widgets
        start_button = QPushButton("Start Match", self)
        start_button.setObjectName("start_button")
        start_button.setGeometry(10, window_height - 70, 140, 60)
        start_button.clicked.connect(self.start_match)

        map_select_label = QLabel("Map", self)
        map_select_label.setObjectName("map_select_label")
        map_select_label.move(170, window_height - 80)
        map_select = QComboBox(self)
        map_select.setObjectName("map_select")
        for m in GAME_MAP_TO_UPK.keys(): 
            map_select.addItem(m)
        map_select.currentTextChanged.connect(self.map_select_change)
        map_select.setGeometry(170, window_height - 50, 230, 40)

        mode_select_label = QLabel("Mode", self)
        mode_select_label.setObjectName("mode_select_label")
        mode_select_label.move(410, window_height - 80)
        mode_select = QComboBox(self)
        mode_select.setObjectName("mode_select")
        for m in GAME_MODES.keys(): 
            mode_select.addItem(m)
        mode_select.currentTextChanged.connect(self.mode_select_change)
        mode_select.setGeometry(410, window_height - 50, 150, 40)

        time_select_label = QLabel("Time Control", self)
        time_select_label.setObjectName("time_select_label")
        time_select_label.move(570, window_height - 80)
        time_select = QComboBox(self)
        time_select.setObjectName("time_select")
        for m in TIME_CONTROLS.keys():
            time_select.addItem(m)
        time_select.currentTextChanged.connect(self.time_select_change)
        time_select.setGeometry(570, window_height - 50, 150, 40)

        boost_select_label = QLabel("Boost Amount", self)
        boost_select_label.setObjectName("boost_select_label")
        boost_select_label.move(730, window_height - 72)
        boost_select_label.adjustSize()
        boost_select = QComboBox(self)
        boost_select.setObjectName("boost_select")
        for m in BOOST_OPTIONS.keys(): 
            boost_select.addItem(m)
        boost_select.currentTextChanged.connect(self.boost_select_change)
        boost_select.setGeometry(730, window_height - 50, 150, 40)

        # Console
        self.console_output = QTextEdit(self)
        self.console_output.setObjectName("console_output")
        self.console_output.setReadOnly(True)
        self.console_output.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.console_output.setFixedWidth(390)
        self.console_output.setFixedHeight(window_height - 50)
        self.console_output.move(window_width - 390, 50)

        sys.stdout = OutputRedirector(self.append_to_console)
        sys.stderr = OutputRedirector(self.append_to_console)

        self.selected_map = GAME_MAP_TO_UPK[STANDARD_MAPS[0]]
        self.selected_mode = GAME_MODES["Soccer"]
        self.selected_time = TIME_CONTROLS["5 Minutes"]
        self.selected_boost = BOOST_OPTIONS["Default"]

    def append_to_console(self, text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        result = ansi_escape.sub('', text)
        self.console_output.append(result)

    def start_match(self):
        print("Launching match...")
        match_settings = MatchSettings(launcher=Launcher.Steam,
                                       auto_start_bots=True,
                                       game_map_upk=self.selected_map,
                                       game_mode=self.selected_mode,
                                       mutator_settings=MutatorSettings(
                                       match_length=self.selected_time,
                                       boost_option=self.selected_boost
                                    ),
                                    )
        
        thread = Thread(target = run_match, args = (match_settings, ))
        thread.start()

    def map_select_change(self, text):
        self.selected_map = GAME_MAP_TO_UPK[text]

    def mode_select_change(self, text):
        self.selected_mode = GAME_MODES[text]

    def time_select_change(self, text):
        self.selected_time = TIME_CONTROLS[text]

    def boost_select_change(self, text):
        self.selected_boost = BOOST_OPTIONS[text]

