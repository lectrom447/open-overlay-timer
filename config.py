from dataclasses import dataclass, asdict, field
import json

@dataclass
class OverlayConfig:
    position_x: int = 0
    position_y: int = 0
    show_at_start: bool = False


@dataclass
class Config:
    overlay_config:OverlayConfig = field(default_factory=OverlayConfig)
    open_overlay = True


CONFIG_STATE = Config()

def save_config_state():
    with open('config.json', 'w') as file:
        json.dump(asdict(CONFIG_STATE), file, indent=4)


def load_config_state():
    try: 
        with open("config.json", 'r') as file:
            data = json.load(file)
            
            CONFIG_STATE.overlay_config.position_x = data['overlay_config']['position_x']
            CONFIG_STATE.overlay_config.position_y = data['overlay_config']['position_y']
            CONFIG_STATE.overlay_config.show_at_start = data['overlay_config']['show_at_start']
    except:
        save_config_state()