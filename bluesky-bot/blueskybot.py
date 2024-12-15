import json
from datetime import datetime
import random

from atproto import Client

def main():
    # super secret password, shhhhh
    pwd = ""
    with open("app-pwd.txt", "r", encoding="UTF-8") as f:
        pwd = f.read()

    # read matches, convert dates etc.
    matches = []
    with open("matches.json", "r", encoding="UTF-8") as f:
        matches = json.load(f)

    for m in matches:
        m["date"] = datetime.strptime(m["date"], "%Y-%m-%dT%H:%M:%SZ")

    # find matches "on this day"
    # if none, select a match at random
    today = datetime.today()

    matches_to_print = []

    for m in matches:
        if m["date"] < today and m["date"].month == today.month and m["date"].day == today.day:
            matches_to_print.append(m)

    on_this_day = len(matches_to_print) > 0

    if len(matches_to_print) == 0:
        matches_to_print.append(random.choice(matches))

    # construct the message
    def print_matches(matches, is_today):
        message = ""
        if is_today:
            message = f'On this day ({today.strftime("%b %d")}):\n'
            for match in matches:
                message += f'\n {match["homeCountryLabel"]} {match.get("homeCountryFlagUnicode", "")} {match["homeGoals"]} : {match["awayGoals"]} {match.get("awayCountryFlagUnicode", "")} {match["awayCountryLabel"]} ({match["date"].year})'
        else:
            match = matches[0]
            message = f'No entry found for {today.strftime("%b %d")}. Here is a random game instead:\n\n {match["homeCountryLabel"]} {match.get("homeCountryFlagUnicode", "")} {match["homeGoals"]} : {match["awayGoals"]} {match.get("awayCountryFlagUnicode", "")} {match["awayCountryLabel"]} ({match["date"].strftime("%d %b %Y")})'
        
        return message

    message = print_matches(matches_to_print, on_this_day)

    # post the message
    client = Client()
    client.login('magyarmatchdaybot.bsky.social', pwd)
    client.send_post(text=message)


if __name__ == "__main__":
    main()