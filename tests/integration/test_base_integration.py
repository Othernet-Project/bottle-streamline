def test_simple_app(http_client, sample_app):
    sample_app('base_only.py')
    c = http_client()
    res = c.get('/')
    assert res.status == 200
    assert 'Hello world!' in res.read()
    assert res.getheader('foo') == 'bar'


def test_simple_app_post_fails(http_client, sample_app):
    sample_app('base_only.py')
    c = http_client()
    res = c.post('/')
    assert res.status == 405


def test_simple_app_other_methods(http_client, sample_app):
    sample_app('base_only.py')
    c = http_client()
    res = c.post('/other')
    assert res.status == 200
    res = c.delete('/other')
    assert res.status == 200
    res = c.patch('/other')
    assert res.status == 200
