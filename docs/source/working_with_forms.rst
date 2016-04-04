Working with forms
==================

While form handling is conceptually simple - user submits a form, which is
processed on the server - there are potentially many nuances that make things
more or less complicated. Instead of accounting for every possible workflow
involving forms, bottle-streamline provides simple classes that provide the
base for workflow-specific subclasses.

Form CBRH basics
----------------

The :py:class:`streamline.forms.SimpleFormRoute` is, as its name suggest, a
simple variant of form-handling CBRHs but it has all the fundamental pieces
that you need to know in order to work with other variants. Let's take a look
at an example of how to works::

    import bottle
    from streamline import FormRoute

    class Simple(FormRoute):
        def show_form(self):
            return 'Imagine this is a form'

        def form_valid(self):
            return 'OK'

        def form_invalid(self):
            self.response.status = 400
            return 'WRONG'

    Simple.route('/simple')


The ``show_form()`` method is normally used to render the form or otherwise
make the form controls available to the user. In this case, we're simply
returning a dummy string for simplicity. It's more or less an alias for
``get()`` and there is nothing wrong with overloading the ``get()`` method 
instead.

The ``form_valid()`` and ``form_invalid()`` methods are called depending on
whether the form is valid or not. ``Simple`` class has no validation code, so
it will always validate.

Let's add some validation code::

    try:
        unicode = unicode
    except NameError:
        unicode = str

    required = lambda v: v and v.strip()
    numeric = lambda v: unicode(v).strip().isnumeric() if v else True

The first lambda verfies that any data is entered and that the data is not just
a series of whitespace characters. Second lambda makes the value optional, but,
if specified, required it to be an integer. To make the two lambdas do
anything, we first need to add them to the validator
dictionary::

    Simple.form_factory.validators['string'] = required
    Simple.form_factory.validators['number'] = numeric

Now the ``Simple`` class is fully equipped to perform validation. Submitting
data to an app running 

.. note::
    The form CBRHs have a ``form_factory`` property, which is a function or a
    class that returns objects that implement the
    :py:class:`streamline.forms.FormAdaptor` API. The class itself can be used
    as a stand-alone rudimentary support code for data validation.

Let's test the form using curl::

    $ curl --data "string=test" localhost:8080/simple
    OK
    $ curl --data "number=12" localhost:8080/simple
    WRONG

It appears to be working.

Within the ``form_valid()`` and ``form_invalid()`` methods, the form object (as
returned by the factory function) is available as the ``form`` property. Let's
use this to show a bit more information on sucessful submission::

    def form_valid(self):
        return 'OK: {} {}'.format(self.form.data.get('string', ''),
                                  self.form.data.get('number', ''))

Let's test this::

    $ curl --data "string=test" localhost:8080/simple
    OK: test
    $ curl --data "string=test&number=2" localhost:8080/simple
    OK: test 2

Using form handling with template rendering
-------------------------------------------

Form handling with template rendering is a cross between the
:py:class:`~streamline.forms.FormRoute` and the two template classes,
:py:class:`~streamline.template.TemplateRoute` and
:py:class:`~streamline.template.XHRPartialRoute`. The two classes are
:py:class:`~streamline.forms.TemplateFormRoute` and
:py:class:`~streamline.forms.XHRPartialFormRoute`. 

We won't go into the details of how they work because they are simply a mix of
fetures provided by the template CBRHs and the features outlined in the
previous section.

Customizing form validation
---------------------------

Form validation can be customized in a few different ways. Most straightforward
way is to use a different (and proper) form or validation library and write an
adaptor for it. Another possibility is to override the ``validate_form()`` 
method. 

Here is an example of a custom form adaptor::

    from streamline.forms import FormAdaptor


    class MyAdaptor(FormAdaptor):
        def __init__(self, data):
            self.messages = {}
            super(MyAdaptor, self).__init__(data)

        def is_valid(self):
            try:
                my_cool_validation_library(self.data)
            except ValidationError as e:
                for error in e.errors:
                    self.messages[error.field_name] = error.message
            return not self.messages:


    class Simple(FormRoute):
        form_factory = MyAdaptor
        ...

The custom adaptor saves error messages in the ``messages`` property on the
adaptor object so that it can be accessed in the ``form_invalid()`` method
later.

Now let's take a look at the second option of overloading the validation
function::

    class Simple(FormRoute):
        def __init__(self, *args, **kwargs):
            super(Simple, self).__init__(*args, **kwargs)
            self.errors = {}

        def validate_form(self, _):
            # We will completely ignore the form that is passed in, and instead
            # use ``request.forms``
            data = self.request.forms
            try:
                my_cool_validation_library(data)
            except ValidationError as e:
                for error in e.errors:
                    self.errors[error.field_name] = error.message
            return not self.errors
            

It works similar to the first example, except we have chosen to ignore the form
object that is passed in as an argument to ``validate_form()``. The form object
passed to this method is a form object returned by the factory function so we
could have actually used the ``form.data`` instead of ``request.forms`` (they
are identical).

Performing a redirect on sucessful submission
---------------------------------------------

The most common way of performing a redirect is to use the bottle's own
:py:func:`~bottle.redirect` function. This function is made available as a
method on the CBRH instances. Here is an example::

    class Simple(FormRoute):
        ...
        def form_valid(self):
            return self.redirect('/see-other')
