=================
Bottle Streamline
=================

.. image:: https://readthedocs.org/projects/bottle-streamline/badge/?version=latest
    :target: http://bottle-streamline.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status
                
.. image:: https://readthedocs.org/projects/bottle-streamline/badge/?version=develop
    :target: http://bottle-streamline.readthedocs.org/en/develop/?badge=develop
    :alt: Development documentation Status

Bottle Streamline is a module that contains classes for writing class-based
route handlers for `Bottle <http://bottlepy.org>`_ applications.

Quick example
=============

Example of a classic Hello world app::

    import bottle
    from streamline import RouteBase


    class Hello(BaseRoute):
        def get(self):
            return 'Hello world!'


    Hello.route('/')
    bottle.run()

Documentation
=============

You will find the complete documentation and tutorials `on ReadTheDocs
<http://bottle-streamline.readthedocs.org/>`_.
