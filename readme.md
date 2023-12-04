# PLEX Janitor

This script lists and optionally deletes watched episodes and films in Plex.

* It keeps the last seen episode of a show, so you can continue where you left off.
* Prevent your favourites from being deleted by putting series / films in a Keep collection.

It requires python 3.9+ and [poetry](https://python-poetry.org/).

Install:

Create `config.ini` with the following contents:

```ini
[Plex]
username = <username>
password = <password>
servername = <plex servername>
```

Run the script:

```shell
poetry install
poetry run python plexjanitor.py
```

The script makes the following assumptions:

- There's two sections: "TV Shows" and "Films"
- The TV Shows section has a collection "Keep" and a collection "Deletable TV"
- The Films section has a collection "Keep" and a collection "Deletable Films"
- Add items to the Keep collection manually (for TV Shows tag the show, not the episode). These will not be deleted.
- The Deletable* collections must have these filters:
  - Plays is greater than 0
  - AND Collection is not Keep

This script will then go through each section and list deletable items. For TV Shows the most recent episode will be kept, as a marker for the last seen episode.

By default deletable items are listed but not deleted. By passing `delete` as a script parameter, items will be actually deleted!
