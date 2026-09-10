import os 
import sys
from banner import banner_
from modules.main import main_

def main_menu():
    print(banner_)
    main_()

main_menu()