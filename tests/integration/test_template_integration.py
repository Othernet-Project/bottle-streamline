def test_template_rendering(http_client, sample_app):
    sample_app('template_app.py')
    c = http_client()
    res = c.get('/hello/Andrean')
    assert res.read() == 'Hello, Andrean!\n'
    res = c.get('/hello/Bob')
    assert res.read() == 'Hello, Bob!\n'


def test_template_xhr(http_client, sample_app):
    sample_app('template_app.py')
    c = http_client()
    res = c.get('/roca')
    assert res.read() == 'This is a full template\n'
    res = c.get('/roca', headers=c.XHR)
    assert res.read() == 'This is a partial template\n'
