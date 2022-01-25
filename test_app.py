"""
Test file for app.py and db_functions.py
"""

import db_functions as df
import app as app


def test_get_filter_str():
    result = df.get_filter_str({"title": "computer"})
    assert result["title"]["$regex"] == ".*computer.*"


def test_get_entries():
    result = df.get_entries({"title": "Algorithms to Live By: The Computer Science of Human Decisions"}, "books")
    assert result[0]["book_id"] == "25666050"


def test_add_entries():
    df.add_entries({"title": "crazy test title", "hey": "should be hey"}, 0, "books")
    result2 = df.get_entries({"title": "crazy test title"}, "books")
    df.del_entries({"title": "crazy test title"}, "books")
    assert result2[0]["hey"] == "should be hey"


def test_update_entries():
    df.add_entries({"title": "crazy test title", "hey": "should be hey"}, 0, "books")
    df.update_entries({"hello": "should be hello"}, {"title": "crazy test title"}, "books")
    result2 = df.get_entries({"title": "crazy test title"}, "books")
    df.del_entries({"title": "crazy test title"}, "books")
    assert result2[0]["hello"] == "should be hello"


def test_del_entries():
    df.add_entries({"title": "crazy test title333", "hey": "should be hey"}, 0, "books")
    df.del_entries({"title": "crazy test title333"}, "books")
    result2 = df.get_entries({"title": "crazy test title333"}, "books")
    print(result2)
    assert len(result2) == 0


def test_advanced_search():
    df.add_entries({"title": "crazy test title1", "hey": "should be hey"}, 0, "books")
    df.add_entries({"title": "crazy test title2", "hey": "should be hey"}, 0, "books")
    result = df.advanced_search({"a": "title1", "b": "title2"}, 0, "title", "books")
    assert len(result) == 2
    df.del_entries({"title": "crazy test title1"}, "books")
    df.del_entries({"title": "crazy test title2"}, "books")


def test_index():
    assert app.index() == 'Hi! Here is the main page.'

# def test_advance():
#     assert False
#
#
# def test_book():
#     assert False
#
#
# def test_books():
#     assert False
