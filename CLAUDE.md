# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-script tool (`plexjanitor.py`) that lists, and optionally deletes, watched TV episodes and films from a Plex server, to free up disk space while keeping favourites and the last-seen episode of each show.

## Commands

```shell
uv run python plexjanitor.py         # dry run: lists what would be deleted
uv run python plexjanitor.py delete  # actually deletes
uv run ruff check .                  # lint
uv run ruff format .                 # format
uv run pytest                        # run tests
```

CI (`.github/workflows/ci.yml`) runs ruff check, ruff format --check, pytest, and pip-audit on every push/PR. Dependabot (`.github/dependabot.yml`) checks `uv` and `github-actions` ecosystems weekly; `.github/workflows/dependabot-auto-merge.yml` auto-merges patch/minor Dependabot PRs once CI passes (major bumps still need manual review — relevant for PlexAPI, which can break on major versions).

## Configuration

Requires a `config.ini` (gitignored, not present in repo) with a `[Plex]` section: `baseurl` (e.g. `http://192.168.0.10:32400`) and `token` (your `X-Plex-Token`). Read via `configparser` in `connect()`, which connects with `PlexServer(baseurl, token)`.

## Architecture

`plexjanitor.py` is organized as small functions called from `main()` (guarded by `if __name__ == "__main__":`), so the deletion logic is testable without a real Plex connection — see `tests/test_plexjanitor.py`, which mocks the section/collection/item objects.

1. `main()` parses the `delete`/dry-run action from `sys.argv[1]`, calls `connect()`, then `clean_tv()` and `clean_films()`.
2. `connect()` reads `baseurl` and `token` from `config.ini` and connects via `plexapi.server.PlexServer` (direct connection, no cloud round-trip).
3. `clean_tv()`: iterates the "Deletable TV" collection in the "TV Shows" library section. Since collection items come in per-episode, it tracks one item per `ep.show()` in the `items` dict — when a new episode of an already-seen show appears, the *previous* one is marked deletable/deleted, and the latest episode is retained as the "continue watching" marker. Only the most recently listed episode per show survives each run.
4. `clean_films()`: iterates the "Deletable Films" collection in the "Films" library section and deletes/lists every item (no last-one-kept logic).
5. `keep_if_starred()`: rescues any 5-star item (Plex `userRating` 10.0) by adding it to the "Keep" collection instead of deleting it — so you can preserve something from the Plex phone/TV apps just by rating it. Films are matched on the film's own rating; TV is matched on the *series* rating (`ep.show().userRating`), which keeps all of that show's episodes. Only mutates in `delete` mode; dry run prints `would keep`.
6. `try_delete()` wraps `item.delete()` and swallows `plexapi.exceptions.BadRequest` and generic exceptions, printing rather than raising.

The "Deletable TV"/"Deletable Films" collections are expected to already be pre-filtered in Plex itself (Plays > 0 AND Collection is not Keep) — this script does not apply those filters itself, it only adds the "keep last watched episode" logic on top and gates on the `delete` action.
