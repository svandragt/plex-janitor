#!/usr/bin/env python3
import configparser
import sys

import plexapi
from plexapi.server import PlexServer

# Plex userRating is 0-10; 5 stars = 10.0.
FIVE_STARS = 10


def keep_if_starred(item, action, kept):
    """Rescue a 5-star item into the Keep collection instead of deleting it.

    `item` is what goes into Keep (a show or a film). Returns True if kept.
    Adds to Keep only in delete mode; reports in dry run.
    """
    if not (item.userRating and item.userRating >= FIVE_STARS):
        return False
    if item.ratingKey not in kept:
        kept.add(item.ratingKey)
        if action == "delete":
            item.addCollection("Keep")
            print("kept (5 star)", item)
        else:
            print("would keep (5 star)", item)
    return True


def try_delete(item):
    try:
        print(item.locations)
        item.delete()
        print("deleted", item)
    except plexapi.exceptions.BadRequest as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def episode_sort_key(ep):
    return (ep.seasonNumber or 0, ep.episodeNumber or 0)


def clean_tv(section, action):
    print("")
    print("TV")
    items = {}
    kept = set()
    episodes = sorted(section.collection("Deletable TV").items(), key=episode_sort_key)
    for ep in episodes:
        if ep.show() in items:
            prev = items[ep.show()]
            if keep_if_starred(prev.show(), action, kept):
                pass
            elif action == "delete":
                try_delete(prev)
            else:
                print("deletable", prev)
        items[ep.show()] = ep


def clean_films(section, action):
    print("")
    print("FILMS")
    kept = set()
    for film in section.collection("Deletable Films").items():
        if keep_if_starred(film, action, kept):
            continue
        if action == "delete":
            try_delete(film)
        else:
            print("deletable", film)


def connect(config_path="config.ini"):
    config = configparser.RawConfigParser()
    if not config.read(config_path):
        sys.exit(f"Error: could not read config file '{config_path}'")
    if not config.has_section("Plex"):
        sys.exit(f"Error: '{config_path}' is missing a [Plex] section")
    baseurl = config.get("Plex", "baseurl")
    token = config.get("Plex", "token")
    return PlexServer(baseurl, token)


def main():
    if len(sys.argv) >= 2:
        action = sys.argv[1]
        if action != "delete":
            print(f'Warning: unrecognized action "{action}", treating as dry run')
    else:
        action = "dryrun"
        print('Note: To delete, add "delete" as the script parameter')
    print("Action:", action)

    plex = connect()
    clean_tv(plex.library.section("TV Shows"), action)
    clean_films(plex.library.section("Films"), action)


if __name__ == "__main__":
    main()
