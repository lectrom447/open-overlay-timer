import sys
import os

def get_asset_path(asset_name: str):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, 'assets', asset_name)

