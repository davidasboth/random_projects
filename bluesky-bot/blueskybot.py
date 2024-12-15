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

    options = []
    match_to_print = None

    for m in matches:
        if m["date"] < today and m["date"].month == today.month and m["date"].day == today.day:
            options.append(m)

    on_this_day = len(options) > 0

    if on_this_day:
        match_to_print = random.choice(options)
    else:
        match_to_print = random.choice(matches)

    # construct the message
    def print_match(match, is_today):
        message = ""
        if is_today:
            message = f"""On this day in {match["date"].year}: {match["homeCountryLabel"]} {match["homeCountryFlagUnicode"]} {match["homeGoals"]} : {match["awayGoals"]} {match["awayCountryFlagUnicode"]} {match["awayCountryLabel"]}\n\nWikidata entry: {match["match"]}"""
        else:
            message = f"""No entry found for {today.strftime("%b %d")}. Here's a random game instead:\n\n{match["homeCountryLabel"]} {match["homeCountryFlagUnicode"]} {match["homeGoals"]}: {match["awayGoals"]} {match["awayCountryFlagUnicode"]} {match["awayCountryLabel"]} ({match["date"].strftime("%d %b %Y")})\n\nWikidata entry: {match["match"]}"""
        
        return message

    message = print_match(match_to_print, on_this_day)

    # post the message
    client = Client()
    client.login('magyarmatchdaybot.bsky.social', pwd)
    client.send_post(text=message)


if __name__ == "__main__":
    main()