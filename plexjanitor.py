#!/usr/bin/env python3
import configparser
import sys

import plexapi
from plexapi.myplex import MyPlexAccount


def try_delete(item):
    try:
        print(item.locations)
        item.delete()
        print("deleted", item)
    except plexapi.exceptions.BadRequest as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def clean_tv(section, action):
    print("")
    print("TV")
    items = {}
    for ep in section.collection("Deletable TV").items():
        if ep.show() in items:
            prev = items[ep.show()]
            if action == "delete":
                try_delete(prev)
            else:
                print("deletable", prev)
        items[ep.show()] = ep


def clean_films(section, action):
    print("")
    print("FILMS")
    for film in section.collection("Deletable Films").items():
        if action == "delete":
            try_delete(film)
        else:
            print("deletable", film)


def connect(config_path="config.ini"):
    config = configparser.RawConfigParser()
    config.read(config_path)
    username = config.get("Plex", "username")
    password = config.get("Plex", "password")
    servername = config.get("Plex", "servername")

    account = MyPlexAccount(username, password)
    return account.resource(servername).connect()


def main():
    if len(sys.argv) >= 2:
        action = sys.argv[1]
    else:
        action = "dryrun"
        print('Note: To delete, add "delete" as the script parameter')
    print("Action:", action)

    plex = connect()
    clean_tv(plex.library.section("TV Shows"), action)
    clean_films(plex.library.section("Films"), action)


if __name__ == "__main__":
    main()
