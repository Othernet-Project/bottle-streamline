import pytest
import mock

from streamline import base as mod


MOD = mod.__name__


def test_get_generic_name():
    class FooBar(mod.RouteBase):
        pass
    exp = 'test_base:foo_bar'
    assert FooBar.get_generic_name() == exp


def test_get_generic_name_nested_module():
    class FooBar(mod.RouteBase):
        pass
    exp = 'module:foo_bar'
    with mock.patch.object(FooBar, '__module__', new='package.module'):
        assert FooBar.get_generic_name() == exp


def test_get_name():
    class FooBar(mod.RouteBase):
        name = 'teddy'
    assert FooBar.get_name() == 'teddy'


def test_get_name_generic_fallback():
    class FooBar(mod.RouteBase):
        pass
    exp = 'module:foo_bar'
    with mock.patch.object(FooBar, '__module__', new='package.module'):
        assert FooBar.get_name() == exp


def test_get_path():
    class FooBar(mod.RouteBase):
        path = '/teddy'
    assert FooBar.get_path() == '/teddy'


def test_get_path_no_default():
    class FooBar(mod.RouteBase):
        pass
    assert FooBar.get_path() is None


def test_no_valid_methods():
    class FooBar(mod.RouteBase):
        pass
    assert FooBar.get_valid_methods() == []


def test_valid_methods_get():
    class FooBar(mod.RouteBase):
        def get(self):
            pass

        def bar(self):
            pass
    assert FooBar.get_valid_methods() == ['GET']


@mock.patch.object(mod.RouteBase, 'bottle')
def test_route_defaults(bottle):
    app = bottle.default_app.return_value

    class FooBar(mod.RouteBase):
        pass
    FooBar.route('/foo')
    app.route.assert_called_once_with(
        '/foo',
        name='test_base:foo_bar',
        method=[],
        apply=None,
        skip=None,
        callback=FooBar)


@mock.patch.object(mod.RouteBase, 'bottle')
def test_route_custom_app(bottle):
    app = mock.Mock()

    class FooBar(mod.RouteBase):
        pass
    FooBar.route('/foo', app=app)
    app.route.assert_called_once_with(
        '/foo',
        name='test_base:foo_bar',
        method=[],
        apply=None,
        skip=None,
        callback=FooBar)


@mock.patch.object(mod.RouteBase, 'bottle')
def test_route_custom_name(bottle):
    app = bottle.default_app.return_value

    class FooBar(mod.RouteBase):
        pass
    FooBar.route('/foo', name='foo')
    app.route.assert_called_once_with(
        '/foo',
        name='foo',
        method=[],
        apply=None,
        skip=None,
        callback=FooBar)


@mock.patch.object(mod.RouteBase, 'bottle')
def test_route_class_specified_path(bottle):
    app = bottle.default_app.return_value

    class FooBar(mod.RouteBase):
        path = '/foo'
    FooBar.route(name='foo')
    app.route.assert_called_once_with(
        '/foo',
        name='foo',
        method=[],
        apply=None,
        skip=None,
        callback=FooBar)


@mock.patch.object(mod.RouteBase, 'bottle')
def test_route_class_specified_name(bottle):
    app = bottle.default_app.return_value

    class FooBar(mod.RouteBase):
        name = 'foo'
    FooBar.route('/foo')
    app.route.assert_called_once_with(
        '/foo',
        name='foo',
        method=[],
        apply=None,
        skip=None,
        callback=FooBar)


@mock.patch.object(mod.RouteBase, 'bottle')
def test_route_extra_params(bottle):
    app = bottle.default_app.return_value

    class FooBar(mod.RouteBase):
        pass
    FooBar.route('/foo', foo='bar')
    app.route.assert_called_once_with(
        '/foo',
        name='test_base:foo_bar',
        method=[],
        apply=None,
        skip=None,
        callback=FooBar,
        foo='bar')


@mock.patch.object(mod.RouteBase, 'bottle')
def test_route_custom_plugins(bottle):
    app = bottle.default_app.return_value

    class FooBar(mod.RouteBase):
        include_plugins = ['foo', 'bar', 'baz']
        exclude_plugins = ['fam', 'bam']
    FooBar.route('/foo')
    app.route.assert_called_once_with(
        '/foo',
        name='test_base:foo_bar',
        method=[],
        apply=['foo', 'bar', 'baz'],
        skip=['fam', 'bam'],
        callback=FooBar)


@mock.patch.object(mod.RouteBase, 'bottle')
def test_route_methods(bottle):
    app = bottle.default_app.return_value

    class FooBar(mod.RouteBase):
        def get(self):
            pass

        def post(self):
            pass

        def delete(self):
            pass
    FooBar.route('/')
    app.route.assert_called_once_with(
        '/',
        name='test_base:foo_bar',
        method=['GET', 'POST', 'DELETE'],
        apply=None,
        skip=None,
        callback=FooBar)


@mock.patch.object(mod.RouteBase, 'request')
def test_init_stashes_kwargs(request):
    class FooBar(mod.RouteBase):
        pass
    f = FooBar(1, 2, 3, foo='bar')
    assert f.args == (1, 2, 3)
    assert f.kwargs == dict(foo='bar')
    assert f.body == []


@mock.patch.object(mod.RouteBase, 'request')
def test_init_adds_app_attrib(request):
    class FooBar(mod.RouteBase):
        pass
    f = FooBar()
    assert f.app == request.app


@mock.patch.object(mod.RouteBase, 'request')
def test_init_adds_config_attrib(request):
    class FooBar(mod.RouteBase):
        pass
    f = FooBar()
    assert f.config == request.app.config


@mock.patch.object(mod.RouteBase, 'request')
@mock.patch.object(mod.RouteBase, 'abort')
def test_create_response_calls_available_methods(abort, request):
    class FooBar(mod.RouteBase):
        def get(self):
            pass
    f = FooBar()
    request.method = 'GET'
    with mock.patch.object(FooBar, 'get') as get:
        iter(f)
        get.assert_called_once_with()


@mock.patch.object(mod.RouteBase, 'request')
def test_call_with_arguments(request):
    class FooBar(mod.RouteBase):
        def get(self):
            pass
    f = FooBar(1, 2, foo='bar')
    request.method = 'GET'
    with mock.patch.object(FooBar, 'get') as get:
        iter(f)
        get.assert_called_once_with(1, 2, foo='bar')


@mock.patch.object(mod.RouteBase, 'request')
def test_create_response_calls_invalid_method(request):
    import bottle

    class FooBar(mod.RouteBase):
        def get(self):
            pass
    request.method = 'DELETE'
    f = FooBar()
    with pytest.raises(bottle.HTTPError):
        iter(f)
