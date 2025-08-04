import json
from pathlib import Path

def run_setup():
    config_path = Path.cwd() / ".pdkgenrc"
    while True:
        tech_root = input("Path to technology root (one time setup): ").strip()
        if not Path(tech_root).is_dir():
            print(f"Directory does not exist: {tech_root}")
            continue
        break
    while True:
        platforms_root = input("Path for destination root: ").strip()
        if not Path(platforms_root).is_dir():
            print(f"Directory does not exist: {platforms_root}")
            continue
        break
    config = {
        "tech_root": tech_root,
        "platforms_root": platforms_root
    }
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Configuration saved in {config_path}")

def load_user_config():
    config_path = Path.cwd() / ".pdkgenrc"
    with open(config_path) as f:
        return json.load(f)

if __name__ == "__main__":
    run_setup()
    