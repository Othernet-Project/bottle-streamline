The basics
==========

The basic workflow when using bottle-streamline is to import a class that does
exactly what you need, or almost what you need, and subclass it. The most basic
of the classes is the :py:class:`streamline.base.RouteBase`.

Although you rarely need to use the :py:class:`~streamline.base.RouteBase`
class directly (unless you are trying to build your own reusable base class
that does things a bit diferently), it is prefect for demonstrating the
lower-level functionality of other classes. It is the base class after all.

Here is an example of a class that returns a simple string response::

    from streamline import RouteBase


    class MyRoute(RouteBase):
        def get(self, name):
            return 'Hello, {}!'.format(name)


    MyRoute.route('/hello/:name')

You can map the handler to a path by invoking the
:py:meth:`~streamline.base.RouteBase.route` method. This method takes a path as
first argument, optional route name as second argument, and an optional
application object as third. Under the hood, this method will invoke the
:py:meth:`bottle.Bottle.route` method to set up routing.

The ``MyRoute`` subclass has a single method, ``get()``
which (you've guessed correctly!) handles the HTTP GET method. The method takes
a single argument, ``name`` which comes from the placeholder pattern in
the path.

Named routes
------------

Named routes can be useful if you want to change the paths later. Instead of
using hard-coded paths, bottle allows you to construct the paths using a route
name and parameters. This is facilitated by the (somewhat `underdocumented
<http://bottlepy.org/docs/dev/api.html#bottle.Bottle.get_url>`_)
:py:meth:`~bottle.Bottle.get_url` method.

This method takes a route name as its first argument, and route parameters as
any number of additional keyword arguments.

All streamline CBRH are named by default, even if you don't explicitly specify
the name when invoking the :py:meth:`~streamline.base.RouteBase.route` method.
The default name is calculated by using the name of the module in which your
subclass resides, and the name of the class itself, which is decamelized. For
instance, if your subclass is ``users.AccountList``, it will be named
``users:account_list``. Keeping your route handlers neatly organized and named
will help you take advantage of this naming convention.

If you are not happy with the default names, you can supply an alternative
name::

    MyRoute.route('/hello/:name', name='hello')

You can also overload the
:py:meth:`~streamline.base.RouteBase.get_generic_name` method::

    class MyRoute(RouteBase):
        ....
        name = 'hello'
        
        @classmethod
        def get_generic_name(cls):
            return cls.name

The above example allows you to specify the route name as a ``name`` property.

Handling different HTTP methods
-------------------------------

In a single route, you can have any number of methods that match HTTP verbs,
and the route handler will be valid for those verbs. These methods can be:

- ``get()``
- ``post()``
- ``put()``
- ``patch()``
- ``delete()``

A handler will only be registered for the HTTP methods it supports, and result
in a HTTP 405 response for missing verbs.

You can have multiple route handlers with different verbs on the same path (if,
for example, you wish to have different handlers for different verbs).

Including and excluding plugins
-------------------------------

If you are using the bottle plugins, you can include additional plugins or skip
the default ones by using
:py:attr:`~streamline.base.RouteBase.include_plugins` and
:py:attr:`~streamline.base.RouteBase.exclude_plugins` attributes. Both are
lists of plugin names.

Here is an example::

    class MyRoute(RouteBase):
        include_plugins = ['auth', 'session']
        exclude_plugins = ['static']
        ....

Route configuration
-------------------

Normally, when invoking the :py:func:`bottle.route` function (or using it as a
decorator), you can pass additional keyword arguments which become part of what
is known as *route configuration*. The same is possible with the
:py:meth:`~streamline.base.RouteBase.route` method.

Convenience properties and methods
----------------------------------

The :py:class:`~streamline.base.RouteBase` class has several properties and
methods that are added to its namespace for your convenience. These are:

- :py:attr:`~streamline.base.RouteBase.bottle`: the :py:mod:`bottle` module
- :py:attr:`~streamline.base.RouteBase.request`: :py:data:`bottle.request` 
  object
- :py:attr:`~streamline.base.RouteBase.response`: :py:data:`bottle.response` 
  object
- :py:meth:`~streamline.base.RouteBase.abort`: :py:func:`bottle.abort`
  function
- :py:meth:`~streamline.base.RouteBase.redirect`: :py:func:`bottle.redirect` 
  function
- :py:attr:`~streamline.base.RouteBase.HTTPResponse`: 
  :py:class:`bottle.HTTPResponse` class

After initialization, two more properties will be available in the instances:

- :py:attr:`app`: application object that is tied to the request
- :py:attr:`config`: application's configuration
