def test_show_form(http_client, sample_app):
    sample_app('form_app.py')
    c = http_client()
    res = c.get('/simple')
    assert res.status == 200
    assert res.read() == 'Imagine this is a form'


def test_submit_form(http_client, sample_app):
    sample_app('form_app.py')
    c = http_client()
    res = c.post('/simple', data={'string': 'Foo', 'number': 12})
    assert res.status == 200
    assert res.read() == 'OK: Foo 12'
