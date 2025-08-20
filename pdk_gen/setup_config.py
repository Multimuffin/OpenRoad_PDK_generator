import json
from pathlib import Path

def run_setup():
    config_path = Path.cwd() / ".pdkgenrc"
    tech_roots = {}
    print("Technology root initialization for 'tower' and 'dongbu':")
    for tech_name in ["tower", "dongbu"]:
        while True:
            tech_path = input(f"Please specify the path for '{tech_name}': ").strip()
            if not Path(tech_path).is_dir():
                print(f"Error: The directory '{tech_path}' does not exist. Please provide a valid path.")
                continue
            break
        tech_roots[tech_name] = tech_path
    while True:
        platforms_root = input("Please specify the destination root path: ").strip()
        if not Path(platforms_root).is_dir():
            print(f"Error: The directory '{platforms_root}' does not exist. Please provide a valid path.")
            continue
        break
    config = {
        "tech_roots": tech_roots,
        "platforms_root": platforms_root
    }
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Configuration successfully saved in {config_path}")

def load_user_config():
    config_path = Path.cwd() / ".pdkgenrc"
    with open(config_path) as f:
        return json.load(f)

if __name__ == "__main__":
    run_setup()
