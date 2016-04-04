Rendering templates
===================

Rendering templates is one of the most common tasks in most web applications.
bottle-streamline provides two classes that can be used for this purpose.

Simple template rendering
-------------------------

The simple variant is the :py:class:`streamline.template.TemplateRoute`, which
renders a single template for all methods.

Let's take a look at example code::

    from streamline import TemplateRoute


    class MyRoute(TemplateRoute):
        template_name = 'accounts/profile'

        def get(self, uid):
            return {'user': Users.get_by_id(uid)}

    
    MyRoute.route('/profiles/:uid')

If you remember what we've discussed about the return value of route handlers,
you will notice that a ``dict`` is not one of the allowed return values. This
is because a ``dict`` is not returned directly by
:py:class:`~streamline.template.TemplateRoute` handlers. 

The return value of the business logic methods is used as a template context,
and a template specified by the
:py:attr:`~streamline.template.TemplateRoute.template_name` is rendered and
returned as response (a string).

If you return any object other than a ``dict``, it wil also be made available
to the template context as ``body`` variable. The only exception is a
:py:class:`~bottle.HTTPResponse` object which completely bypasses template
rendering.

XHR partial rendering
---------------------

XHR partial rendering is a technique where we use full and partial 
HTML representations of a single resource and return one or the other depending
on whether a request is made using XHR (AJAX) or not. This can be useful for
partial page updates using XHR.

The :py:class:`streamline.template.XHRPartialRoute` is a variant of the
:py:class:`~streamline.template.TemplateRoute` which uses two template names
and selects an alternative template when a request is made using XHR.

Here is an example::

    from streamline import XHRPartialRoute


    class MyRoute(XHRPartialRoute):
        template_name = 'accounts/profile'
        partial_template_name = 'accounts/_profile'
        
        def get(self, uid):
            return {'user': Users.get_by_id(uid)}


    MyRoute.route('/profiles/:uid')

As we can see, most of the code is identical to the previous example, with the
addition of
:py:attr:`~streamline.template.XHRPartialRoute.partial_template_name` property.

Using a different rendering function
------------------------------------

The default implementation of the classes discussed in this chapter use
:py:func:`bottle.template` function to render the templates. You can override
this by assigning a different function to the ``template_func`` attribute on
both classes.

Default context
---------------

The default context can be changed globally by modifying the
:py:attr:`bottle.BaseTemplate.defaults` dict. This will change the default
context for all route handlers.

With CBRH, you can additionally change the default context of the route handler
classes by modifying the ``default_context`` property. By default, the default
context is ``{'request': bottle.request}``.

Dynamically changing parameters at runtime
------------------------------------------

All of the values we've covered thus far (``template_name``,
``partial_template_name``, ``template_func`` and ``default_context``) can be
also modified dynamically by overloading the following methods:

- ``get_template_name()``
- ``get_template_func()``
- ``get_default_context()``

In addition, the way final template context is calculated can also be changed.
By default, the context is calculated by merging the default context and the
return value of the business logic methods. By overloading the
``get_context()`` function, you can change this behavior.

Customizing the rendering function invocation
---------------------------------------------

The rendering function is invoked by passing the template name as first
positional argument, and template context as second. The function returns the
rendered template as a string or an iterable of strings. This is done in the
``render_template()`` method. You can customize the behavior by overloading
this method.
