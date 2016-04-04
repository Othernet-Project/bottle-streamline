import mock

from streamline import forms as mod


MOD = mod.__name__


# FormAdaptor


def test_form_adaptor_init():
    f = mod.FormAdaptor()
    assert f.data == {}
    f = mod.FormAdaptor({'foo': 'bar'})
    assert f.data == {'foo': 'bar'}


def test_form_adaptor_validator():
    class MyAdaptor(mod.FormAdaptor):
        validators = {
            'foo': lambda x: x == 'bar'  # foo field must be bar
        }
    f = MyAdaptor({'foo': 'bar'})
    assert f.is_valid() is True
    f = MyAdaptor({'foo': 'baz'})
    assert f.is_valid() is False


# FormMixin


def test_get_form_factory():
    class Foo(mod.FormMixin):
        form_factory = 'foo'
    f = Foo()
    assert f.get_form_factory() == 'foo'


def test_get_default_form_factory():
    class Foo(mod.FormMixin):
        pass
    f = Foo()
    assert f.get_form_factory() == mod.FormAdaptor


def test_get_unbound_form():
    class Foo(mod.FormMixin):
        form_factory = mock.Mock()
    f = Foo()
    frm = f.get_unbound_form()
    Foo.form_factory.assert_called_once_with()
    assert frm == Foo.form_factory.return_value


def test_get_bound_form():
    class Foo(mod.FormMixin):
        request = mock.Mock()
        form_factory = mock.Mock()
    f = Foo()
    frm = f.get_bound_form()
    Foo.form_factory.assert_called_once_with(Foo.request.forms)
    assert frm == Foo.form_factory.return_value


@mock.patch.object(mod.FormMixin, 'get_unbound_form')
@mock.patch.object(mod.FormMixin, 'get_bound_form')
def test_get_form(get_bound_form, get_unbound_form):
    class Foo(mod.FormMixin):
        request = mock.Mock()
        method = 'get'  # This is normally set in __init__, but this is mixin
        form_factory = mock.Mock()
    f = Foo()
    f.get_form()
    get_unbound_form.assert_called_once_with()
    Foo.method = 'post'
    f = Foo()
    f.get_form()
    get_bound_form.assert_called_once_with()


def test_validate_form():
    class Foo(mod.FormMixin):
        pass
    form = mock.Mock()
    f = Foo()
    ret = f.validate_form(form)
    form.is_valid.assert_called_once_with()
    assert ret == form.is_valid.return_value


def set_up_form_for_validate(valid):
    class Foo(mod.FormMixin):
        form_valid = mock.Mock()
        form_invalid = mock.Mock()
        form = mock.Mock()  # This is normally assigned in FormBase
    Foo.form.is_valid.return_value = valid
    return Foo()


def test_validate_valid():
    f = set_up_form_for_validate(valid=True)
    f.validate()
    assert f.form_valid.call_count == 1
    assert f.form_invalid.call_count == 0


def test_validate_invalid():
    f = set_up_form_for_validate(valid=False)
    f.validate()
    assert f.form_valid.call_count == 0
    assert f.form_invalid.call_count == 1


def test_form_valid_methods():
    class Foo(mod.RouteBase, mod.FormBase):
        pass
    assert Foo.valid_methods == ['GET', 'POST']


# SimpleFormRoute


@mock.patch.object(mod.FormRoute, 'request')
@mock.patch.object(mod.FormRoute, 'get_form')
def test_simple_form_form_attrib(get_form, request):
    form = mock.Mock()
    get_form.return_value = form
    request.method = 'GET'

    class Foo(mod.FormRoute):
        pass
    f = Foo()
    assert not hasattr(f, 'form')
    f.create_response()
    assert f.form == form


# FormRoute


@mock.patch.object(mod.TemplateFormRoute, 'request')
@mock.patch.object(mod.TemplateFormRoute, 'get_form')
@mock.patch.object(mod.TemplateFormRoute, 'render_template')
def test_form_route_form_attrib(render_template, get_form, request):
    form = mock.Mock()
    get_form.return_value = form
    request.method = 'GET'

    class Foo(mod.TemplateFormRoute):
        pass
    f = Foo()
    assert not hasattr(f, 'form')
    f.create_response()
    assert f.form == form


# XHRPartialFormRoute


@mock.patch.object(mod.XHRPartialFormRoute, 'request')
@mock.patch.object(mod.XHRPartialFormRoute, 'get_form')
@mock.patch.object(mod.XHRPartialFormRoute, 'render_template')
def test_roca_form_route_form_attrib(render_template, get_form, request):
    form = mock.Mock()
    get_form.return_value = form
    request.method = 'GET'

    class Foo(mod.XHRPartialFormRoute):
        pass
    f = Foo()
    assert not hasattr(f, 'form')
    f.create_response()
    assert f.form == form
