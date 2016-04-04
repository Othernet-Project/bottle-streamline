Introduction to class-based route handlers
==========================================

Class-based route handlers (CBRH) can help you make your code more modular,
deal with complexity, and isolate pieces of code for better testability. In
order to take full advantage of the CBRHs, however, you will need to to have
good undestanding of Python OOP, and especially topics like inheritance and
mixins. It also helps to know a bit more about how bottle deals with handlers
in general, though we will disucss that briefly here.

Bottle route handlers behind the scenes
---------------------------------------

Conventional bottle route handlers are written as functions. There are also
many decorators that you can use to modify the way these functions work (e.g.,
a :py:func:`~bottle.@view` decorator that causes the output of your function
to be rendered using a template). 

Any parameters that are found in the path pattern that is associated with a
route handler will be mapped to the function's parameters. When the request is
made to the path, handler will receive parsed out data as arguments.

The return value of a route handler function can be:

- a string
- an iterable of strings
- :py:class:`bottle.HTTPResponse` object
- :py:class:`bottle.HTTPError` objecta string
- file-like object (:py:class:`~StringIO.StringIO`, file object, et al) 

.. note::
   For all practical purposes, special exceptions in the form of
   :py:class:`~bottle.HTTPResponse` and :py:class:`~bottle.HTTPError` objects
   (e.g., raised by :py:func:`bottle.abort()`) can be considered return values.
  
Bottle contains a function that looks at the return value, and then tries to
determine the type. It does different things depending on what the value is,
and converts it to a form that is compatible with the underlying WSGI protocol
(it expects an iterable). This function is :py:meth:`bottle.Bottle._cast()`.
Going through all the cases it handles would be too long, so we will only focus
on the iterables which are relevant to bottle-streamline.

If the return value of a route handler is an iterable, then
:py:meth:`~bottle.Bottle._cast()` attempts to fetch the first object. Failing
that, it returns an empty string.  If the first object is found, it checks its
type. It only allows two kinds of objects at this stage:

- :py:class:`~bottle.HTTPResponse`
- string (either ``unicode`` or ``bytes``)

If the first object is an :py:class:`~bottle.HTTPResponse` object,
:py:meth:`~bottle.Bottle._cast()` is called on it.

How CBRH fit into bottle route handling
---------------------------------------

When a CBRH is invoked, it is basically instantiated (its ``__init__`` method 
is invoked). Unlike handler functions, CBRHs don't do any actual work when they 
are invoked/instantiated. Instead, they implement the container interface of
the `iterator types
<https://docs.python.org/2/library/stdtypes.html#typeiter>`_ and presents
itself as an iterator. The entire CBRH object is, therefore, acts as a http
response.

.. note::
    CBRH classes are *not* subclasses of :py:class:`~bottle.HTTPResponse`.

The main implication of CBRH being an iterator container is that the response
body (discussed in later chapters) can only be a string or
:py:class:`~bottle.HTTPResponse` object. In your handler code, you cannot
expect to return any other kind of object. If you need to return objects other
than strings you need to either raise or return
:py:class:`~bottle.HTTPResponse` objects (these objects double as exception
classes so they can be raised) and pass the object you want to return as body. 
Here is an example::

    class MyRoute(RouteBase):
        def get(self):
            data = open('somefile.ext', 'r')
            return self.HTTPResponse(data)

The following chapters will go into the details of how to use CBRH classes in
different scenarios.
