import json
import argparse
import os

def save_scores_to_file(scores_info, filename):
    with open(filename, 'w') as file:
        json.dump(scores_info, file, indent=4)

def load_scores_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def main():
    parser = argparse.ArgumentParser(description="Team Scores CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add a description about the use of environment variable
    parser.add_argument(
        '--env-var', type=str, default='SCORES_FILE',
        help='Name of the environment variable to get the default filename'
    )

    # Save command
    save_parser = subparsers.add_parser('save', help="Save team scores to a JSON file")
    save_parser.add_argument('filename', type=str, nargs='?', help="The filename to save the scores")

    # Load command
    load_parser = subparsers.add_parser('load', help="Load team scores from a JSON file")
    load_parser.add_argument('filename', type=str, nargs='?', help="The filename to load the scores from")

    # Check command
    check_parser = subparsers.add_parser('check', help="Check team positions")
    check_parser.add_argument('filename', type=str, nargs='?', help="The filename to load the scores from")

    args = parser.parse_args()

    # Get the default filename from the environment variable if provided
    env_var_name = args.env_var
    default_filename = os.getenv(env_var_name)

    if args.command == "save":
        filename = args.filename or default_filename
        if not filename:
            print(f"No filename provided and environment variable '{env_var_name}' is not set.")
            return

        scores_info = {
            "First Team": 100,
            "Second Team": 90,
            "Third Team": 80,
            "Fourth Team": 50,
            "Fifth Team": 30,
        }
        save_scores_to_file(scores_info, filename)
        print(f"Scores saved to {filename}")

    elif args.command == "load":
        filename = args.filename or default_filename
        if not filename:
            print(f"No filename provided and environment variable '{env_var_name}' is not set.")
            return

        try:
            scores_info = load_scores_from_file(filename)
            print(f"Scores loaded from {filename}: {scores_info}")
        except FileNotFoundError:
            print(f"File {filename} not found")

    elif args.command == "check":
        filename = args.filename or default_filename
        if not filename:
            print(f"No filename provided and environment variable '{env_var_name}' is not set.")
            return

        try:
            scores_info = load_scores_from_file(filename)
        except FileNotFoundError:
            print(f"File {filename} not found")
            return

        team_list = [
            input(f"{i+1}. Enter team name (First Team, Second Team, Third Team, Fourth Team, Fifth Team): \n")
            for i in range(5)
        ]

        if position_checker(scores_info, team_list):
            print("Team positions correct!")
        else:
            print("Team positions incorrect!")

def position_checker(scores_info: dict, team_list: list) -> bool:
    sorted_teams = sorted(scores_info.keys(), key=lambda x: scores_info[x], reverse=True)
    return sorted_teams == team_list

if __name__ == '__main__':
    main()
