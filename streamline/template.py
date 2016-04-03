import bottle

from .base import RouteBase


class TemplateMixin(object):
    """
    Mixin that contains methods required to render templates.
    """

    template_name = None
    template_func = staticmethod(bottle.template)
    default_context = {'request': bottle.request}

    def get_template_name(self, template_name=None):
        """
        Returns template name. Default behavior is to return the value of the
        :py:attr:`~TemplateMixin.template_name` property.

        If ``template_name`` argument is specified, it will be used instead of
        the property.
        """
        template_name = template_name or self.template_name
        if not template_name:
            raise NotImplementedError('Missing template_name value')
        return template_name

    def get_default_context(self):
        """
        Returns default context. Default behavior is to return the value of the
        :py:attr:`~TemplateMixin.default_context` property. The property must
        be a dict, and it is copied before being returned so that the original
        remains intact.
        """
        return self.default_context.copy()

    def get_context(self):
        """
        Returns the complete template context. This context is is a dict, and
        is built from the default context by augmenting it with the contents of
        the ``body`` attribute on the route handler class.

        If ``body`` attribute is a dict, its keys are copied to inthe context.
        Otherwise, a new key, ``'body'`` is added and the value of the
        attribute is assigned to it.
        """
        ctx = self.get_default_context()
        if isinstance(self.body, dict):
            ctx.update(self.body)
        else:
            ctx['body'] = self.body
        return ctx

    def get_template_func(self):
        """
        Return a template rendering function. Default behavior is to return the
        :py:attr:`~TemplateMixin.template_func`, which must be a callable.
        """
        return self.template_func

    def render_template(self):
        """
        Renders the template using the template name, context, and function
        obtained by calling the respective methods.
        """
        template = self.get_template_name()
        ctx = self.get_context()
        fn = self.get_template_func()
        return fn(template, ctx)


class TemplateRoute(RouteBase, TemplateMixin):
    """
    Class that renders the response into a template.
    """

    def create_response(self):
        super(TemplateRoute, self).create_response()
        self.body = self.render_template()


class XHRPartialRoute(TemplateRoute, TemplateMixin):
    """
    Class that renders different templates depending on whether request is XHR
    or not.
    """

    partial_template_name = None

    def get_template_name(self):
        template_name = (self.partial_template_name
                         if self.request.is_xhr else None)
        return super(XHRPartialRoute, self).get_template_name(template_name)

ROCARoute = XHRPartialRoute
