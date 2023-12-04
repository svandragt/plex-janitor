#!/usr/bin/env python3
import sys
import configparser

import plexapi
from plexapi.myplex import MyPlexAccount

# script action
if len(sys.argv) >= 2:
    action = sys.argv[1]
else:
    action = "dryrun"
    print('Note: To delete, add "delete" as the script parameter')
print("Action:", action)

# read config
configparser = configparser.RawConfigParser()
configparser.read(r"config.ini")
username = configparser.get("Plex", "username")
password = configparser.get("Plex", "password")
servername = configparser.get("Plex", "servername")

# sign in
account = MyPlexAccount(username, password)
plex = account.resource(servername).connect()  # returns a PlexServer instance

# delete tv shows ep
print("")
print("TV")
items = {}


def try_delete(item):
    try:
        print(item.locations)
        item.delete()
        print("deleted", item)
    except plexapi.exceptions.BadRequest as e:
        print(f"Error: {e}")
        # Handle the specific exception (BadRequest) as needed
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Handle other exceptions here


for ep in plex.library.section("TV Shows").collection("Deletable TV").items():
    if ep.show() in items:
        prev = items[ep.show()]
        if action == "delete":
            try_delete(prev)
        else:
            print("deletable", prev)
    items[ep.show()] = ep

# delete films
print("")
print("FILMS")
for film in plex.library.section("Films").collection("Deletable Films").items():
    if action == "delete":
        try_delete(film)
        print("deleted", film)
    else:
        print("deletable", film)
