# main.py
import os, sys
os.environ["SDL_VIDEO_WINDOW_POS"] = "100,100"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import Game

if __name__ == "__main__":
    Game().run()
