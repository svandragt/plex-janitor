from unittest.mock import MagicMock

import plexapi.exceptions

import plexjanitor


def make_episode(show_name):
    show = MagicMock(name=f"show-{show_name}")
    ep = MagicMock()
    ep.show.return_value = show
    return ep, show


def test_clean_tv_keeps_last_episode_per_show_dryrun(capsys):
    ep1, show = make_episode("Foo")
    ep2, _ = make_episode("Foo")
    ep2.show.return_value = show  # same show as ep1

    section = MagicMock()
    section.collection.return_value.items.return_value = [ep1, ep2]

    plexjanitor.clean_tv(section, action="dryrun")

    ep1.delete.assert_not_called()
    ep2.delete.assert_not_called()


def test_clean_tv_deletes_all_but_last_episode_per_show():
    ep1, show = make_episode("Foo")
    ep2, _ = make_episode("Foo")
    ep2.show.return_value = show

    section = MagicMock()
    section.collection.return_value.items.return_value = [ep1, ep2]

    plexjanitor.clean_tv(section, action="delete")

    ep1.delete.assert_called_once()
    ep2.delete.assert_not_called()


def test_clean_tv_does_not_delete_single_episode_shows():
    ep1, _ = make_episode("Foo")
    ep2, _ = make_episode("Bar")

    section = MagicMock()
    section.collection.return_value.items.return_value = [ep1, ep2]

    plexjanitor.clean_tv(section, action="delete")

    ep1.delete.assert_not_called()
    ep2.delete.assert_not_called()


def test_clean_films_deletes_all_when_action_is_delete():
    film1 = MagicMock()
    film2 = MagicMock()
    section = MagicMock()
    section.collection.return_value.items.return_value = [film1, film2]

    plexjanitor.clean_films(section, action="delete")

    film1.delete.assert_called_once()
    film2.delete.assert_called_once()


def test_clean_films_dryrun_deletes_nothing():
    film1 = MagicMock()
    section = MagicMock()
    section.collection.return_value.items.return_value = [film1]

    plexjanitor.clean_films(section, action="dryrun")

    film1.delete.assert_not_called()


def test_try_delete_swallows_bad_request():
    item = MagicMock()
    item.delete.side_effect = plexapi.exceptions.BadRequest("nope")

    plexjanitor.try_delete(item)  # must not raise


def test_try_delete_swallows_unexpected_errors():
    item = MagicMock()
    item.delete.side_effect = RuntimeError("boom")

    plexjanitor.try_delete(item)  # must not raise
