import mock
import pytest


from streamline import template as mod


MOD = mod.__name__


def test_get_template():
    class Foo(mod.TemplateMixin):
        template_name = 'foobar'
    f = Foo()
    assert f.get_template_name() == 'foobar'


def test_get_template_as_argument():
    class Foo(mod.TemplateMixin):
        template_name = 'foobar'
    f = Foo()
    assert f.get_template_name('barfoo') == 'barfoo'


def test_get_template_with_no_template_name():
    class Foo(mod.TemplateMixin):
        pass
    f = Foo()
    with pytest.raises(NotImplementedError):
        f.get_template_name()


def test_get_template_as_argument_none():
    class Foo(mod.TemplateMixin):
        pass
    f = Foo()
    with pytest.raises(NotImplementedError):
        f.get_template_name(None)


def test_get_default_ctx():
    class Foo(mod.TemplateMixin):
        default_context = {'foo': 'bar'}
    f = Foo()
    assert f.get_default_context() == {'foo': 'bar'}


def test_get_default_ctx_always_copies():
    class Foo(mod.TemplateMixin):
        default_context = {'foo': 'bar'}
    f = Foo()
    assert id(f.get_default_context()) != id(Foo.default_context)
    assert id(f.get_default_context()) != id(f.get_default_context())


def test_get_default_default_context():
    import bottle

    class Foo(mod.TemplateMixin):
        pass
    f = Foo()
    assert f.get_default_context() == {'request': bottle.request}


def test_get_template_func():
    mock_tpl_func = mock.Mock()

    class Foo(mod.TemplateMixin):
        template_func = mock_tpl_func
    f = Foo()
    assert f.get_template_func() == mock_tpl_func


def test_get_default_template_func():
    import bottle

    class Foo(mod.TemplateMixin):
        pass
    f = Foo()
    assert f.get_template_func() == bottle.template


def test_get_context():
    class Foo(mod.TemplateMixin):
        default_context = {'foo': 'bar'}
        body = {}
    f = Foo()
    assert f.get_context() == {'foo': 'bar'}


def test_get_context_with_body():
    class Foo(mod.TemplateMixin):
        default_context = {'foo': 'bar'}
        body = {}
    f = Foo()
    f.body = {'this': 'that'}
    assert f.get_context() == {'foo': 'bar', 'this': 'that'}


def test_get_context_with_nondict_body():
    class Foo(mod.TemplateMixin):
        default_context = {'foo': 'bar'}
        body = {}
    f = Foo()
    f.body = 12
    assert f.get_context() == {'foo': 'bar', 'body': 12}


@mock.patch.object(mod.TemplateMixin, 'get_template_name')
@mock.patch.object(mod.TemplateMixin, 'get_context')
def test_render_template(get_context, get_template_name):
    mock_func = mock.Mock()

    class Foo(mod.TemplateMixin):
        template_func = mock_func
    f = Foo()
    f.render_template()
    mock_func.assert_called_once_with(get_template_name.return_value,
                                      get_context.return_value)


@mock.patch.object(mod.TemplateRoute, 'request')
@mock.patch.object(mod.TemplateRoute, 'render_template')
def test_template_route_renders(render_template, request):
    class Foo(mod.TemplateRoute):
        def get(self):
            pass
    request.method = 'GET'
    f = Foo()
    f.create_response()
    render_template.assert_called_once_with()


@mock.patch.object(mod.XHRPartialRoute, 'request')
def test_roca_normally_selects_default_template(request):
    class Foo(mod.XHRPartialRoute):
        template_name = 'foo'
        partial_template_name = 'bar'
    request.is_xhr = False
    f = Foo()
    ret = f.get_template_name()
    assert ret == 'foo'


@mock.patch.object(mod.XHRPartialRoute, 'request')
def test_roca_returns_partial_on_xhr(request):
    class Foo(mod.XHRPartialRoute):
        template_name = 'foo'
        partial_template_name = 'bar'
    request.is_xhr = True
    f = Foo()
    ret = f.get_template_name()
    assert ret == 'bar'


@mock.patch.object(mod.XHRPartialRoute, 'request')
@mock.patch.object(mod.XHRPartialRoute, 'response')
def test_roca_sets_cache_control_header_for_xhr(response, request):
    mock_func = mock.Mock()

    class Foo(mod.XHRPartialRoute):
        def get(self):
            pass
        template_name = 'foo'
        partial_template_name = 'bar'
        template_func = mock_func
    f = Foo()
    request.method = 'GET'
    request.is_xhr = True
    response.headers = {}
    f.create_response()
    assert response.headers == {'Cache-Control': 'no-store'}
    request.is_xhr = False
    response.headers = {}
    f.create_response()
    assert response.headers == {}
