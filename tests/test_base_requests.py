import pytest


def test_simple_app(http_client, sample_app):
    sample_app('base_only.py')
    c = http_client()
    res = c.get('/')
    assert res.status == 200
    assert 'Hello world!' in res.read()


def test_simple_app_post_fails(http_client, sample_app):
    sample_app('base_only.py')
    c = http_client()
    res = c.post('/')
    assert res.status == 405
