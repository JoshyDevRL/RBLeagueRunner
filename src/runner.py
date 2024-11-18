
from rlbot.managers import MatchManager
from rlbot.flat import GameStatus
from pathlib import Path
import time

def run_match(match_settings):
    root_dir = Path(__file__).parent
    match_manager = MatchManager(root_dir)
    match_manager.ensure_server_started()
    match_manager.start_match(match_settings)
    try:
        while match_manager.packet.game_info.game_status != GameStatus.Ended:
            time.sleep(1.0)
    finally:
        match_manager.shut_down()
    match_manager.shut_down()
    print("Shuting down match...")
    